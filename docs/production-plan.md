# Production Readiness Plan

This outlines how to take the simple random-number POC to a production-ready service.

## Architecture & Scalability
- **Runtime**: Keep FastAPI; containerize and run on managed orchestrator (EKS/ECS/Fargate or GKE). Use horizontal pod autoscaling on CPU/latency, with pod disruption budgets and multi-AZ clusters.
- **Ingress**: Front with a managed API Gateway or ALB/ELB for TLS termination, WAF, and request throttling. Enable gzip/brotli and connection reuse.
- **Statelessness**: Service remains stateless; use Redis or another cache only if high QPS requires memoization/rate state.
- **Configuration**: All config/env come from a managed secrets store (AWS Secrets Manager/SSM) and ConfigMap/Parameter Store with strict IAM.

## Deployment & Delivery
- **IaC**: Provision infra via Terraform (networking, clusters, IAM, registry, observability stack). Version everything.
- **Images**: Build via CI with pinned base images, SBOM (Syft) and signing (cosign). Push to ECR/GHCR and promote via tags.
- **Rollouts**: Use progressive delivery (rolling/update, blue-green, or canary with Argo Rollouts/Flagger). Enforce readiness/liveness probes.
- **Environments**: Separate dev/stage/prod with isolated accounts/VPCs; use short-lived preview envs for PRs.

## Security
- **Supply chain**: Dependabot/Renovate for deps; SAST (bandit/semgrep), container scan (Trivy/Grype) in CI; verify signatures on pull.
- **Runtime**: Non-root containers, read-only FS where possible, seccomp/AppArmor, minimal permissions (IAM roles for service accounts).
- **Network**: TLS everywhere, mTLS service-to-service if in mesh (Istio/Linkerd). Restrict inbound via WAF and security groups; egress via NAT with allowlists.
- **AuthN/Z**: If exposed publicly, front with OIDC/JWT validation at the gateway. Rate limiting and DoS protections at edge.

## Observability & Operations
- **Logging**: Structured JSON logs to centralized sink (CloudWatch/ELK/OpenSearch). Correlate with request IDs; include latency and bounds used.
- **Metrics**: Export Prometheus metrics (request count/latency, error rates, RNG bounds). Define SLOs (e.g., p95 < 150ms, error rate <0.1%).
- **Tracing**: OpenTelemetry auto-instrumentation; export to Tempo/Jaeger/XRay.
- **Health**: `/health` for liveness and `/ready` for readiness (ensuring deps reachable).
- **Runbooks**: Playbooks for on-call, incident comms, and rollback steps. DR via multi-AZ and backup/restore drills.

## Data & Compliance
- **Determinism**: If auditability matters, capture seed and RNG source; otherwise ensure RNG uses `secrets` for stronger entropy.
- **Compliance**: Maintain audit trails for deployments and access; enforce least privilege on CI and registries.

## Future Evolution
- **API Growth**: Version the API; add OpenAPI docs and client SDK generation. Use contract tests for backward compatibility.
- **Performance**: Add caching/batching if upstream RNG changes; benchmark with k6/Locust before releases.
- **Cost**: Auto-scale to zero in dev; spot instances or serverless (Lambda + ALB) if latency profile allows.
