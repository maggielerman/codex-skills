# MacBook Air Automation Ownership Inventory

Recorded: 2026-09-01 05:37 ET (America/New_York)

This inventory covers the 17 local Codex scheduler records present on the MacBook Air. It is sanitized: prompts, destinations, task/thread identifiers, notification payloads, mailbox identities, credentials, message data, and private source paths are omitted.

The scheduler records do not declare an explicit timezone identifier. Cadences below are therefore rendered in the Air's host-local timezone, `America/New_York`.

## Inventory

| User-visible name | State | Human-readable cadence | Timezone | Kind | Owning repository or domain | Current host ownership | Recommendation |
|---|---|---|---|---|---|---|---|
| 1085 Growth Packet | Paused | Mondays at 9:00 AM | America/New_York, Air local | Cron | Shopify/RPS growth packet | Air local scheduler record | Leave paused pending review |
| Customer Account Cutover Reminder | Paused | Every 24 hours; start time not encoded | America/New_York, Air local | Cron | Shopify customer-account cutover | Air local scheduler record | Retire/review |
| Twice-weekly Chronicle automatic publisher | Paused | Mondays and Thursdays at 9:00 AM | America/New_York, Air local | Cron | Hyphenomenon historical Chronicle publishing | Air local scheduler record | Retire/review |
| Daily intake queue summary | Paused | Daily at 9:00 AM | America/New_York, Air local | Heartbeat | Hyphenomenon intake queue | Air local scheduler record | Leave paused pending review |
| Uniform multi-mailbox important-mail monitor | Active | Hourly from 7:00 AM through 10:00 PM | America/New_York, Air local | Heartbeat | Multi-Mailbox Ops monitoring | Air local scheduler record | Keep Air |
| Daily Skysight source durability | Active | Daily at 1:15 AM | America/New_York, Air local | Cron | Chronicle Visualizer / Skysight source collection | Air local scheduler record | Keep Air |
| Notion dashboard sync | Paused | Daily at 5:00 AM, 12:00 PM, and 5:00 PM | America/New_York, Air local | Cron | Notion project dashboard | Air local scheduler record | Leave paused pending review |
| Performance regression watch | Paused | Daily at 9:00 AM | America/New_York, Air local | Cron | Family Shapes performance | Air local scheduler record | Leave paused pending review |
| Performance regression watch | Paused | Daily at 9:00 AM | America/New_York, Air local | Cron | Shopify/RPS storefront performance | Air local scheduler record | Leave paused pending review |
| Project 1138 closure heartbeat | Paused | Daily; execution time not encoded | America/New_York, Air local | Heartbeat | Shopify/RPS Project 1138 closure | Air local scheduler record | Retire/review |
| RPS autonomous catalog and editorial operator | Active | Daily at 6:00 AM | America/New_York, Air local | Cron | RPS Shopify catalog and editorial operations | Air local scheduler record | Keep Air |
| Skill progression map | Paused | Fridays at 10:00 AM | America/New_York, Air local | Cron | Family Shapes skill progression | Air local scheduler record | Leave paused pending review |
| Skills Sync | Paused | Fridays at 9:00 AM | America/New_York, Air local | Cron | `codex-skills` capability sync | Air local scheduler record | Retire/review |
| Skills Sync | Paused | Fridays at 9:00 AM | America/New_York, Air local | Cron | Codex-home capability sync | Air local scheduler record | Retire/review |
| Daily Skysight automatic publisher | Active | Daily at 9:00 AM | America/New_York, Air local | Cron | Hyphenomenon Skysight publishing | Air local scheduler record | Candidate Pro |
| Weekly Codex report publisher | Active | Mondays at 9:00 AM | America/New_York, Air local | Cron | Hyphenomenon Codex-usage reporting | Air local scheduler record | Candidate Pro |
| RPS autonomous and editorial review | Active | Daily at 9:00 AM | America/New_York, Air local | Heartbeat | RPS wholesale/digital editorial review | Air local scheduler record | Candidate Pro |

## Proven Ownership Split

The tracked two-workstation baseline assigns live mailbox monitoring to Air and combined report publishing/orchestration to Pro. It also assigns Chronicle Visualizer source collection to Air and report aggregation to Pro. The documented Skysight cutover separately distinguishes source durability from forward-writing publishers.

This supports the following split:

- **Keep Air:** `Uniform multi-mailbox important-mail monitor` is the credential-bound live MMO operations stream.
- **Keep Air:** `Daily Skysight source durability` is the source collector/durability stream.
- **Candidate Pro:** `Daily Skysight automatic publisher` is a forward-writing publisher.
- **Candidate Pro:** `Weekly Codex report publisher` is a forward-writing combined report publisher.
- **Retire/review:** `Twice-weekly Chronicle automatic publisher` is the preserved historical publisher and is already paused after successor proof.

The current local Skysight publisher name and daily cadence differ from the documented cutover record, which describes a twice-weekly Skysight publisher. That is recorded as contract drift requiring review, not silently interpreted as an approved cadence change.

The active RPS catalog/editorial operator remains recommended for Air because it is an operational, credential-bound writer. The baseline also labels Air as fallback rather than primary for the broader Shopify project, so this recommendation should be revisited if Pro becomes the exclusive RPS orchestration owner. The separate read-only RPS editorial-review heartbeat is a Pro candidate.

Duplicate user-visible names are not assumed to be duplicate work: the two performance watches have different domains. The two paused Skills Sync records have overlapping capability-sync ownership and should be reviewed together before either is resumed.

## Totals

### By status

- Active: 6
- Paused: 11
- Total: 17

### By recommendation

- Keep Air: 3
- Candidate Pro: 3
- Retire/review: 5
- Leave paused pending review: 6
- Total: 17

## Zero-change Statement

This was a read-only inventory. No automation was created, updated, paused, resumed, renamed, deleted, triggered, duplicated, or moved. No prompt, destination, notification policy, plugin, credential, mailbox, or scheduler state was changed.
