# Portfolio and interview summary

## Project description

Built a cloud-only Okta identity lab covering department-based group automation, SAML federation, group-targeted MFA, OIDC authorization-code testing, and SCIM account creation through a Flask API hosted on Render with Neon PostgreSQL storage.

## Resume bullets

- Configured department-based Okta group rules and verified Finance-to-Engineering reassignment using before/after membership and successful audit events.
- Implemented group-based SAML and OIDC application assignments, tested unassigned-user denial, and inspected department claims received by the SAML service provider and decoded OIDC ID token.
- Configured group-targeted MFA enrollment and application authentication policies, validating Okta Verify challenges and successful MFA audit events.
- Built and integrated a bearer-authenticated Flask SCIM service; verified Okta account creation through provisioning logs and authenticated retrieval of the active destination user.

## Interview explanation

“I built this lab to understand how identity data drives access and account provisioning. I tested department group changes, denied and allowed application access, SAML claims, MFA enforcement, OIDC token issuance, and SCIM user creation. I checked both Okta logs and the receiving system where evidence was available. The downstream department update remains unverified, and deactivation testing is incomplete, so I describe those limitations explicitly.”

## Claims to preserve accurately

This is hands-on lab experience. Do not describe it as a production rollout, full lifecycle completion, a cryptographic token-validation implementation, or a quantified operational improvement. The verified Okta department-group move is distinct from the unverified SCIM department update.
