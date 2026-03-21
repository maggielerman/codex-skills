# Cluster Plan Template

Use this table for planning before any branch/worktree setup.

| Cluster | Projects | Objective | Dependencies | Shared File Risk | Branch | Worktree | Tracking Issue | First Agent Command |
|---|---|---|---|---|---|---|---|---|
| A | 3004 | Rebaseline docs execution | None | Low | `codex/3004-rebaseline-phase1` | `/abs/path/repo-worktrees/3004-rebaseline-phase1` | `#123` | `git status -sb` |
| B | 3024,3022 | Public/docs polish | Wait for A docs index shape | Medium | `codex/3024-3022-public-polish` | `/abs/path/repo-worktrees/3024-3022-public-polish` | `#124` | `rg --files DOCS` |

## Required checks

- Ensure each cluster has a clear merge gate.
- Flag any pair of clusters that edit the same files/directories.
- Include one checkpoint timestamp expectation per cluster.
