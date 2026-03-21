# Label Taxonomy — Pilot Shell DevSecOps Fork

> **Purpose**: Standardized labeling system for issues and pull requests.
> **Usage**: Apply labels consistently to enable filtering, prioritization, and triage.

---

## How to Apply Labels in GitHub

To apply these labels in your repository:

1. Navigate to **Settings → Labels** in your GitHub repository
2. Delete or archive any unused default labels
3. Create each label below with the exact name and color hex code
4. Use the description field to add context for each label

Or use the GitHub CLI:

```bash
# Example: Create a priority label
gh label create "priority:P0" --color "B60205" --description "Critical — ship blocker"
```

---

## Priority Labels

Indicate urgency and implementation order. **Every issue should have exactly one priority label.**

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `priority:P0` | `#B60205` | Critical — ship blocker | Security vulnerabilities, installer breakage, data loss risks |
| `priority:P1` | `#D93F0B` | High — should do immediately | High-impact security improvements, core functionality gaps |
| `priority:P2` | `#FBCA04` | Medium — schedule within release cycle | Important improvements, non-critical bugs |
| `priority:P3` | `#0E8A16` | Low — backlog | Nice-to-have enhancements, minor issues |

---

## Type Labels

Categorize the nature of the work. **Every issue should have exactly one type label.**

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `type:bug` | `#D73A4A` | Bug or defect | Incorrect behavior, crashes, unexpected errors |
| `type:feature` | `#A2EEEF` | New feature or capability | New functionality, user-facing improvements |
| `type:security` | `#5319E7` | Security vulnerability or issue | CVEs, security flaws, trust boundary issues |
| `type:hardening` | `#6F42C1` | Security hardening or trust improvement | Safer defaults, permission tightening, supply chain work |
| `type:docs` | `#0075CA` | Documentation update | README, guides, API docs, comments |
| `type:process` | `#C2E0C6` | Process or governance | Issue templates, workflows, contribution guidelines |
| `type:release` | `#1D76DB` | Release preparation or coordination | Release checklists, versioning, changelog updates |

---

## Area Labels

Indicate which part of the codebase or system is affected. **Issues may have multiple area labels.**

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `area:installer` | `#F9D0C4` | Installation script and bootstrap | `install.sh`, `uninstall.sh`, bootstrap logic |
| `area:settings` | `#FAD8C7` | Settings and configuration | `pilot/settings.json`, default configs |
| `area:mcp` | `#E4E669` | MCP servers and integration | `.mcp.json`, MCP trust boundaries |
| `area:verification` | `#BFDADC` | Testing and verification workflows | CI/CD, SAST, dependency scanning |
| `area:hooks` | `#BFD4F2` | Git hooks and quality automation | Pre-commit, quality hooks, linters |
| `area:github` | `#D4C5F9` | GitHub-specific features | Actions, issue templates, labels |
| `area:docs` | `#C5DEF5` | Documentation files and sites | `docs/`, `README.md`, Docusaurus |
| `area:branding` | `#F9D0C4` | Fork identity and attribution | Upstream references, fork positioning |
| `area:readme` | `#C5DEF5` | README.md specifically | Main repository landing page |
| `area:roadmap` | `#C5DEF5` | Planning and roadmap docs | Roadmap, TODO, fork-delta |

---

## Status Labels

Track workflow state. **Apply status labels as work progresses.**

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `status:blocked` | `#000000` | Blocked by external dependency | Waiting on upstream, legal review, infrastructure |
| `status:ready` | `#0E8A16` | Ready to implement | Issue is triaged, scoped, and unblocked |
| `status:in-progress` | `#FBCA04` | Work in progress | Someone is actively working on this |
| `status:needs-audit` | `#BFD4F2` | Requires security or compliance review | Changes need security team sign-off |
| `needs-triage` | `#EDEDED` | Needs initial review and labeling | New issues that haven't been categorized yet |

---

## Risk Labels

Indicate security or operational risk level. **Use for security-related issues only.**

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `risk:high` | `#B60205` | High risk — critical security impact | Remote code execution, auth bypass, data exposure |
| `risk:medium` | `#D93F0B` | Medium risk — significant but contained | CSRF, XSS, supply chain gaps |
| `risk:low` | `#0E8A16` | Low risk — minor or theoretical | Information disclosure, low-impact DoS |

---

## Special Labels

Additional context labels for specific workflows.

| Label | Color | Description | When to Use |
|-------|-------|-------------|-------------|
| `good-first-issue` | `#7057FF` | Suitable for new contributors | Well-scoped, documented, low complexity |
| `help-wanted` | `#008672` | Community contributions welcome | Maintainers don't have bandwidth, community can help |
| `duplicate` | `#CFD3D7` | Duplicate of another issue | Link to the original issue and close |
| `wontfix` | `#FFFFFF` | Will not be implemented | Out of scope, intentionally unsupported |
| `upstream` | `#E99695` | Should be fixed in upstream project | Issue belongs to `maxritter/pilot-shell` |
| `breaking-change` | `#B60205` | Introduces breaking changes | Requires migration guide or major version bump |

---

## Label Combination Guidelines

### Every Issue Should Have

