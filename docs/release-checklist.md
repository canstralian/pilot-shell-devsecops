# Release Checklist — Pilot Shell DevSecOps Fork

> **Purpose**: Comprehensive quality gates and verification steps for releasing new versions.
> **Audience**: Release managers, maintainers, and contributors preparing releases.

---

## Release Philosophy

This fork prioritizes **provenance over speed** and **evidence over claims**. Every release should be:

- **Reproducible** — Built from tagged source with deterministic dependencies
- **Verifiable** — Signed, checksummed, and attestable
- **Documented** — Changelog, known issues, and upgrade path clearly stated
- **Secure** — Vetted for vulnerabilities and supply chain risks
- **Honest** — No false security claims; limitations are disclosed

---

## Release Types

| Type | Version Format | When to Use | Quality Bar |
|------|----------------|-------------|-------------|
| **Alpha** | `v0.x.0-alpha` | Early testing, incomplete features | Functional but unstable |
| **Beta** | `v0.x.0-beta` | Feature-complete, needs validation | Stable, ready for testing |
| **Stable** | `v1.x.0` | Production-ready release | Full quality gates |
| **Patch** | `v1.x.1` | Bug fixes, security patches | Regression testing required |

---

## Pre-Release Checklist

### 1. Code Quality

**Requirement**: All planned work is complete and tested.

- [ ] All issues tagged for this milestone are closed or deferred
- [ ] All planned features are implemented and merged to main branch
- [ ] All automated tests pass in CI
- [ ] Manual testing completed for critical workflows
- [ ] Code review is complete for all changes since last release
- [ ] Linters pass without warnings (`ruff`, `prettier`, `shellcheck`, etc.)
- [ ] Type checking passes (if applicable)
- [ ] No known regressions from previous version

**Validation command**:
```bash
# Run all quality checks locally before release
./scripts/quality-check.sh  # If available
```

---

### 2. Security Verification

**Requirement**: No known vulnerabilities or unmitigated risks.

- [ ] Security audit completed (required for stable releases)
- [ ] All high-severity vulnerabilities addressed or documented
- [ ] Dependency versions reviewed for known CVEs
  - `npm audit` passes (or exceptions documented)
  - `pip-audit` passes (or exceptions documented)
- [ ] Secret scanning passes (no leaked credentials or keys)
- [ ] SAST/CodeQL checks pass (if workflow exists)
- [ ] MCP server versions pinned and vetted
- [ ] External dependencies reviewed for supply chain risks

**Validation commands**:
```bash
# Check for dependency vulnerabilities
npm audit --production
uv pip list --outdated

# Check for secrets (if pre-commit hook exists)
pre-commit run detect-secrets --all-files
```

**Security exception process**:
- Document in `SECURITY.md` or release notes
- Create follow-up issue for resolution
- Tag with `risk:medium` or `risk:high` as appropriate

---

### 3. Documentation

**Requirement**: All user-facing changes are documented.

- [ ] `CHANGELOG.md` updated with all changes since last release
  - Breaking changes clearly marked with `⚠️ BREAKING`
  - Security fixes marked with `🔒 SECURITY`
  - Grouped by type: Added, Changed, Fixed, Removed
- [ ] `README.md` accurately reflects current capabilities
  - Installation instructions up to date
  - Feature list current
  - No stale references to unimplemented features
- [ ] All new features documented in relevant docs
- [ ] Breaking changes have migration guide
- [ ] `TODO.md` and `FEATURES.md` updated
- [ ] `docs/fork-delta.md` updated with any upstream divergence
- [ ] API changes documented (if applicable)

**Templates**:
- See `docs/release-notes-template.md` for release notes structure
- See `CHANGELOG.md` for entry format examples

---

### 4. Supply Chain & Provenance

**Requirement**: Artifacts are traceable and integrity-verifiable.

- [ ] `install.sh` `REPO` variable points to `canstralian/pilot-shell-devsecops`
- [ ] Release artifacts built from tagged commit (not `main` branch tip)
- [ ] Build is reproducible (can be rebuilt from source with same output)
- [ ] SBOM generated for release (when tooling available)
- [ ] Release artifacts signed with GPG key (when available)
- [ ] SHA-256 checksums generated for all release assets
- [ ] Provenance attestations created (GitHub Actions, SLSA)
- [ ] No upstream release artifacts misrepresented as fork-native

