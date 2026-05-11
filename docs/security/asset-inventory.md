# Security Asset and Trust-Boundary Inventory

## Security-relevant assets

### Application code
- `/home/runner/work/dvca/dvca/docker-backend/app.py`
  - Flask endpoint `/test-hook` accepts user-controlled URL and performs server-side fetch.
  - Highly sensitive for SSRF and metadata credential exposure scenarios.
- `/home/runner/work/dvca/dvca/serverless-backend/webhook-tester.py`
  - Lambda handler accepts user-controlled URL and fetches arbitrary URL content.
  - Sensitive for SSRF, cloud metadata, and role-abuse paths.

### Frontend interaction layer
- `/home/runner/work/dvca/dvca/static-frontend/assets/js/main.js`
  - Browser form submits handler URL to selected backend domain.
  - Trust boundary from untrusted browser input to privileged backend fetch logic.

### Infrastructure as code
- `/home/runner/work/dvca/dvca/cloudformation/**/*.yml`
  - IAM roles/trust relationships, ECS task role, EC2 execution role.
  - Security groups with internet ingress in selected components.
  - Public bucket policy and cloud edge/domain routing.

### Deployment and runtime
- `/home/runner/work/dvca/dvca/Makefile`
  - CloudFormation deployment and ECR image push path.
- `/home/runner/work/dvca/dvca/docker-backend/Dockerfile`
  - Runtime supply-chain and container hardening posture.
- `/home/runner/work/dvca/dvca/docker-backend/requirements.txt`
  - Python dependency risk surface.

## Trust boundaries and data flow
1. **Browser/User Input → Frontend JS**
   - User-controlled `handler` URL and backend selection are untrusted.
2. **Frontend JS → Public Backend Endpoints**
   - POST to `/test-hook` on serverless/fargate/ec2 backend domains.
3. **Backend Endpoint → Outbound URL Fetch**
   - Backend performs server-side URL retrieval based on user input.
4. **Backend Runtime → Cloud Metadata/Credentials**
   - SSRF path can target metadata and container credential endpoints.
5. **Runtime Credentials → AWS APIs**
   - Potential use of IAM role credentials for S3/ECR/STS actions.
6. **Infrastructure Control Plane**
   - CloudFormation/IAM/network definitions define reachable attack paths.

## Priority review hotspots
- Backend URL fetch handlers (`app.py`, `webhook-tester.py`)
- CloudFormation IAM policies with wildcard resources/actions
- Security groups/bucket policies exposing public access
- Deployment credentials and image provenance steps
