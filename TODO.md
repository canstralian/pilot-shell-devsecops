# TODO — Pilot Shell DevSecOps Fork

> **Living document** — Update as work progresses.
> Items are organized by implementation phase and priority.

---

## Now (P0/P1 — Immediate Focus)

### Security & Trust Boundaries

- [ ] Add installer binary integrity verification (SHA-256 + GPG signatures)
- [ ] Review and document trust model for external `grep-mcp` HTTP endpoint
- [ ] Add CodeQL SAST workflow to `.github/workflows/`
- [ ] Add Dependabot configuration for npm and pip dependencies
- [ ] Add GitHub dependency review workflow on PRs
- [ ] Create `pilot/rules/devsecops.md` — DevSecOps rules for AI agents
- [ ] Document remaining `DISABLE_INSTALLATION_CHECKS` risk in settings

### Documentation & Identity

- [x] Create `SECURITY.md` with responsible disclosure policy
- [x] Create `TODO.md` (this file)
- [ ] Create `FEATURES.md` with inherited vs fork-specific features
- [ ] Replace temporary `README.md` with credible DevSecOps positioning
- [ ] Create initial threat model document (`docs/threat-model.md`)
- [ ] Update `pilot/plugin.json` to add fork identity metadata (requires legal review)

### Repository Hygiene

- [x] Add basic issue templates (bug, feature, security)
- [ ] Add hardening task issue template
- [ ] Add release checklist issue template
- [ ] Document label taxonomy in `docs/label-taxonomy.md`
- [ ] Create release checklist document in `docs/release-checklist.md`
- [ ] Create release notes template for v0.1.0-alpha

---

## Next (P2 — Short-Term Work)

### Supply Chain & Releases

- [ ] Generate and publish SBOM for releases
- [ ] Add signed releases with GitHub attestations
- [ ] Implement SLSA Level 1+ build provenance
- [ ] Create fork-native release pipeline (independent from upstream)
- [ ] Document release process and artifact verification steps

### Documentation Replacement

- [ ] Replace upstream Docusaurus docs in `docs/docusaurus/` with fork-specific content
- [ ] Update `CHANGELOG.md` to reflect fork history starting point
- [ ] Update `cliff.toml` changelog header with fork attribution
- [ ] Review and update all `pyproject.toml` and `package.json` metadata

### MCP Security

- [ ] Develop MCP server allowlist policy
- [ ] Add per-server trust review documentation
- [ ] Evaluate alternatives to external `grep-mcp` HTTP endpoint
- [ ] Document MCP server threat model
- [ ] Consider migrating `npx -y` to locked npm workspace

---

## Later (P3 — Medium/Long-Term)

### Advanced Security Features

- [ ] Policy-as-code for agent rules (OPA or equivalent)
- [ ] Implement fine-grained permission model for MCP servers
- [ ] Add runtime sandboxing for MCP servers
- [ ] Implement secrets detection in pre-commit hooks
- [ ] Add compliance scanning (CIS benchmarks, etc.)

### Infrastructure & Tooling

- [ ] Secret scanning workflow integration
- [ ] Automated security testing in CI/CD
- [ ] Container security scanning (if applicable)
- [ ] License compliance checking
- [ ] Automated dependency update PR workflow

### Governance & Compliance

- [ ] Create SLSA provenance chain
- [ ] Document data retention and privacy policies
- [ ] Create security incident response playbook
- [ ] Establish security advisory process
- [ ] Create contribution security guidelines

---

## Blocked (Waiting on External Dependencies)

- [ ] Replace proprietary Pilot binary with open, auditable runtime (requires architectural decision)
- [ ] Fork-native MCP server implementations (blocked on upstream MCP protocol stability)
- [ ] Upstream plugin.json modification (blocked on legal review of attribution requirements)

---

## Done (Completed Items)

### Trust Boundary Hardening

- [x] Change `permissions.defaultMode` from `"bypassPermissions"` to `"default"`
- [x] Set `skipDangerousModePermissionPrompt` to `false`
- [x] Set `enableAllProjectMcpServers` to `false`
- [x] Pin all `npx` MCP server package versions in `.mcp.json`
- [x] Update `install.sh` REPO variable to point to fork
- [x] Remove upstream star tip from `pilot/settings.json`

### Documentation & Planning

- [x] Create `docs/devsecops-fork-roadmap.md` with audit and prioritization
- [x] Create `docs/fork-delta.md` tracking upstream divergence
- [x] Create `docs/hardening-note.md` documenting security changes
- [x] Replace temporary README with fork-specific positioning (temporary placeholder)

---

## Notes

### Priority Levels

- **P0**: Critical security or identity issues — ship blockers
- **P1**: High-impact security or trust improvements — should do immediately
- **P2**: Important improvements — schedule within next release cycle
- **P3**: Nice-to-have enhancements — backlog items

### Contribution Areas

High-value contributions include:

- Security workflow design and implementation
- DevSecOps-oriented AI agent rules
- Threat modeling and trust boundary analysis
- Supply chain security improvements
- Documentation cleanup and fork identity work

### Upstream Dependency Note

Some items depend on continued access to upstream `maxritter/pilot-shell` releases until the fork establishes its own independent release artifacts. This is documented in `docs/fork-delta.md`.

---

**Last Updated**: 2026-03-21