**Checksum generation**:
```bash
# Generate SHA-256 checksums for release artifacts
cd release-artifacts/
sha256sum * > SHA256SUMS.txt
gpg --clearsign SHA256SUMS.txt  # If GPG signing is set up
```

**Known limitations** (as of 2026-03-21):
- Installer binary still downloaded from GitHub without checksum validation
- GPG signing not yet implemented
- SLSA provenance not yet implemented

---

### 5. Installation & Compatibility

**Requirement**: Installation works on all supported platforms.

- [ ] Install script tested on **Linux** (Ubuntu 24.04 or equivalent)
- [ ] Install script tested on **macOS** (latest stable)
- [ ] Install script tested on **WSL2** (if applicable)
- [ ] Upgrade path tested from previous version
  - Settings preserved
  - MCP config preserved
  - No data loss
- [ ] Clean install tested (no previous version installed)
- [ ] Uninstall script tested (leaves system clean)
- [ ] MCP server compatibility verified (all servers load correctly)
- [ ] Shell integration tested (bash, zsh, fish)

**Test matrix**:

| Platform | Clean Install | Upgrade | Uninstall |
|----------|---------------|---------|-----------|
| Ubuntu 24.04 | ☐ | ☐ | ☐ |
| macOS 14.x | ☐ | ☐ | ☐ |
| WSL2 Ubuntu | ☐ | ☐ | ☐ |

---

### 6. Release Notes

**Requirement**: Clear, honest communication about what's in the release.

- [ ] Release notes drafted using `docs/release-notes-template.md`
- [ ] Summary section highlights major changes
- [ ] "Included" section lists all features and fixes
- [ ] "Not Yet Included" section is honest about unfinished work
- [ ] "Known Limitations" section documents current constraints
- [ ] Upgrade instructions provided (if needed)
- [ ] Breaking changes clearly marked
- [ ] Security improvements highlighted
- [ ] Contributors credited (with permission)

**Tone guidelines**:
- Factual, not marketing language
- No unproven security claims
- Honest about limitations
- Clear upgrade path

---

## Release Process

### Step 1: Create Release Branch

For stable releases, create a release branch:

```bash
git checkout -b release/v1.0.0
git push origin release/v1.0.0
```

For alpha/beta, release directly from `main` (or `develop` if using gitflow).

---

### Step 2: Update Version Metadata

Update version strings in:

- `pyproject.toml` (if applicable)
- `package.json` files (if applicable)
- `pilot/plugin.json` (if applicable)
- Any other version references

```bash
# Example version bump
sed -i 's/version = "0.0.1"/version = "0.1.0"/' pyproject.toml
```

---

### Step 3: Update Documentation

- [ ] Finalize `CHANGELOG.md` for this version
- [ ] Update `README.md` version references
- [ ] Update `TODO.md` to move completed items to "Done"
- [ ] Review and update `FEATURES.md` if needed

Commit these changes:

```bash
git add CHANGELOG.md README.md TODO.md
git commit -m "docs: prepare for v0.1.0-alpha release"
git push origin release/v0.1.0-alpha
```

---

### Step 4: Create Git Tag

Create an **annotated and signed tag**:

```bash
# Annotated tag (minimum)
git tag -a v0.1.0-alpha -m "Release v0.1.0-alpha — Trust reset"

# Signed tag (preferred when GPG is set up)
git tag -s v0.1.0-alpha -m "Release v0.1.0-alpha — Trust reset"

# Push tag
git push origin v0.1.0-alpha
```

**Tag naming convention**:
- Stable: `v1.0.0`
- Alpha: `v0.1.0-alpha`
- Beta: `v0.1.0-beta`
- Patch: `v1.0.1`

---

### Step 5: Build Release Artifacts

If the fork publishes custom binaries or packages:

```bash
# Build artifacts
./scripts/build-release.sh v0.1.0-alpha

# Generate checksums
cd dist/
sha256sum * > SHA256SUMS.txt

# Sign checksums (if GPG available)
gpg --clearsign SHA256SUMS.txt
```

**Current state** (2026-03-21):
- No fork-native binary build yet
- Installer pulls from upstream or fork release tags
- Document this dependency clearly in release notes

---

### Step 6: Create GitHub Release (Draft)

