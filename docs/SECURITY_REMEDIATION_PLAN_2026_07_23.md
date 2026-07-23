# Red Team AppSec Audit & Remediation Plan — BrineValue OS

**Date:** 2026-07-23  
**Scope:** Application security of on-prem CLI / FastAPI / Streamlit surfaces  
**Note:** Existing `docs/RED_TEAM_*.md` cover model/econ honesty, not cyber controls.

## Verdict

BrineValue is an offline screening library with optional unauthenticated local services.
Primary risk is **operator mis-deployment** (compose binding services to a reachable network)
combined with **HTML injection in reports** and **unbounded / weakly validated API input**.
No secrets store, no DB, no outbound integrations.

## Findings (priority)

| ID | Severity | Finding | Status |
|----|----------|---------|--------|
| RT-01 | High | HTML XSS via `brine.name` / meta strings in `report.py` (unescaped interpolation) | **Fixed** |
| RT-02 | High | Docker Compose bound API/UI to `0.0.0.0` without auth/TLS | **Fixed** (loopback default) |
| RT-03 | High | Unauthenticated `POST /analyze` with unconstrained `ions: dict` | **Fixed** (Pydantic bounds + optional token) |
| RT-04 | Medium | Container ran as root; full repo `COPY` | **Fixed** (non-root + slim COPY) |
| RT-05 | Medium | `Brine.validate()` accepted non-numeric strings via hard crash; unknown ions kept | **Fixed** |
| RT-06 | Medium | CSV/Excel garbage rows crashed or silently produced bad brines | **Fixed** (row errors) |
| RT-07 | Medium | CPU DoS via unauthenticated heavy `analyze()` (MC n=200 + DoE) | **Mitigated** (auth optional + bind localhost); full rate-limit deferred |
| RT-08 | Low | Streamlit default CORS / usage stats on exposed host | **Fixed** in compose flags |
| RT-09 | Low | CLI `--report` write without parent-dir check | **Fixed** |
| RT-10 | Info | No CI SAST / dependency pinning / SBOM | **Open** (plan below) |
| RT-11 | Info | No TLS in compose (acceptable for loopback; required if LAN publish) | **Open** |

## Fixes shipped in this pass

1. `brinevalue/report.py` — `html.escape` on all dynamic fields; safe badge CSS class allowlist.
2. `brinevalue/chemistry.py` — stricter `validate(strict_species=…)`, concentration/flow/name caps, coerce & drop unknown ions.
3. `brinevalue/api.py` — bounded `StreamIn`, 422 on bad input, optional `BRINEVALUE_API_TOKEN`, no stack leakage on 500.
4. `brinevalue/io.py` — numeric parse errors per cell; skip bad rows with warning.
5. `brinevalue/cli.py` — report parent exists; index/n bounds for demo/surrogate.
6. `Dockerfile` — non-root `brinevalue` user; copy only package + metadata.
7. `docker-compose.yml` — `127.0.0.1` binds; Streamlit XSRF on / CORS off; optional API token env; read-only FS.
8. `tests/test_security_redteam.py` — XSS + validation regressions.

## Residual risk & follow-up plan

### P0 — before any network exposure beyond localhost

- [ ] Set `BRINEVALUE_API_TOKEN` in production compose/env and require clients to send `X-API-Token`.
- [ ] Terminate TLS at reverse proxy (Caddy/nginx) if services must leave the host.
- [ ] Keep compose ports on `127.0.0.1` unless an authenticated proxy fronts them.
- [ ] Document that Streamlit has **no app-level password** in this package; use OS firewall / VPN / proxy auth.

### P1 — hardening (next sprint)

- [ ] Add FastAPI middleware: request body size limit, concurrent request semaphore / timeout around `analyze()`.
- [ ] Add `--with-doe` / lighter API mode (`with_doe=False`, smaller `n_robust`) as default for HTTP to cut CPU DoS surface.
- [ ] Pin dependencies (`requirements.lock` / `uv.lock`) and enable Dependabot / `pip-audit` in CI.
- [ ] Add GitHub Actions: `run_tests.py` + `pip-audit` + Bandit on `brinevalue/`.
- [ ] Streamlit: consider `streamlit-authenticator` or reverse-proxy basic auth if multi-user LAN use is required.

### P2 — hygiene

- [ ] `.env.example` documenting `BRINEVALUE_API_TOKEN`.
- [ ] SBOM (`cyclonedx` / `syft`) on release tags.
- [ ] Explicit security section in README (link this plan).
- [ ] Red-team retest checklist after each release (below).

## Retest checklist

1. Generate report with `name='</title><script>alert(1)</script>'` → no raw `<script>` in HTML.
2. `POST /analyze` with unknown ion / negative / NaN → HTTP 422.
3. With `BRINEVALUE_API_TOKEN=secret`, request without header → 401; with header → 200.
4. `docker compose up` → ports listen on `127.0.0.1` only (`ss`/`netstat`).
5. Container process UID ≠ 0.
6. `python run_tests.py` green including `tests.test_security_redteam`.

## Trust model (unchanged product intent)

On-prem advisory screening. Operators own network boundary. Cyber controls above make the **default** deploy match that intent; they do not make the tool a multi-tenant SaaS.
