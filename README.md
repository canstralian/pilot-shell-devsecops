# Pilot Shell DevSecOps

**A security-hardened fork of Pilot Shell for controlled, auditable, AI-assisted software development.**

---

## What This Is

This is a **DevSecOps-oriented fork** of the [Pilot Shell](https://github.com/maxritter/pilot-shell) project. It adapts Pilot's structured workflow foundation—spec-driven development, AI agent orchestration, and quality automation—toward:

- **Explicit trust boundaries** — Permission prompts before dangerous operations
- **Safer defaults** — Reduced ambient trust in execution and MCP loading
- **Supply chain integrity** — Version-pinned dependencies and verifiable artifacts
- **Evidence-based security** — Documented threat surfaces and honest limitations
- **Policy-backed development** — Secure-by-default workflows over convenience-first automation

---

## What Differs from Upstream

This fork makes **targeted security improvements** while preserving Pilot's core workflow capabilities:

| Area | Upstream | This Fork |
|------|----------|-----------|
| **Permission model** | Bypasses prompts by default | Requires explicit approval |
| **MCP server loading** | Auto-loads all project servers | Explicit opt-in required |
| **Dependency pinning** | Unpinned \`npx -y\` packages | Version-locked MCP servers |
| **Installer provenance** | Points to upstream | Points to fork repository |
| **Security documentation** | Limited | Comprehensive threat model, hardening notes |
| **Core workflows** | Spec-driven dev, quality hooks | Fully retained |

See **[docs/fork-delta.md](docs/fork-delta.md)** for complete divergence tracking.

---

## Key Features

### Inherited from Upstream (Retained)

- **Spec-driven development** — \`/spec\` command for structured planning, implementation, and verification
- **Quality automation** — Auto-linting, formatting, type-checking, and TDD enforcement
- **Multi-agent orchestration** — Specialized agents for planning, coding, and review
- **Persistent memory** — Context preservation across sessions
- **MCP integration** — Model Context Protocol servers for extended capabilities
- **LSP support** — Real-time diagnostics for Python, TypeScript, and Go
- **Console web UI** — Session browser, memory explorer, and skill management at \`localhost:41777\`

### Fork-Specific Hardening

- **Permission prompts** — Explicit approval required for dangerous operations
- **MCP opt-in model** — Project servers must be explicitly enabled
- **Pinned dependencies** — MCP packages locked to specific versions
- **Security policy** — Responsible disclosure process in [SECURITY.md](SECURITY.md)
- **Hardening roadmap** — Prioritized security work in [docs/devsecops-fork-roadmap.md](docs/devsecops-fork-roadmap.md)
- **Audit documentation** — Trust boundary analysis and residual risk disclosure

---

## Current State

**Status**: Alpha — hardening in progress.

This fork has completed the first phase of trust boundary reset:

✅ **Done**:
- Safer default permissions (\`bypassPermissions\` → \`default\`)
- MCP version pinning and opt-in loading
- Installer fork provenance
- Security documentation (roadmap, threat surfaces, hardening notes)
- Issue templates and label taxonomy

⏳ **In Progress**:
- Installer binary integrity verification
- Signed releases with GitHub attestations
- CodeQL SAST workflow
- DevSecOps agent rules

❌ **Not Yet Implemented**:
- SBOM generation
- SLSA provenance chain
- Fork-native binary releases
- Complete documentation replacement

See **[TODO.md](TODO.md)** for the full backlog and **[FEATURES.md](FEATURES.md)** for detailed feature inventory.

---

## Installation

### Requirements

- **Platforms**: macOS, Linux, or WSL2
- **Tools**: \`curl\` or \`wget\`, \`git\`, \`bash\`
- **Claude API access**: Required for AI agent functionality

### Install Command

\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/canstralian/pilot-shell-devsecops/main/install.sh | bash
\`\`\`

Or specify a version:

\`\`\`bash
VERSION=0.1.0-alpha curl -fsSL https://raw.githubusercontent.com/canstralian/pilot-shell-devsecops/main/install.sh | bash
\`\`\`

### Post-Install

- Run \`/setup-rules\` after installation to generate project-specific rules
- Review settings in \`~/.claude/pilot/settings.json\`
- Enable MCP servers explicitly if needed

### Uninstall

\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/canstralian/pilot-shell-devsecops/main/uninstall.sh | bash
\`\`\`

---

## Quick Start

### Spec-Driven Development

For features, bug fixes, or any structured work:

\`\`\`bash
pilot
> /spec "Add user authentication with JWT tokens"
\`\`\`

Pilot will:
1. Explore your codebase
2. Ask clarifying questions
3. Generate a plan for review
4. Implement with quality checks
5. Verify with tests and code review

### Quick Mode

For small changes or exploration:

\`\`\`bash
pilot
> Fix the typo in README.md
\`\`\`

Quality hooks still run, but without the full spec workflow.

---

## Security Principles

This fork is guided by these principles:

1. **Explicit over implicit** — Require approval for trust escalation
2. **Evidence over claims** — Document actual controls, not aspirations
3. **Honest limitations** — Disclose what's not yet hardened
4. **Minimal ambient trust** — Reduce default permission surfaces
5. **Verifiable supply chain** — Pin, sign, and attest artifacts
6. **Transparent operation** — Clear data flows and trust boundaries

---

## Threat Model

### Current Trust Surfaces

**High Risk**:
- Installer binary downloaded without integrity verification
- Proprietary \`pilot\` runtime binary (closed-source, not independently auditable)

**Medium Risk**:
- External MCP HTTP endpoint (\`grep-mcp\` at \`https://mcp.grep.app\`)
- \`npx -y\` auto-install flag (even with pinned versions)
- \`DISABLE_INSTALLATION_CHECKS\` enabled for CI compatibility

**Mitigated**:
- ~~Silent permission bypass~~ → Explicit prompts now required
- ~~Auto-trust all MCP servers~~ → Opt-in model now enforced
- ~~Unpinned runtime dependencies~~ → MCP versions now locked

See **[docs/devsecops-fork-roadmap.md](docs/devsecops-fork-roadmap.md)** for the full audit and prioritized hardening work.

---

## Documentation

- **[docs/devsecops-fork-roadmap.md](docs/devsecops-fork-roadmap.md)** — Security audit, prioritized work, and next steps
- **[docs/fork-delta.md](docs/fork-delta.md)** — Complete upstream divergence tracking
- **[docs/hardening-note.md](docs/hardening-note.md)** — Execution and MCP trust boundary changes
- **[docs/release-checklist.md](docs/release-checklist.md)** — Quality gates for releases
- **[docs/label-taxonomy.md](docs/label-taxonomy.md)** — Issue/PR labeling system
- **[SECURITY.md](SECURITY.md)** — Responsible disclosure policy
- **[TODO.md](TODO.md)** — Prioritized backlog
- **[FEATURES.md](FEATURES.md)** — Feature inventory (inherited vs fork-specific)

---

## Contributing

Contributions are welcome, especially in these areas:

- **Security automation** — CodeQL, Dependabot, secret scanning workflows
- **DevSecOps agent rules** — AI guidance for secure development practices
- **Supply chain hardening** — Binary verification, signed releases, SBOM generation
- **Threat modeling** — Attack surface analysis and mitigation strategies
- **Documentation** — Security guides, deployment best practices

### How to Contribute

1. Review **[TODO.md](TODO.md)** for current priorities
2. Check **[docs/devsecops-fork-roadmap.md](docs/devsecops-fork-roadmap.md)** for context
3. Open an issue to discuss your approach
4. Submit a pull request with tests and documentation

### Contribution Guidelines

- **Security first** — No changes that weaken trust boundaries
- **Evidence over claims** — Document actual security improvements
- **Minimal diffs** — Prefer surgical changes over large refactors
- **Honest about limitations** — Don't overclaim capabilities

---

## Known Limitations

**Be aware of these current constraints**:

1. **Installer binary integrity** — No checksum or signature validation yet
2. **Proprietary runtime** — The \`pilot\` binary is closed-source
3. **Upstream dependencies** — Some artifacts still pulled from upstream
4. **External MCP endpoint** — \`grep-mcp\` calls out to third-party service
5. **Incomplete docs cleanup** — Some upstream content remains

These are documented in the roadmap and prioritized for future releases.

---

## Troubleshooting

### GitHub Actions Authentication Error

If you see this error in GitHub Actions:
```
Environment variable validation failed:
  - Either ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN is required
```

**Fix**: Configure the required API authentication. See **[docs/github-actions-setup.md](docs/github-actions-setup.md)** for detailed instructions.

**Quick fix:**
1. Navigate to repository Settings → Secrets and variables → Actions
2. Add a new secret named `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`
3. Get the token from the [Anthropic Console](https://console.anthropic.com/)
4. Re-run the failed workflow

---

## Upstream Attribution

This fork builds on **[maxritter/pilot-shell](https://github.com/maxritter/pilot-shell)**. Credit for the original workflow engine, agent architecture, and quality automation belongs to that project.

This fork's goal is not to replace the upstream positioning, but to evolve it toward a more security-conscious operating model for teams that prioritize trust boundaries and supply chain integrity.

---

## License

See **[LICENSE](LICENSE)** for details. This fork respects the upstream license terms.

---

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/canstralian/pilot-shell-devsecops/issues)
- **Discussions**: [GitHub Discussions](https://github.com/canstralian/pilot-shell-devsecops/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting

---

## Versioning

This fork uses **semantic versioning** with alpha/beta pre-releases:

- **0.x.0-alpha** — Early testing, incomplete features
- **0.x.0-beta** — Feature-complete, ready for validation
- **1.x.0** — Stable, production-ready

Current version: **0.1.0-alpha** (trust reset baseline)

---

## Roadmap

### v0.1.0-alpha (Current)
- ✅ Trust boundary reset (permissions, MCP, installer)
- ✅ Security documentation (roadmap, audit, hardening notes)
- ✅ Repository hygiene (templates, labels, TODO)

### v0.2.0 (Planned)
- 🔄 Installer binary integrity verification
- 🔄 Signed releases with GitHub attestations
- 🔄 CodeQL SAST workflow
- 🔄 Dependabot integration
- 🔄 DevSecOps agent rules

### v1.0.0 (Future)
- 📋 SLSA provenance chain
- 📋 Fork-native binary releases
- 📋 Complete documentation replacement
- 📋 Threat model document
- 📋 Policy-as-code framework

See **[TODO.md](TODO.md)** for the full roadmap.

---

<div align="center">

**Build with structure. Verify with rigor. Ship with evidence.**

</div>
