# Trust Boundary Hardening Note

## What changed and why

Three high-trust defaults in `pilot/settings.json` were tightened to reduce ambient
privilege in local execution. All MCP package invocations in `pilot/.mcp.json` were
pinned to exact versions to prevent silent supply-chain updates.

### `pilot/settings.json` – before → after

| Setting | Before | After | Reason |
|---|---|---|---|
| `permissions.defaultMode` | `"bypassPermissions"` | `"default"` | Require explicit approval for dangerous file-system and shell operations instead of silently bypassing all permission checks. |
| `skipDangerousModePermissionPrompt` | `true` | `false` | Surface the danger prompt so the operator actively acknowledges elevated operations. |
| `enableAllProjectMcpServers` | `true` | `false` | Prevent project-level `.mcp.json` files from loading MCP servers automatically; each server must be explicitly opted in. |

### `pilot/.mcp.json` – pinned `npx` package versions

| Server | Before | After |
|---|---|---|
| `context7` | `@upstash/context7-mcp` (unpinned) | `@upstash/context7-mcp@2.1.4` |
| `web-search` | `open-websearch` (unpinned) | `open-websearch@1.2.7` |
| `web-fetch` | `fetcher-mcp` (unpinned) | `fetcher-mcp@0.3.9` |

`codebase-memory-mcp` and `mem-search` are invoked via local binaries and are not
affected by npm registry updates; no version pinning is required for those entries.

---

## Residual trust surfaces

The following settings remain at elevated trust levels intentionally. They should be
revisited as the fork matures.

### Still in `pilot/settings.json`

| Setting | Value | Risk | Mitigation status |
|---|---|---|---|
| `DISABLE_INSTALLATION_CHECKS` | `"true"` | Bypasses Claude Code installation guard-rails. Required for the fork's custom install path. | Accepted; document in install.sh |
| `grep-mcp` (`type: http`) | `https://mcp.grep.app` | All tool calls are sent to a third-party HTTPS endpoint. No local execution, but data leaves the machine. | Low – read-only code search. Review if sensitive code is present. |
| `mem-search` | Local `bun` script path | Script is not version-controlled in this repo; integrity relies on the local filesystem. | Medium – verify script provenance after install. |
| `npx -y` flags | Present on all pinned packages | Auto-installs the pinned version without a secondary prompt. Acceptable given explicit pinning. | Low – monitor for yanked/compromised releases. |

### Not changed in this patch

- `install.sh` still points to `REPO="maxritter/pilot-shell"` upstream. Supply-chain
  risk at bootstrap time. Tracked separately (P0 installer issue).
- No cryptographic signature verification is performed on downloaded binaries or MCP
  packages. This is a structural gap that requires a separate hardening pass.
