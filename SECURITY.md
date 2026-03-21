# Security Policy

## Reporting Security Vulnerabilities

We take security seriously in the Pilot Shell DevSecOps fork. If you discover a security vulnerability, we appreciate your responsible disclosure.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report security issues privately using one of these methods:

1. **GitHub Security Advisories** (Preferred):
   - Navigate to the [Security tab](https://github.com/canstralian/pilot-shell-devsecops/security/advisories)
   - Click "Report a vulnerability"
   - Fill out the advisory form with details

2. **Direct Contact**:
   - Email: [security contact to be added]
   - Subject line: `[SECURITY] Brief description of issue`

### What to Include

Please provide the following information in your report:

- **Description**: A clear description of the vulnerability
- **Impact**: What an attacker could do with this vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Components**: Which files, features, or dependencies are affected
- **Suggested Fix**: If you have a proposed fix or mitigation (optional)
- **Your Contact Info**: So we can follow up with you

### What to Expect

- **Acknowledgment**: We will acknowledge your report within 48 hours
- **Updates**: We will provide regular updates on our progress
- **Fix Timeline**: We aim to release fixes for critical vulnerabilities within 7 days
- **Credit**: With your permission, we will credit you in the release notes and CHANGELOG

### Scope

This security policy applies to:

- The Pilot Shell DevSecOps fork repository
- Official release artifacts
- Installation scripts
- Default configurations
- Bundled dependencies

### Out of Scope

The following are considered out of scope:

- Vulnerabilities in upstream dependencies (report to their maintainers)
- Issues in user-modified configurations
- Social engineering attacks
- Physical security issues

### Security Principles

This fork is being hardened with these security principles:

- **Explicit Trust Boundaries**: Permission prompts before dangerous operations
- **Minimal Ambient Trust**: Reduced default permissions
- **Pinned Dependencies**: Version-locked MCP servers and packages
- **Supply Chain Integrity**: Verified release artifacts (work in progress)
- **Transparent Operation**: Clear documentation of data flows

### Known Security Considerations

As documented in our [DevSecOps Fork Roadmap](docs/devsecops-fork-roadmap.md), we are actively working to address several trust boundaries:

- Installer binary integrity verification (planned)
- Signed releases (planned)
- SBOM generation (planned)
- External MCP server trust model (under review)

### Security Disclosure Process

1. **Report received**: Security team acknowledges receipt
2. **Initial assessment**: Team evaluates severity and impact
3. **Investigation**: Team investigates and develops fix
4. **Fix development**: Patch is developed and tested
5. **Private disclosure**: Fix is shared with reporter for validation
6. **Public disclosure**: Security advisory and fix are published
7. **Release**: Fixed version is released

### Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

As this fork matures, we will update this policy with long-term support commitments.

---

**Last Updated**: 2026-03-21

This security policy will be updated as the fork's security posture and processes evolve.
