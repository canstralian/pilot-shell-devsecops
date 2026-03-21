# FEATURES — Pilot Shell DevSecOps Fork

> **Status**: Living inventory of inherited, retained, fork-specific, and removed features.
> **Purpose**: Track feature evolution relative to upstream `maxritter/pilot-shell`.

---

## Inherited Upstream Features (Retained)

These features are inherited from the upstream Pilot Shell project and remain active in the fork:

### Core Workflow

- **Spec-driven development** — `/spec` command for structured planning, implementation, and verification
- **Quick Mode** — Conversational mode for small changes and exploration
- **Plan approval workflow** — User review and approval before implementation
- **Verification loops** — Automatic code review and test validation before completion
- **Worktree isolation** — Optional git worktree-based isolation for `/spec` tasks

### Agent Architecture

- **Multi-agent system** — Specialized agents for planning, implementation, and verification
- **Smart model routing** — Opus for planning/verification, Sonnet for implementation
- **Plan verifier** — Independent code review against plans before completion
- **Quality hooks** — Automatic linting, formatting, and type-checking on edits
- **TDD enforcer** — Warnings when code changes without failing tests first

### Memory & Context

- **Pilot Memory** — Persistent memory across sessions
- **Auto-compaction** — Seamless context preservation during summarization
- **Context monitoring** — Real-time usage tracking and automatic compaction

### MCP Integration

- **MCP server support** — Model Context Protocol server integration
- **Project-scoped MCP** — Per-project `.mcp.json` configuration
- **Bundled MCP servers**:
  - `context7` — Up-to-date library documentation fetching
  - `codebase-memory-mcp` — Code knowledge graph and call tracing
  - `web-search` — DuckDuckGo/Bing/Exa web search integration
  - `web-fetch` — Web page content fetching
  - `grep-mcp` — GitHub public repository code search

### IDE & Tooling

- **LSP integration** — Language Server Protocol support (Python, TypeScript, Go)
- **Real-time diagnostics** — IDE-integrated error and warning feedback
- **Probe** — Semantic code search by meaning
- **RTK** — Token-optimized CLI proxy (60-90% token savings)
- **Playwright CLI** — Headless browser automation and testing

### Console & Interface

- **Pilot Shell Console** — Web UI at `localhost:41777`
- **Session browser** — Browse memory, sessions, and specs
- **Share Dashboard** — Sync skills across machines and teams
- **Custom status line** — Configurable status bar integration
- **Command history** — Ctrl+R search, persistent history

### Extensibility

- **Custom rules** — `.claude/rules/` for project-specific guidance
- **Custom commands** — `.claude/commands/` for slash commands
- **Custom skills** — `.claude/skills/` for reusable agent capabilities
- **Conditional rules** — File-type-specific rule activation
- **Rule generation** — `/setup-rules` discovers codebase patterns

### Developer Experience

- **Shell integration** — `pilot` and `ccp` commands in bash/zsh/fish
- **Multi-platform** — macOS, Linux, WSL2 support
- **Auto-updates** — Automatic version updates on launch
- **No API keys** — Web search and scraping work without configuration
- **JSON output** — `--json` flag for structured CLI responses

---

## Fork-Specific Features (Implemented)

These features have been added or modified specifically for the DevSecOps fork:

### Trust & Security Boundaries

- **Safer default execution posture**:
  - `permissions.defaultMode = "default"` (upstream: `"bypassPermissions"`)
  - `skipDangerousModePermissionPrompt = false` (upstream: `true`)
  - `enableAllProjectMcpServers = false` (upstream: `true`)
- **Pinned MCP server versions** — Explicit version locking for `npx`-invoked servers
- **Hardening documentation**:
  - `docs/devsecops-fork-roadmap.md` — Security audit and prioritized roadmap
  - `docs/fork-delta.md` — Complete upstream divergence tracking
  - `docs/hardening-note.md` — Execution and MCP trust boundary changes
  - `SECURITY.md` — Responsible disclosure policy
  - `TODO.md` — Prioritized feature and security work tracking
  - `FEATURES.md` (this file) — Feature inventory

### Repository Hygiene

- **Fork identity**:
  - `install.sh` REPO variable points to `canstralian/pilot-shell-devsecops`
  - Temporary README clearly positions repo as DevSecOps fork
  - Upstream advertising removed from settings
- **Issue templates**:
  - Security issue template (`.github/ISSUE_TEMPLATE/security_issue.yml`)
  - Bug report and feature request templates

---

## Fork-Specific Features (Planned)

These features are planned for future implementation in the DevSecOps fork:

