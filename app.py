
import os
import re
import uuid
import hmac
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

SCIM_USER_SCHEMA = (
    "urn:ietf:params:scim:schemas:core:2.0:User"
)
SCIM_LIST_SCHEMA = (
    "urn:ietf:params:scim:api:messages:2.0:ListResponse"
)
SCIM_ERROR_SCHEMA = (
    "urn:ietf:params:scim:api:messages:2.0:Error"
)
SCIM_PATCH_SCHEMA = (
    "urn:ietf:params:scim:api:messages:2.0:PatchOp"
)
SCIM_ENTERPRISE_SCHEMA = (
    "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
)
ENTERPRISE_FIELDS = {
    "employeeNumber", "costCenter", "organization", "division", "department", "manager"
}

ALLOWED_FIELDS = {
    "userName", "externalId", "displayName",
    "name", "emails", "phoneNumbers", "active",
    "title", "nickName", "preferredLanguage",
    "locale", "timezone"
}


def db():
    return psycopg.connect(
        os.environ["DATABASE_URL"],
        row_factory=dict_row
    )


def initialize_database():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scim_users (
                id UUID PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                attributes JSONB NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)


def scim_response(data, status=200, headers=None):
    return Response(
        jsonify(data).get_data(),
        status=status,
        mimetype="application/scim+json",
        headers=headers
    )


def scim_error(status, detail):
    return scim_response({
        "schemas": [SCIM_ERROR_SCHEMA],
        "detail": detail,
        "status": str(status)
    }, status)


@app.before_request
def authenticate_scim():
    if not request.path.startswith("/scim/v2"):
        return

    expected = os.environ.get("SCIM_BEARER_TOKEN", "")
    supplied = request.headers.get("Authorization", "")

    if not expected or not supplied.startswith("Bearer "):
        return scim_error(401, "Unauthorized")

    token = supplied[len("Bearer "):]

    if not hmac.compare_digest(token, expected):
        return scim_error(401, "Unauthorized")


def normalize_user(payload, existing=None):
    if not isinstance(payload, dict):
        raise ValueError("Expected a SCIM user object")

    result = dict(existing or {})

    for key in ALLOWED_FIELDS:
        if key in payload:
            result[key] = payload[key]

    if not isinstance(result.get("userName"), str):
        raise ValueError("userName is required")

    result["userName"] = result["userName"].strip()

    if not result["userName"]:
        raise ValueError("userName cannot be empty")

    if not isinstance(result.get("active", True), bool):
        raise ValueError("active must be a boolean")

    result.setdefault("active", True)
    extension = payload.get(SCIM_ENTERPRISE_SCHEMA)
    if extension is not None:
        if not isinstance(extension, dict):
            raise ValueError("Enterprise extension must be an object")
        current = dict(result.get(SCIM_ENTERPRISE_SCHEMA) or {})
        for key in ENTERPRISE_FIELDS:
            if key in extension:
                current[key] = extension[key]
        if current:
            result[SCIM_ENTERPRISE_SCHEMA] = current

    result["schemas"] = [SCIM_USER_SCHEMA]
    if result.get(SCIM_ENTERPRISE_SCHEMA):
        result["schemas"].append(SCIM_ENTERPRISE_SCHEMA)

    return result


def serialize_user(row):
    user = dict(row["attributes"])
    user["id"] = str(row["id"])
    user["schemas"] = [SCIM_USER_SCHEMA]
    if user.get(SCIM_ENTERPRISE_SCHEMA):
        user["schemas"].append(SCIM_ENTERPRISE_SCHEMA)
    user["meta"] = {
        "resourceType": "User",
        "created": row["created_at"].isoformat(),
        "lastModified": row["updated_at"].isoformat(),
        "location": (
            request.url_root.rstrip("/")
            + "/scim/v2/Users/"
            + str(row["id"])
        )
    }
    return user


def get_user(conn, user_id):
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        return None

    return conn.execute(
        "SELECT * FROM scim_users WHERE id = %s",
        (uid,)
    ).fetchone()