1. Go to **Releases → Draft a new release**
2. **Choose tag**: Select `v0.1.0-alpha`
3. **Release title**: `v0.1.0-alpha — Trust Reset` (or appropriate title)
4. **Description**: Paste release notes from `docs/release-notes-template.md`
5. **Upload assets**:
   - Installer script (`install.sh`)
   - Checksums (`SHA256SUMS.txt`, `SHA256SUMS.txt.asc`)
   - Any binaries (when available)
6. **Mark as pre-release** if alpha/beta
7. **Save as draft** (do not publish yet)

---

### Step 7: Verification & Smoke Testing

Before publishing, verify the draft release:

- [ ] Download release assets from draft
- [ ] Verify checksums match:
  ```bash
  sha256sum -c SHA256SUMS.txt
  ```
- [ ] Test installation using release artifacts:
  ```bash
  curl -fsSL https://github.com/canstralian/pilot-shell-devsecops/releases/download/v0.1.0-alpha/install.sh | bash
  ```
- [ ] Smoke test critical workflows:
  - `pilot --version` shows correct version
  - MCP servers load correctly
  - Basic CLI commands work
  - Permission prompts appear (not bypassed)

**Rollback plan if issues found**:
- Do not publish release
- Fix issues on release branch
- Create new tag (e.g., `v0.1.0-alpha.1`)
- Rebuild artifacts and re-verify

---

### Step 8: Publish Release

Once verification passes:

1. Go to the draft release
2. Review all fields one more time
3. **Publish release**
4. Verify release appears in repository

---

## Post-Release

### Immediate (Within 24 hours)

- [ ] Monitor issue tracker for regression reports
- [ ] Watch for installation failures in different environments
- [ ] Respond to user questions or confusion about release
- [ ] Update fork-delta.md if any upstream references changed
- [ ] Close release milestone in GitHub

### Short-Term (Within 1 week)

- [ ] Create follow-up issues for deferred work
- [ ] Update roadmap if priorities shifted
- [ ] Archive or close release checklist issue
- [ ] Merge release branch back to main (if using release branches)
- [ ] Tag contributors in release notes (if not done already)

### Medium-Term (Within 1 month)

- [ ] Review release process for improvements
- [ ] Update this checklist document with lessons learned
- [ ] Plan next release based on feedback

---

## Rollback & Hotfix Process

### If Critical Issue Discovered Post-Release

1. **Assess severity**:
   - Security vulnerability: Immediate action required
   - Breaking bug: Hotfix within 24-48 hours
   - Minor issue: Fix in next regular release

2. **Communicate**:
   - Mark GitHub release as "pre-release" if stable
   - Add prominent warning to release notes
   - Create GitHub issue describing the problem
   - Post announcement if users are affected

3. **Hotfix process** (for critical issues):
   ```bash
   # Create hotfix branch from release tag
   git checkout -b hotfix/v0.1.1 v0.1.0-alpha

   # Fix the issue
   git commit -m "fix: critical issue description"

   # Create new patch release
   git tag -s v0.1.1 -m "Hotfix: critical issue description"
   git push origin v0.1.1
   ```

4. **Release hotfix**:
   - Follow abbreviated release process
   - Highlight fix in release notes
   - Reference original issue in changelog

---

## Security-Specific Release Notes

For releases containing security fixes:

- **Embargo period**: Do not disclose details until users have time to upgrade
- **CVE assignment**: Request CVE if applicable
- **Credit researchers**: With permission, credit vulnerability reporters
- **Upgrade urgency**: Clearly state upgrade priority (immediate, recommended, optional)

Example release note for security fix:

```markdown
## 🔒 Security Fixes

- **[HIGH]** Fixed command injection vulnerability in installer script (CVE-2026-XXXXX)
  - **Impact**: Malicious actors could execute arbitrary code during installation
  - **Mitigation**: Upgrade to v0.1.1 immediately
  - **Credit**: Thanks to @security-researcher for responsible disclosure
```

---

## Release Metrics (Future)

Track these metrics to improve release quality over time:

- Time from tag to published release
- Number of issues found in verification
- Installation success rate across platforms
- Number of regressions reported post-release
- Time to hotfix (for critical issues)

---

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Release Best Practices](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [SLSA Framework](https://slsa.dev/)

---

**Last Updated**: 2026-03-21
