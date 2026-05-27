# Media Hosting URL Contract

Use this contract whenever an Etsy Shop Uploader file includes `image_*`,
`video_1`, or `digital_file_*` URLs.

## Required Behavior

- Follow `/Users/maggielerman/Github/rps-etsy/docs/etsy/asset-hosting-policy.md`.
- Use approval-state-aware paths that are clear, current, and not copied from historical rapid-draft locations.
- Preserve a hosted URL manifest under the owning `rps-etsy` evidence folder.
- Audit every public URL before upload.
- Keep temporary URL cleanup status in the evidence packet.
- Do not populate Shop Uploader media/file URL columns until Maggie has approved the media/file apply plan.

## Default Audit Command

```bash
python3 scripts/etsy/audit-hosted-url-manifest.py <hosted-url-manifest.csv>
```
