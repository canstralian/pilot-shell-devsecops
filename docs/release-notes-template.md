# Release Notes Template — v0.1.0-alpha

> **Template for first fork release**: Use this as the base for `v0.1.0-alpha` release notes.
> Modify as needed, but maintain the structure and honest tone.

---

## v0.1.0-alpha — Trust Reset

**Release Date**: [YYYY-MM-DD]

This is the first opinionated release of the **Pilot Shell DevSecOps fork**, establishing a safer default security posture and clearer fork identity.

---

## 🎯 Release Goal

This alpha release resets trust boundaries and default permissions to align with DevSecOps principles. It prioritizes **explicit approval over convenience** and **evidence-based security over marketing claims**.

---

## ✅ What's Included

### Trust Boundary Hardening

- **Safer default execution posture**:
  - Changed `permissions.defaultMode` from `"bypassPermissions"` to `"default"`
  - Enabled permission prompts for dangerous operations (`skipDangerousModePermissionPrompt = false`)
  - Disabled automatic loading of all project MCP servers (`enableAllProjectMcpServers = false`)
- **Pinned MCP server versions**:
  - `context7`: `@upstash/context7-mcp@2.1.4`
  - `web-search`: `open-websearch@1.2.7`
  - `web-fetch`: `fetcher-mcp@0.3.9`
- **Fork installer provenance**:
  - `install.sh` now points to `canstralian/pilot-shell-devsecops`
  - Removed upstream advertising from settings

### Documentation & Planning

- **Security policy**: Added `SECURITY.md` with responsible disclosure process
- **Comprehensive roadmap**: Created `docs/devsecops-fork-roadmap.md` with audit findings and prioritized next steps
- **Fork divergence tracking**: Created `docs/fork-delta.md` documenting all differences from upstream
- **Hardening notes**: Created `docs/hardening-note.md` explaining trust boundary changes
- **Feature inventory**: Created `FEATURES.md` distinguishing inherited vs fork-specific features
- **Work tracking**: Created `TODO.md` with prioritized backlog

### Repository Hygiene

- **Issue templates**:
  - Security issue template (`.github/ISSUE_TEMPLATE/security_issue.yml`)
  - Hardening task template
  - Release checklist template
  - Bug report and feature request templates
- **Label taxonomy**: Created `docs/label-taxonomy.md` with standardized labeling system
- **Release documentation**: Created `docs/release-checklist.md` with comprehensive quality gates

---

## ⏳ What's Not Yet Included

This is an **alpha release**. The following are planned but not yet implemented:

### Supply Chain Security

- ❌ Installer binary integrity verification (SHA-256 + GPG signatures)
- ❌ Signed release artifacts
- ❌ SBOM generation
- ❌ SLSA provenance attestations
- ❌ Fork-native binary releases

### DevSecOps Automation

- ❌ CodeQL SAST workflow
- ❌ Dependabot configuration
- ❌ Dependency review workflow
- ❌ Automated secret scanning
- ❌ Pre-commit security hooks

### Agent Security Rules

- ❌ `pilot/rules/devsecops.md` — Security-focused AI agent behavior
- ❌ Threat model document (`docs/threat-model.md`)
- ❌ Secrets handling rules

### Documentation Cleanup

- ❌ Replace upstream Docusaurus documentation
- ❌ Update plugin.json fork metadata (pending legal review)
- ❌ Clean up inherited upstream changelog

---

## ⚠️ Known Limitations

Be aware of these current constraints:

### Supply Chain Dependencies

- **Installer binary**: Still pulled from GitHub without checksum validation
- **Proprietary runtime**: The `pilot` binary is closed-source and cannot be independently audited
- **Upstream artifacts**: Some release artifacts may still depend on upstream infrastructure

### Remaining Trust Surfaces

- **External MCP endpoint**: `grep-mcp` points to `https://mcp.grep.app` (third-party HTTP service)
- **`DISABLE_INSTALLATION_CHECKS`**: Set to `true` in default settings for CI compatibility
- **`npx -y` flag**: Auto-installs without confirmation, even with pinned versions

