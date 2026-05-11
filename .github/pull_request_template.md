## Summary
- Describe the change and impacted areas.

## Security Review Scope
- [ ] Backend handlers changed
- [ ] IAM policy/trust policy changed
- [ ] Security group/network exposure changed
- [ ] Bucket policy/public access changed
- [ ] Deployment/container build path changed

## Security Checklist
### Application
- [ ] Input handling and SSRF implications reviewed
- [ ] Authn/authz expectations documented
- [ ] Secrets/logging/error handling reviewed

### IaC
- [ ] IAM least privilege and wildcards reviewed
- [ ] Network ingress/egress exposure reviewed
- [ ] Public data access policy reviewed

### Supply Chain
- [ ] Dependency and container risks reviewed
- [ ] Secret scan results reviewed

## Intentional Vulnerability Declaration
- [ ] No intentional vulnerability introduced/modified
- [ ] Intentional vulnerability introduced/modified (complete below)

If intentional vulnerability changed:
- Label: `intentional-vuln`
- Owner:
- Scope (files/resources):
- Reason:
- Expiration/review date:
- Risk acceptance link:

## Finding Risk Ratings and Disposition
| Finding/Area | Severity (Critical/High/Medium/Low) | Decision (Remediate/Accepted-Risk/Intentional-Vuln) | Owner | Due Date | Evidence |
|---|---|---|---|---|---|
| _example_ | Medium | Remediate | @owner | YYYY-MM-DD | link |

## Security Owner Sign-off (required for high-risk files)
- [ ] Security owner approved this PR
