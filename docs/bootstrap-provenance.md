# Bootstrap and Release Provenance

## Current Status

This fork (`canstralian/pilot-shell-devsecops`) does **not yet** publish independent
release artifacts. The installer (`install.sh`) downloads all binaries and Python
installer files from the upstream repository:

```
https://github.com/maxritter/pilot-shell
```

This means users who install via this fork's `install.sh` are trusting artifacts
produced by the upstream project, not by this fork. That dependency is
intentional and documented — it is not a silent supply-chain assumption.

## Supply Chain Dependency Summary

| Artifact | Source |
| --- | --- |
| `pilot` binary wrapper | `github.com/maxritter/pilot-shell` releases |
| `pilot.<platform>.so` module | `github.com/maxritter/pilot-shell` releases |
| `installer/*.py` files | `github.com/maxritter/pilot-shell` releases |
| `pyproject.toml` | `github.com/maxritter/pilot-shell` raw at version tag |

## Installer Provenance Notice

The installer displays an explicit supply-chain notice at startup so users are
informed before any downloads begin:

```
  ⚠  SUPPLY CHAIN NOTICE
  This fork does not yet publish independent release artifacts.
  Binaries and installer files are downloaded from upstream:
    https://github.com/maxritter/pilot-shell
  See docs/bootstrap-provenance.md for details.
```

## Next Steps to Publish Fork-Native Releases

To eliminate the upstream binary dependency and ship fully fork-native artifacts:

1. **Build the `pilot` binary and `.so` module** from the fork's source.
   The `.releaserc.json` in this repo already configures semantic-release, but
   the binary build pipeline must be adapted to build and attach platform artifacts
   to GitHub Releases.

2. **Trigger a versioned release** from the `main` branch. The semantic-release
   configuration will create a `vX.Y.Z` tag and GitHub Release automatically
   when a `feat:` or `fix:` commit lands on `main`.

3. **Update `REPO` in `install.sh`** once a valid release exists:
   ```bash
   # Change:
   REPO="$UPSTREAM_REPO"
   # To:
   REPO="$FORK_REPO"
   ```
   Also remove or update the supply-chain notice to reflect the fork-native status.

4. **Verify end-to-end** by running the installer against a fork release and
   confirming no upstream downloads occur.

## Attribution

The upstream project is [`maxritter/pilot-shell`](https://github.com/maxritter/pilot-shell).
This fork preserves attribution and relies on upstream binaries in the interim.
All upstream intellectual property remains credited to its authors.