1. **One priority label** (`priority:P0` through `priority:P3`)
2. **One type label** (`type:bug`, `type:feature`, etc.)
3. **At least one area label** (`area:installer`, `area:settings`, etc.)
4. **Status labels as needed** (`status:blocked`, `status:ready`, etc.)

### Security Issues

Security-related issues should have:

- `type:security` or `type:hardening`
- One `risk:*` label
- Relevant `area:*` labels
- `status:needs-audit` if review is required

### Examples

**Critical security vulnerability in installer:**
- `priority:P0`
- `type:security`
- `area:installer`
- `risk:high`

**Add CodeQL workflow:**
- `priority:P1`
- `type:hardening`
- `area:verification`
- `area:github`
- `status:ready`

**Documentation for MCP trust model:**
- `priority:P2`
- `type:docs`
- `area:mcp`
- `area:docs`

**Replace temporary README:**
- `priority:P1`
- `type:docs`
- `area:readme`
- `area:branding`

---

## Import Script

Use this script to bulk-create all labels:

```bash
#!/bin/bash
# create-labels.sh — Bulk create GitHub labels

REPO="canstralian/pilot-shell-devsecops"

# Priority
gh label create "priority:P0" --color "B60205" --description "Critical — ship blocker" --repo "$REPO"
gh label create "priority:P1" --color "D93F0B" --description "High — should do immediately" --repo "$REPO"
gh label create "priority:P2" --color "FBCA04" --description "Medium — schedule within release cycle" --repo "$REPO"
gh label create "priority:P3" --color "0E8A16" --description "Low — backlog" --repo "$REPO"

# Type
gh label create "type:bug" --color "D73A4A" --description "Bug or defect" --repo "$REPO"
gh label create "type:feature" --color "A2EEEF" --description "New feature or capability" --repo "$REPO"
gh label create "type:security" --color "5319E7" --description "Security vulnerability or issue" --repo "$REPO"
gh label create "type:hardening" --color "6F42C1" --description "Security hardening or trust improvement" --repo "$REPO"
gh label create "type:docs" --color "0075CA" --description "Documentation update" --repo "$REPO"
gh label create "type:process" --color "C2E0C6" --description "Process or governance" --repo "$REPO"
gh label create "type:release" --color "1D76DB" --description "Release preparation or coordination" --repo "$REPO"

# Area
gh label create "area:installer" --color "F9D0C4" --description "Installation script and bootstrap" --repo "$REPO"
gh label create "area:settings" --color "FAD8C7" --description "Settings and configuration" --repo "$REPO"
gh label create "area:mcp" --color "E4E669" --description "MCP servers and integration" --repo "$REPO"
gh label create "area:verification" --color "BFDADC" --description "Testing and verification workflows" --repo "$REPO"
gh label create "area:hooks" --color "BFD4F2" --description "Git hooks and quality automation" --repo "$REPO"
gh label create "area:github" --color "D4C5F9" --description "GitHub-specific features" --repo "$REPO"
gh label create "area:docs" --color "C5DEF5" --description "Documentation files and sites" --repo "$REPO"
gh label create "area:branding" --color "F9D0C4" --description "Fork identity and attribution" --repo "$REPO"
gh label create "area:readme" --color "C5DEF5" --description "README.md specifically" --repo "$REPO"
gh label create "area:roadmap" --color "C5DEF5" --description "Planning and roadmap docs" --repo "$REPO"

# Status
gh label create "status:blocked" --color "000000" --description "Blocked by external dependency" --repo "$REPO"
gh label create "status:ready" --color "0E8A16" --description "Ready to implement" --repo "$REPO"
gh label create "status:in-progress" --color "FBCA04" --description "Work in progress" --repo "$REPO"
gh label create "status:needs-audit" --color "BFD4F2" --description "Requires security or compliance review" --repo "$REPO"
gh label create "needs-triage" --color "EDEDED" --description "Needs initial review and labeling" --repo "$REPO"

# Risk
gh label create "risk:high" --color "B60205" --description "High risk — critical security impact" --repo "$REPO"
gh label create "risk:medium" --color "D93F0B" --description "Medium risk — significant but contained" --repo "$REPO"
gh label create "risk:low" --color "0E8A16" --description "Low risk — minor or theoretical" --repo "$REPO"

# Special
gh label create "good-first-issue" --color "7057FF" --description "Suitable for new contributors" --repo "$REPO"
gh label create "help-wanted" --color "008672" --description "Community contributions welcome" --repo "$REPO"
gh label create "duplicate" --color "CFD3D7" --description "Duplicate of another issue" --repo "$REPO"
gh label create "wontfix" --color "FFFFFF" --description "Will not be implemented" --repo "$REPO"
gh label create "upstream" --color "E99695" --description "Should be fixed in upstream project" --repo "$REPO"
gh label create "breaking-change" --color "B60205" --description "Introduces breaking changes" --repo "$REPO"

echo "✅ All labels created successfully"
```

---

## Maintenance

- **Review quarterly**: Remove unused labels, add new categories as needed
- **Update this doc**: Keep label taxonomy documentation in sync with actual labels
- **Retag old issues**: Apply new labels to existing issues during triage

---

**Last Updated**: 2026-03-21
