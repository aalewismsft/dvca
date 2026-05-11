# OWASP Compliance Baseline

This baseline applies to the web application components in this repository and is used during PR and release security reviews.

## Compliance Targets
- OWASP Top 10 risk coverage for web application changes.
- OWASP ASVS-aligned review evidence for authentication/session/input/output/error/logging controls.
- SSRF controls required for any server-side URL fetch path.

## Required Controls (Minimum)
- Input validation and canonicalization on all untrusted inputs.
- No insecure URL schemes for server-side requests.
- Block internal/private/link-local/metadata network targets from user-driven fetches.
- Consistent error responses that do not leak sensitive internals.
- Production-safe runtime settings (no debug mode in production paths).
- Security review evidence in PR for impacted controls.

## Evidence Requirements
A PR is considered OWASP-compliant only if it includes:
- Completed security checklist in PR template.
- Severity and disposition for security findings.
- Exception record with owner + expiration for any accepted intentional risk.
- Security owner sign-off for high-risk files.
