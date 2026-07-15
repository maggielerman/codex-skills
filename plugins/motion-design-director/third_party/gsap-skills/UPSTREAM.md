# GSAP Skills Upstream

This plugin vendors official GSAP AI skills as the implementation layer for Motion Design Director.

- Source: https://github.com/greensock/gsap-skills
- Imported commit: `aed9cfd3277740755f6bfc1155c7aa645403b760`
- Imported date: 2026-07-15
- Imported paths: `skills/gsap-*`
- License: MIT, preserved in `LICENSE`
- Local normalization: trailing whitespace was removed from vendored `SKILL.md` files so repo `git diff --check` validation passes.

## Update Command

From the `codex-skills` repo root:

```bash
tmp_dir="$(mktemp -d)"
git clone --depth 1 https://github.com/greensock/gsap-skills.git "$tmp_dir"
rm -rf plugins/motion-design-director/skills/gsap-*
cp -R "$tmp_dir"/skills/gsap-* plugins/motion-design-director/skills/
cp "$tmp_dir/LICENSE" plugins/motion-design-director/third_party/gsap-skills/LICENSE
cp "$tmp_dir/README.md" plugins/motion-design-director/third_party/gsap-skills/README.md
git -C "$tmp_dir" rev-parse HEAD
rm -rf "$tmp_dir"
```

After updating, edit this file with the new commit SHA and rerun the plugin validation checks.