@app.get("/")
def home():
    return jsonify({
        "service": "ZeroTrustNomad SCIM 2.0 Lab",
        "status": "running"
    })


@app.get("/scim/v2/ServiceProviderConfig")
def service_provider_config():
    return scim_response({
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"
        ],
        "patch": {"supported": True},
        "bulk": {"supported": False},
        "filter": {"supported": True, "maxResults": 100},
        "changePassword": {"supported": False},
        "sort": {"supported": False},
        "etag": {"supported": False},
        "authenticationSchemes": [{
            "type": "oauthbearertoken",
            "name": "Bearer Token",
            "description": "Static lab bearer token",
            "primary": True
        }]
    })


@app.get("/scim/v2/Users")
def list_users():
    filter_value = request.args.get("filter", "")
    try:
        start = max(1, int(request.args.get("startIndex", 1)))
        count = min(100, max(0, int(request.args.get("count", 100))))
    except ValueError:
        return scim_error(400, "Invalid pagination values")

    with db() as conn:
        if filter_value:
            match = re.fullmatch(
                r'(userName|externalId)\s+eq\s+"([^"]+)"',
                filter_value,
                re.IGNORECASE
            )

            if not match:
                return scim_error(400, "Unsupported SCIM filter")

            field, value = match.groups()
            field = (
                "userName"
                if field.lower() == "username"
                else "externalId"
            )

            rows = conn.execute(
                """SELECT * FROM scim_users
                   WHERE attributes ->> %s = %s
                   ORDER BY created_at, id""",
                (field, value)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM scim_users
                   ORDER BY created_at, id"""
            ).fetchall()

    total = len(rows)
    page = rows[start - 1:start - 1 + count]

    return scim_response({
        "schemas": [SCIM_LIST_SCHEMA],
        "totalResults": total,
        "startIndex": start,
        "itemsPerPage": len(page),
        "Resources": [serialize_user(row) for row in page]
    })


@app.post("/scim/v2/Users")
def create_user():
    try:
        user = normalize_user(request.get_json(silent=True))
    except ValueError as exc:
        return scim_error(400, str(exc))

    uid = uuid.uuid4()

    try:
        with db() as conn:
            row = conn.execute(
                """INSERT INTO scim_users
                   (id, username, attributes)
                   VALUES (%s, %s, %s)
                   RETURNING *""",
                (
                    uid,
                    user["userName"],
                    Jsonb(user)
                )
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        return scim_error(409, "userName already exists")

    resource = serialize_user(row)

    return scim_response(
        resource,
        201,
        {"Location": resource["meta"]["location"]}
    )


@app.get("/scim/v2/Users/<user_id>")
def retrieve_user(user_id):
    with db() as conn:
        row = get_user(conn, user_id)

    if not row:
        return scim_error(404, "User not found")

    return scim_response(serialize_user(row))


def update_record(conn, user_id, user):
    return conn.execute(
        """UPDATE scim_users
           SET username = %s,
               attributes = %s,
               updated_at = NOW()
           WHERE id = %s
           RETURNING *""",
        (
            user["userName"],
            Jsonb(user),
            uuid.UUID(user_id)
        )
    ).fetchone()


@app.put("/scim/v2/Users/<user_id>")
def replace_user(user_id):
    try:
        with db() as conn:
            existing = get_user(conn, user_id)

            if not existing:
                return scim_error(404, "User not found")

            user = normalize_user(
                request.get_json(silent=True)
            )
            row = update_record(conn, user_id, user)

    except ValueError as exc:
        return scim_error(400, str(exc))
    except psycopg.errors.UniqueViolation:
        return scim_error(409, "userName already exists")

    return scim_response(serialize_user(row))


@app.patch("/scim/v2/Users/<user_id>")
def patch_user(user_id):
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return scim_error(400, "Invalid SCIM PATCH request")

    if SCIM_PATCH_SCHEMA not in payload.get("schemas", []):
        return scim_error(400, "Missing SCIM PatchOp schema")

    operations = payload.get("Operations")

    if not isinstance(operations, list) or not operations:
        return scim_error(400, "PATCH operations are required")

    field_names = {
        field.lower(): field for field in ALLOWED_FIELDS
    }

    name_fields = {
        "givenname": "givenName",
        "familyname": "familyName",
        "middlename": "middleName",
        "formatted": "formatted",
        "honorificprefix": "honorificPrefix",
        "honorificsuffix": "honorificSuffix"
    }

    try:
        with db() as conn:
            existing = get_user(conn, user_id)

            if not existing:
                return scim_error(404, "User not found")

            user = dict(existing["attributes"])

            for operation in operations:
                if not isinstance(operation, dict):
                    raise ValueError("Invalid PATCH operation")

                action = str(operation.get("op", "")).lower()
                path = operation.get("path")
                value = operation.get("value")

                if action not in ("add", "replace", "remove"):
                    raise ValueError("Unsupported PATCH operation")

                if path is None:
                    if action == "remove":
                        raise ValueError("Remove requires a path")

                    if not isinstance(value, dict):
                        raise ValueError(
                            "Pathless PATCH requires an object"
                        )

                    for key, item in value.items():
                        if key == SCIM_ENTERPRISE_SCHEMA:
                            if not isinstance(item, dict):
                                raise ValueError("Invalid enterprise extension")
                            ext = dict(user.get(SCIM_ENTERPRISE_SCHEMA) or {})
                            for attr, attr_value in item.items():
                                if attr not in ENTERPRISE_FIELDS:
                                    raise ValueError("Unsupported enterprise attribute")
                                ext[attr] = attr_value
                            user[SCIM_ENTERPRISE_SCHEMA] = ext
                            continue
                        field = field_names.get(key.lower())

                        if field is None:
                            raise ValueError(
                                "Unsupported attribute: " + key
                            )

                        user[field] = item

                    continue

                if not isinstance(path, str):
                    raise ValueError("Invalid PATCH path")

                path = path.strip()
                field = field_names.get(path.lower())

                if field is not None:
                    if action == "remove":
                        if field in ("userName", "active"):
                            raise ValueError(
                                "Cannot remove required attribute"
                            )
                        user.pop(field, None)
                    else:
                        user[field] = value

                    continue

                if path.lower().startswith(SCIM_ENTERPRISE_SCHEMA.lower() + ":"):
                    attr = path[len(SCIM_ENTERPRISE_SCHEMA) + 1:]
                    enterprise_names = {k.lower(): k for k in ENTERPRISE_FIELDS}
                    attr = enterprise_names.get(attr.lower())
                    if attr is None:
                        raise ValueError("Unsupported enterprise PATCH path")
                    ext = dict(user.get(SCIM_ENTERPRISE_SCHEMA) or {})
                    if action == "remove":
                        ext.pop(attr, None)
                    else:
                        ext[attr] = value
                    if ext:
                        user[SCIM_ENTERPRISE_SCHEMA] = ext
                    else:
                        user.pop(SCIM_ENTERPRISE_SCHEMA, None)
                    continue

                if path.lower().startswith("name."):
                    child = path.split(".", 1)[1]
                    child = name_fields.get(child.lower())

                    if child is None:
                        raise ValueError(
                            "Unsupported name attribute"
                        )

                    name = dict(user.get("name") or {})

                    if action == "remove":
                        name.pop(child, None)
                    else:
                        name[child] = value

                    if name:
                        user["name"] = name
                    else:
                        user.pop("name", None)

                    continue

                raise ValueError(
                    "Unsupported PATCH path: " + path
                )

            user = normalize_user(user)
            row = update_record(conn, user_id, user)

    except ValueError as exc:
        return scim_error(400, str(exc))
    except psycopg.errors.UniqueViolation:
        return scim_error(409, "userName already exists")

    return scim_response(serialize_user(row))
