# Digital Product Packet Contract

Digital product packets are handoff bundles for creating, reviewing, and later
publishing Etsy digital-download products. They are not live-upload authority.

## Packet Must Include

- product type and target listing action
- source artwork and rights notes
- SKU/listing identifiers where known
- buyer ZIP/file manifest
- all promised aspect ratios and delivered file set
- mockup/media review board when media is included
- Shop Uploader template shape and field coverage notes
- hosted URL manifest when media or buyer files are hosted
- apply plan and explicit approval state

## Storage

Resolve the `rps-etsy` root using `repository-resolution.md`, then store real
packets in `docs/evidence/active/<project>/` relative to that root.

Store reusable creative assets in the Google Drive `RPS Creative Assets`
library and register them in the Drive-backed creative asset catalog snapshot
used by `rps-etsy`.
