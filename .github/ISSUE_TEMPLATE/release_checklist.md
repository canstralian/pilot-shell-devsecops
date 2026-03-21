---
name: Release Checklist
about: Track pre-release verification and quality gates for a new version
labels: type:release, status:ready
---

## Release Information

- **Version**: <!-- e.g., v0.1.0-alpha -->
- **Target Date**: <!-- YYYY-MM-DD -->
- **Release Type**: <!-- alpha / beta / stable / patch -->
- **Release Manager**: <!-- @username -->

---

## Pre-Release Checklist

### Code Quality

- [ ] All planned features are implemented and merged
- [ ] All tests pass in CI
- [ ] Code review is complete for all changes
- [ ] Linters and formatters pass without errors
- [ ] No unresolved critical or high-severity issues

### Security Verification

- [ ] Security audit completed (if required for this release)
- [ ] All known vulnerabilities are addressed or documented
- [ ] Dependency versions reviewed for known CVEs
- [ ] Secret scanning passes (no leaked credentials)
- [ ] SAST/CodeQL checks pass (if enabled)

### Documentation

- [ ] `CHANGELOG.md` updated with all changes since last release
- [ ] `README.md` accurately reflects current capabilities
- [ ] All new features are documented
- [ ] Breaking changes are clearly noted
- [ ] Migration guide provided (if needed)
- [ ] `TODO.md` and `FEATURES.md` updated

### Supply Chain & Provenance

- [ ] Installer script `REPO` variable points to correct fork
- [ ] Release artifacts are built from tagged commit
- [ ] SBOM generated (if applicable)
- [ ] Release artifacts signed (if applicable)
- [ ] Checksums generated for all release assets
- [ ] Provenance attestations created (if applicable)

### Installation & Compatibility

- [ ] Install script tested on Linux
- [ ] Install script tested on macOS
- [ ] Install script tested on WSL2 (if applicable)
- [ ] Upgrade path tested from previous version
- [ ] Clean install tested
- [ ] MCP server compatibility verified

### Release Notes

- [ ] Release notes drafted (see `docs/release-notes-template.md`)
- [ ] Known issues and limitations documented
- [ ] Upgrade instructions provided
- [ ] Contributors credited
- [ ] Security improvements highlighted

---

## Release Process

### 1. Create Release Tag

- [ ] Tag created: `git tag -s vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Tag pushed: `git push origin vX.Y.Z`

### 2. Build & Upload Artifacts

- [ ] Release artifacts built
- [ ] Checksums generated
- [ ] Artifacts uploaded to GitHub release
- [ ] Release marked as draft initially

### 3. Verification

- [ ] Download and verify checksums
- [ ] Test installation from release artifacts
- [ ] Smoke test critical workflows

### 4. Publication

- [ ] Release notes finalized
- [ ] GitHub release published (remove draft status)
- [ ] Announcement prepared (if applicable)
- [ ] Documentation site updated (if applicable)

---

## Post-Release

- [ ] Monitor issue tracker for regression reports
- [ ] Update fork-delta.md if needed
- [ ] Create follow-up issues for any deferred work
- [ ] Archive release checklist issue

---

## Rollback Plan

**If critical issues are discovered post-release:**

1. Mark release as "pre-release" in GitHub
2. Add warning to release notes
3. Create hotfix branch if needed
4. Document issue and resolution timeline
5. Prepare patch release

---

## References

- [DevSecOps Fork Roadmap](../docs/devsecops-fork-roadmap.md)
- [Release Checklist Documentation](../docs/release-checklist.md)
- [Security Policy](../SECURITY.md)
- [Changelog](../CHANGELOG.md)

---

## Notes

<!-- Additional context, risks, or special considerations for this release -->
