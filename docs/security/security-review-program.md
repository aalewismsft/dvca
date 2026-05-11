# Security Review Program

## Scope and Guardrails

This repository is intentionally vulnerable for cloud-security training and demonstrations. Security reviews in this repository are for **intentional-vulnerability governance** by default, not automatic hardening of all known weaknesses.

### Security review objectives
- Preserve intentionally vulnerable learning paths when explicitly documented and approved.
- Prevent accidental vulnerabilities from being introduced without review.
- Require explicit risk acceptance for intentionally unsafe components.
- Maintain auditable security decisions for pull requests and releases.

### Intentional vs accidental vulnerability policy
A security-relevant change must be labeled as one of:

1. **Intentional Vulnerability (IV)**
   - Required for demo/training objective.
   - Must include:
     - explicit label (`intentional-vuln`),
     - rationale,
     - owner,
     - scope/path,
     - expiration/review date,
     - risk-acceptance record.
2. **Accidental Vulnerability (AV)**
   - Any vulnerability not explicitly declared as intentional.
   - Must be fixed or formally accepted through the security exception workflow.

If unclear, classify as **AV** until triage completes.

## Review Domains

Security reviews are required for changes to:
- Backend handlers (`docker-backend`, `serverless-backend`)
- IAM policies and trust policies (`cloudformation/**`)
- Security groups/network routes (`cloudformation/**`)
- Public bucket/domain policies (`cloudformation/**`)
- Deployment scripts and container definitions (`Makefile`, `docker-backend/*`)

## Triage and Remediation Lifecycle

### Severity model
- **Critical**: Immediate compromise likely (privilege escalation, exposed credentials, unrestricted critical access).
- **High**: Major impact or exploitable weakness with realistic attack path.
- **Medium**: Important security issue with constrained impact/exploitability.
- **Low**: Minor weakness, defense-in-depth gap, or hardening item.

### SLA targets
| Severity | Production-like exposure | Demo-only exposure |
|---|---:|---:|
| Critical | 24 hours | 5 business days |
| High | 3 business days | 10 business days |
| Medium | 15 business days | 30 business days |
| Low | 45 business days | 90 business days |

### Finding workflow
1. Open/update a security finding item (issue template) with owner, due date, severity, status, and evidence.
2. Record disposition: `remediate`, `accepted-risk`, `intentional-vuln`.
3. Provide closure evidence: code diff, scan output, or approved exception.
4. Close only after reviewer validation.

## Release/Deployment Security Checkpoints
Before deployment:
- No unapproved Critical/High findings.
- PR security checklist completed.
- Exceptions approved only for intentional-vulnerability scenarios.
- Security decision log entry recorded for the release.

## Rollout Phases
1. **Phase 1**: Policy, inventory, checklists, PR workflow.
2. **Phase 2**: CI checks in monitor/report-only mode and baseline collection.
3. **Phase 3**: Enforce fail-on-critical/high for non-excepted findings.
4. **Phase 4**: Quarterly control review and exception cleanup.

## Default answers to open decisions
- Preserve intentional vulnerabilities for training/demo unless a hardening objective is explicitly declared.
- Begin CI checks in report-only mode.
- Use semgrep + checkov + trivy + gitleaks + CodeQL.
- Apply review scope across EC2, Fargate, and Serverless backends.