### Incomplete Fork Identity

- **Docusaurus docs**: Still contain upstream product copy
- **Plugin metadata**: Still references upstream author (requires legal review)
- **Changelog**: Reflects upstream history

---

## 🔧 Upgrade Instructions

### From Upstream `maxritter/pilot-shell`

1. **Back up your settings**:
   ```bash
   cp ~/.claude/pilot/settings.json ~/.claude/pilot/settings.json.backup
   ```

2. **Install the fork**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/canstralian/pilot-shell-devsecops/v0.1.0-alpha/install.sh | bash
   ```

3. **Review permission changes**:
   - You will now see permission prompts for dangerous operations
   - MCP servers require explicit enablement per session
   - Review and adjust settings in `~/.claude/pilot/settings.json` if needed

### From Previous Fork Versions

This is the first fork release. No previous versions exist.

---

## 🔒 Security Improvements

This release addresses several high-impact trust boundaries:

1. **Removed silent permission bypass** — Every dangerous operation now requires user approval
2. **Removed auto-trust for MCP servers** — MCP servers must be explicitly enabled
3. **Pinned runtime dependencies** — MCP packages are version-locked for reproducibility
4. **Clarified installer provenance** — Installation points to fork repository

### What's Still Needed

- Installer binary integrity verification (planned for v0.2.0)
- Signed releases (planned for v0.2.0)
- External MCP endpoint review (in progress)

---

## 📋 Migration Impact

### Breaking Changes

- **Permission prompts**: Operations that previously ran without confirmation now require approval
  - **Mitigation**: Review prompts and approve explicitly, or adjust settings per your risk tolerance
- **MCP servers**: Project `.mcp.json` servers are no longer auto-loaded
  - **Mitigation**: Enable MCP servers explicitly via settings or per-session flags

### Non-Breaking Changes

- All core workflows (spec-driven development, quick mode, verification loops) remain unchanged
- Existing rules, commands, and skills continue to work
- Shell integration and console remain functional

---

## 🙏 Contributors

Thanks to everyone who contributed to this release:

- [Contributor names to be added]

Special thanks to the upstream `maxritter/pilot-shell` project for the foundational workflow engine.

---

## 📚 Documentation

- [DevSecOps Fork Roadmap](docs/devsecops-fork-roadmap.md)
- [Fork Delta (Upstream Divergence)](docs/fork-delta.md)
- [Hardening Note](docs/hardening-note.md)
- [Security Policy](SECURITY.md)
- [Features](FEATURES.md)
- [TODO](TODO.md)

---

## 🐛 Known Issues

No known critical issues at release time. Please report any problems via [GitHub Issues](https://github.com/canstralian/pilot-shell-devsecops/issues).

---

## 🔮 What's Next

Planned for v0.2.0 (tentative):

- Installer binary integrity verification
- Signed releases with GitHub attestations
- CodeQL SAST workflow
- Dependabot integration
- DevSecOps agent rules (`pilot/rules/devsecops.md`)
- Initial threat model document

See [TODO.md](TODO.md) for the full roadmap.

---

## 📦 Release Assets

- `install.sh` — Fork installer script
- `SHA256SUMS.txt` — Checksums for release artifacts (when available)

**Note**: This alpha release does not yet include fork-native binary artifacts. The installer pulls binaries from GitHub releases.

---

## 🔗 Links

- **Repository**: https://github.com/canstralian/pilot-shell-devsecops
- **Issues**: https://github.com/canstralian/pilot-shell-devsecops/issues
- **Discussions**: https://github.com/canstralian/pilot-shell-devsecops/discussions
- **Upstream**: https://github.com/maxritter/pilot-shell

---

## ⚖️ License

See [LICENSE](LICENSE) for details. This fork builds on the upstream `maxritter/pilot-shell` project and respects its licensing terms.

---

**Build with structure. Verify with rigor. Ship with evidence.**