### Supply Chain Security

- **Installer binary integrity verification** — SHA-256 + GPG signature validation
- **Signed releases** — GitHub attestations and cryptographic provenance
- **SBOM generation** — Software Bill of Materials for all releases
- **SLSA provenance** — Level 2+ build provenance chain
- **Fork-native release pipeline** — Independent from upstream artifacts

### DevSecOps Automation

- **CodeQL SAST workflow** — Automated vulnerability detection in CI
- **Dependabot integration** — Automated dependency updates
- **Dependency review workflow** — Block known-vulnerable dependencies in PRs
- **Secret scanning** — Pre-commit and CI-based secret detection
- **Security policy enforcement** — Automated security check framework

### Agent Security Rules

- **`pilot/rules/devsecops.md`** — Security-focused agent behavior rules
- **Threat model guidance** — AI agent instructions for threat modeling
- **Secrets handling rules** — Safe credential and secret management
- **Supply chain rules** — Dependency vetting and verification guidance

### Governance & Documentation

- **Threat model document** — `docs/threat-model.md` with attack surface analysis
- **Security incident playbook** — Response procedures for vulnerabilities
- **Compliance documentation** — CIS benchmarks, security baselines
- **Label taxonomy** — Structured issue/PR labeling system
- **Release checklist** — Provenance, integrity, and quality gates

### Advanced Security

- **Policy-as-code** — OPA or equivalent for machine-verifiable policies
- **Fine-grained MCP permissions** — Per-server trust boundaries
- **MCP server sandboxing** — Runtime isolation for MCP servers
- **Auditable runtime** — Open-source replacement for proprietary binary (long-term)

---

## Removed or Intentionally Unsupported Features

These upstream features have been removed or are not supported in the fork:

### Removed

- **Automatic permission bypass** — Upstream `bypassPermissions` default removed
- **Silent dangerous mode** — Upstream `skipDangerousModePermissionPrompt: true` removed
- **Auto-load all MCP servers** — Upstream `enableAllProjectMcpServers: true` removed
- **Upstream advertising** — Star-the-repo tips removed from settings
- **Unpinned MCP versions** — `npx -y` without version locking removed

### Intentionally Unsupported (Pending Review)

- **External HTTP MCP endpoints** — `grep-mcp` HTTP server under trust review
- **Unverified installation binaries** — No checksum validation (to be added)
- **Proprietary runtime binary** — Closed-source `pilot` binary (long-term replacement planned)

---

## Feature Comparison Matrix

| Feature | Upstream | Fork | Notes |
|---------|----------|------|-------|
| Permission prompts | Bypassed by default | Enabled by default | Fork prioritizes explicit approval |
| MCP server loading | Auto-load all | Explicit opt-in | Fork requires per-session MCP enablement |
| MCP version pinning | Unpinned `npx -y` | Pinned versions | Fork ensures deterministic dependencies |
| Security documentation | Limited | Comprehensive | Fork includes threat model, security policy |
| Installation integrity | No verification | Planned | Fork will add checksum/signature validation |
| Release signing | None | Planned | Fork will add GitHub attestations |
| DevSecOps rules | Not present | Planned | Fork-specific AI agent security guidance |
| Spec workflow | Full support | Full support | Retained from upstream |
| Quality hooks | Full support | Full support | Retained from upstream |
| MCP integration | Full support | Full support | Retained with hardened defaults |

---

## Temporary Upstream Dependencies

These features currently depend on upstream `maxritter/pilot-shell` infrastructure:

- **Installer binary artifacts** — Downloaded from upstream GitHub releases
- **Pilot runtime binary** — Proprietary `.so` binary from upstream
- **Docusaurus documentation** — Upstream docs content still present

These dependencies are temporary and documented in `docs/fork-delta.md`. The roadmap includes establishing fork-native artifact pipelines.

---

## Contribution Priorities

High-value feature development areas:

1. **Security automation** — CodeQL, Dependabot, dependency review workflows
2. **DevSecOps agent rules** — AI guidance for secure development
3. **Supply chain integrity** — Binary verification, signed releases, SBOM
4. **MCP security model** — Fine-grained trust boundaries, sandboxing
5. **Threat modeling** — Attack surface documentation and mitigation
6. **Documentation cleanup** — Replace upstream content with fork-specific docs

---

## Version History

| Fork Version | Major Features Added |
|--------------|---------------------|
| 0.1.0-alpha (planned) | Trust reset: safer defaults, pinned MCP versions, fork identity |
| Future | Supply chain integrity, DevSecOps automation, security rules |

---

**Last Updated**: 2026-03-21
