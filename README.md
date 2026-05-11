# Damn Vulnerable Cloud Application
This is a demonstration project to show how to do privilege escalation on AWS. DO NOT deploy this on an AWS account unless you know very well what you are doing!

## Implemented Cloud Providers & Vulnerabilities
More details about how to use it are available on my [blog](https://medium.com/poka-techblog/privilege-escalation-in-the-cloud-from-ssrf-to-global-account-administrator-fd943cf5a2f6). For now, it's very AWS-centric, but the frontend is completely agnostic to the backend's technology, so if you want to contribute with a backend using other Cloud providers, I gladly accept PRs.

## Prerequisites
- A domain name managed by AWS
- The ACM Certificate ID associated to this domain
- A Wildcard Certificate associated to this domain
- The Hosted Zone ID associated to this domain

## Deployment
_In theory_, you should be able to deploy the Damn Vulnerable Cloud Application with a simple command:
```
make all DOMAIN_NAME=<your_aws_managed_domain_name> \
  ROOT_CERTIFICATE=<your_root_acm_certificate_id> \
  CERTIFICATE=<your_acm_certificate_id> \
  HOSTED_ZONE=<your_hosted_zone_id>
```

But the project is modular, so you could also deploy it in multiple steps. Typical `make` resources would be: prerequisites, frontend and a backend of your choice
```
make prerequisites DOMAIN_NAME=<your_aws_managed_domain_name> \
  CERTIFICATE=<your_acm_certificate_id> \
  HOSTED_ZONE=<your_hosted_zone_id>
make frontend DOMAIN_NAME=<your_aws_managed_domain_name> \
  ROOT_CERTIFICATE=<your_acm_certificate_id> \
  HOSTED_ZONE=<your_hosted_zone_id>
make fargate DOMAIN_NAME=<your_aws_managed_domain_name> \
  CERTIFICATE=<your_acm_certificate_id> \
  HOSTED_ZONE=<your_hosted_zone_id>
```
Just be careful: The frontend needs your root domain Certificate ID for the CloudFront distribution, while the rest just needs your wildcard Certificate ID

In the end, you should end-up with something like this  :-)

![DVCA](https://raw.githubusercontent.com/m6a-UdS/dvca/master/img/DVCA.png)

## Security Review Process
Security governance and review artifacts:
- Program policy and rollout: `/home/runner/work/dvca/dvca/docs/security/security-review-program.md`
- Asset inventory and trust boundaries: `/home/runner/work/dvca/dvca/docs/security/asset-inventory.md`
- Review checklists: `/home/runner/work/dvca/dvca/docs/security/checklists.md`
- OWASP compliance baseline: `/home/runner/work/dvca/dvca/docs/security/owasp-compliance.md`
- Exceptions register: `/home/runner/work/dvca/dvca/security/exceptions.json`

GitHub review and automation:
- PR template: `/home/runner/work/dvca/dvca/.github/pull_request_template.md`
- Security finding issue template: `/home/runner/work/dvca/dvca/.github/ISSUE_TEMPLATE/security-finding.yml`
- CODEOWNERS security sign-off scope: `/home/runner/work/dvca/dvca/.github/CODEOWNERS`
- Security workflows: `/home/runner/work/dvca/dvca/.github/workflows/security-review.yml`, `/home/runner/work/dvca/dvca/.github/workflows/codeql.yml`

