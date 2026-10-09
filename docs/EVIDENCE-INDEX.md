# Screenshot evidence index

All 47 supplied screenshots are preserved in sequence. Filenames and captions describe the visible evidence rather than treating the uploaded titles as proof. Image pixels are unchanged.

| No. | Screenshot | Evidence and interpretation |
| --- | --- | --- |
| 01 | [01-cloud-iam-group-architecture.png](../screenshots/01-groups/01-cloud-iam-group-architecture.png) | Department, application entitlement, and MFA policy groups configured in Okta. |
| 02 | [02-engineering-user-group-membership.png](../screenshots/01-groups/02-engineering-user-group-membership.png) | Alex belongs to Engineering; initial membership snapshot. |
| 03 | [03-finance-user-group-membership.png](../screenshots/01-groups/03-finance-user-group-membership.png) | Jordan belongs to Finance; initial membership snapshot. |
| 04 | [04-engineering-group-rule-preview-match.png](../screenshots/01-groups/04-engineering-group-rule-preview-match.png) | Engineering department rule preview matches Alex. |
| 05 | [05-engineering-rule-managed-membership.png](../screenshots/01-groups/05-engineering-rule-managed-membership.png) | Alex Engineering membership is managed by the department rule. |
| 06 | [06-pre-mover-finance-rule-managed-membership.png](../screenshots/01-groups/06-pre-mover-finance-rule-managed-membership.png) | Jordan Finance membership is managed by the department rule before the move. |
| 07 | [07-post-mover-automatic-group-reassignment.png](../screenshots/01-groups/07-post-mover-automatic-group-reassignment.png) | Jordan belongs to rule-managed Engineering after the move; Finance is absent. |
| 08 | [08-mover-automated-group-reassignment-audit-log.png](../screenshots/01-groups/08-mover-automated-group-reassignment-audit-log.png) | System Log records successful profile update, Finance removal, and Engineering addition. |
| 09 | [09-saml-attribute-claim-mapping.png](../screenshots/02-saml/09-saml-attribute-claim-mapping.png) | SAML department and email attribute expressions configured. |
| 10 | [10-saml-group-based-app-assignment.png](../screenshots/02-saml/10-saml-group-based-app-assignment.png) | SAML application assigned to its entitlement group. |
| 11 | [11-saml-unassigned-user-access-denied.png](../screenshots/02-saml/11-saml-unassigned-user-access-denied.png) | Unassigned Alex receives an application-assignment denial. |
| 12 | [12-saml-entitlement-group-user-assignment.png](../screenshots/02-saml/12-saml-entitlement-group-user-assignment.png) | Alex manually assigned to the SAML entitlement group. |
| 13 | [13-saml-two-factor-authentication-policy-requirement.png](../screenshots/02-saml/13-saml-two-factor-authentication-policy-requirement.png) | Two-factor application policy rule configured. |
| 14 | [14-saml-app-two-factor-policy-assignment.png](../screenshots/02-saml/14-saml-app-two-factor-policy-assignment.png) | SAML application appears under the two-factor policy. |
| 15 | [15-okta-verify-fastpass-user-verification-enabled.png](../screenshots/02-saml/15-okta-verify-fastpass-user-verification-enabled.png) | Okta Verify enrollment completed with user verification enabled. |
| 16 | [16-fastpass-remediation-success-audit-log.png](../screenshots/02-saml/16-fastpass-remediation-success-audit-log.png) | System Log shows earlier policy denials and subsequent successful sign-on and verification; chronology does not establish every cause. |
| 17 | [17-successful-saml-sso-event-details.png](../screenshots/02-saml/17-successful-saml-sso-event-details.png) | Successful SAML application sign-on event details. |
| 18 | [18-okta-verify-successful-authentication-audit-event.png](../screenshots/02-saml/18-okta-verify-successful-authentication-audit-event.png) | Successful user.authentication.verify event involving Okta Verify. |
| 19 | [19-saml-real-service-provider-configuration.png](../screenshots/02-saml/19-saml-real-service-provider-configuration.png) | SAML service-provider ACS URL and audience configured. |
| 20 | [20-end-to-end-saml-federation-success.png](../screenshots/02-saml/20-end-to-end-saml-federation-success.png) | Service provider reports successful federation and displays Alex NameID. |
| 21 | [21-saml-attribute-claims-received-by-service-provider.png](../screenshots/02-saml/21-saml-attribute-claims-received-by-service-provider.png) | Service provider displays received Engineering department and email attributes. |
| 22 | [22-saml-assertion-details-inspection.png](../screenshots/02-saml/22-saml-assertion-details-inspection.png) | Assertion details inspected: issuer, audience, timestamps, and hashing algorithm; independent signature-validation testing is not shown. |
| 23 | [23-group-targeted-mfa-enrollment-policy.png](../screenshots/03-mfa/23-group-targeted-mfa-enrollment-policy.png) | Active group-targeted enrollment policy requires Password and Okta Verify. |
| 24 | [24-mfa-policy-group-user-assignment.png](../screenshots/03-mfa/24-mfa-policy-group-user-assignment.png) | Alex assigned to the MFA policy group. |
| 25 | [25-group-targeted-mfa-authentication-rule.png](../screenshots/03-mfa/25-group-targeted-mfa-authentication-rule.png) | Enabled authentication rule targets the MFA group and requires two factor types. |
| 26 | [26-mfa-policy-protected-application-assignment.png](../screenshots/03-mfa/26-mfa-policy-protected-application-assignment.png) | SAML application assigned to the group-targeted MFA authentication policy. |
| 27 | [27-mfa-fastpass-second-factor-challenge.png](../screenshots/03-mfa/27-mfa-fastpass-second-factor-challenge.png) | Okta Verify prompts for Touch ID or password to verify the user. |
| 28 | [28-mfa-enforced-saml-access-success.png](../screenshots/03-mfa/28-mfa-enforced-saml-access-success.png) | Successful SAML federation after the authentication challenge. |
| 29 | [29-group-targeted-mfa-policy-challenge-audit-event.png](../screenshots/03-mfa/29-group-targeted-mfa-policy-challenge-audit-event.png) | Policy evaluation records CHALLENGE for the named group-targeted rule. |
| 30 | [30-group-targeted-mfa-success-audit-event.png](../screenshots/03-mfa/30-group-targeted-mfa-success-audit-event.png) | Authentication via MFA records SUCCESS involving Okta Verify. |
| 31 | [31-oidc-confidential-web-client-configuration.png](../screenshots/04-oidc/31-oidc-confidential-web-client-configuration.png) | OIDC application configured for client-secret authentication; secret remains masked; PKCE requirement is unchecked. |
| 32 | [32-oidc-department-token-claim-configuration.png](../screenshots/04-oidc/32-oidc-department-token-claim-configuration.png) | Department token claim expression configured as user.profile.department. |
| 33 | [33-oidc-group-based-application-assignment.png](../screenshots/04-oidc/33-oidc-group-based-application-assignment.png) | OIDC application assigned to its entitlement group. |
| 34 | [34-oidc-authorization-code-and-redirect-uri-configuration.png](../screenshots/04-oidc/34-oidc-authorization-code-and-redirect-uri-configuration.png) | Authorization Code grant and allowed redirect URIs configured; this does not prove all listed redirect paths were exercised. |
| 35 | [35-oidc-unassigned-user-access-denied.png](../screenshots/04-oidc/35-oidc-unassigned-user-access-denied.png) | OIDC request denied because the user is not assigned to the client application. |
| 36 | [36-oidc-entitlement-group-user-assignment.png](../screenshots/04-oidc/36-oidc-entitlement-group-user-assignment.png) | Alex assigned to the OIDC entitlement group. |
| 37 | [37-oidc-id-token-claims-inspection.png](../screenshots/04-oidc/37-oidc-id-token-claims-inspection.png) | ID-token payload decoded and selected claims inspected, including Engineering; signature validation is not shown. |
| 38 | [38-oidc-authorization-token-success-audit-trail.png](../screenshots/04-oidc/38-oidc-authorization-token-success-audit-trail.png) | System Log records successful authorization-code request, sign-on, ID-token issuance, and access-token issuance. |
| 39 | [39-scim-cloud-api-successful-deployment.png](../screenshots/05-scim/39-scim-cloud-api-successful-deployment.png) | Render reports a successful deployment and live web service. |
| 40 | [40-scim-unauthorized-request-denied.png](../screenshots/05-scim/40-scim-unauthorized-request-denied.png) | Unauthenticated request receives a SCIM-formatted error with status 401. |
| 41 | [41-scim-authenticated-api-capabilities.png](../screenshots/05-scim/41-scim-authenticated-api-capabilities.png) | ServiceProviderConfig advertises PATCH, filtering, and static bearer authentication; advertisement alone is not execution evidence. |
| 42 | [42-scim-authenticated-empty-user-list.png](../screenshots/05-scim/42-scim-authenticated-empty-user-list.png) | Bearer-authenticated GET Users returns HTTP 200 and an initially empty SCIM ListResponse. |
| 43 | [43-okta-scim-api-credentials-verified.png](../screenshots/05-scim/43-okta-scim-api-credentials-verified.png) | Okta Test API Credentials reports successful verification; bearer token is masked. |
| 44 | [44-okta-scim-lifecycle-provisioning-settings.png](../screenshots/05-scim/44-okta-scim-lifecycle-provisioning-settings.png) | Create Users, Update User Attributes, and Deactivate Users enabled; settings alone do not prove execution. |
| 45 | [45-okta-scim-user-provisioning-success.png](../screenshots/05-scim/45-okta-scim-user-provisioning-success.png) | Okta logs successful push of a new Alex account to the external application. |
| 46 | [46-scim-provisioned-user-api-retrieval.png](../screenshots/05-scim/46-scim-provisioned-user-api-retrieval.png) | Authenticated GET Users returns HTTP 200 and Alex active account; API retrieval, not a direct database-console query. |
| 47 | [47-okta-scim-profile-push-success-event.png](../screenshots/05-scim/47-okta-scim-profile-push-success-event.png) | Okta profile-push event reports SUCCESS; no downstream department value or before/after comparison is shown. |
