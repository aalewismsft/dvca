# Security Review Checklists

## A) Application Security Checklist
- [ ] User-controlled URL/input validated and normalized.
- [ ] SSRF controls reviewed (allowlist/blocklist, scheme restrictions, metadata endpoint protections).
- [ ] Outbound network restrictions assessed.
- [ ] Authn/authz expectations explicitly documented.
- [ ] Secrets are not logged, hardcoded, or returned to clients.
- [ ] Error handling avoids sensitive leakage.
- [ ] Security logging is sufficient for triage/audit.
- [ ] Intentional vulnerability labeling is present when applicable.

## B) IaC Security Checklist
- [ ] IAM follows least privilege and avoids unnecessary wildcards.
- [ ] Trust policies reviewed for overbroad principals.
- [ ] Security groups/network ACLs are justified for public ingress.
- [ ] Public bucket policies are necessary and documented.
- [ ] Encryption settings verified where applicable.
- [ ] Network segmentation and route exposure reviewed.
- [ ] Runtime hardening settings evaluated.
- [ ] Intentional vulnerability labeling is present when applicable.

## C) Supply Chain Checklist
- [ ] Python/runtime versions are supported and documented.
- [ ] Dependency vulnerabilities scanned and triaged.
- [ ] Container base image posture reviewed.
- [ ] Build/deploy credentials handling reviewed.
- [ ] Secret leakage checks passed.
- [ ] Exceptions include owner + expiration + rationale.

## D) Intentional Vulnerability Labeling Criteria
A change may be labeled intentional only if all are true:
- [ ] It is required for a specific training/demo objective.
- [ ] Scope is minimized to documented files/components.
- [ ] Risk acceptance includes owner, expiration, and compensating controls.
- [ ] A remediation/hardening alternative is documented for non-demo contexts.
