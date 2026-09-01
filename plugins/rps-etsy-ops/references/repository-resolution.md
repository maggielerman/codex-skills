# Repository Resolution

RPS Etsy workflows must resolve repositories on the current host; committed
skill text must never assume a username or absolute home-directory path.

## Resolution Order

1. When the active Codex project is the needed repository, resolve its root
   with `git rev-parse --show-toplevel`.
2. Otherwise use the current host's local project mapping or ignored
   `codex-skills/config/host-overlay.local.json` `repositoryRoots` entry.
3. If the repository is not cloned or attached on this host, stop before
   creating artifacts or attempting a live operation and report the missing
   repository by name.

Use these stable mapping keys:

- `rps-etsy` for the Etsy catalog operations repository
- `rps-creative-assets` for the read-only migration archive
- `shopify-headless` for the optional Shopify readiness repository
- `codex-skills` for the capability-source repository

After resolution, treat every documented path and command as relative to the
owning repository root. Do not copy a resolved host-local path into Git-backed
context, evidence, templates, or skill instructions.
