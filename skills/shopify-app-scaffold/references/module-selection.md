# Module Selection

Use this reference after the scaffold script finishes.

## Core Assumption

The script handles the repeatable setup. The remaining work is product integration.

## `merchant-comms`

Adds:

- `ShopCommsPreferences`
- `EmailQueueItem`
- `JobLock`
- contact email sync helpers
- email opt-in persistence
- unsubscribe token generation
- queued email sending via SendGrid
- generic welcome, feedback, and review templates

Manual integration still needed:

- call `ensureShopContactEmail` after authentication or onboarding
- expose an email opt-in toggle in the app UI
- call `scheduleWelcomeEmail`, `scheduleFeedbackEmail`, or `scheduleReviewEmail` at product-specific milestones

## `review-prompts`

Adds:

- `ShopReviewState`
- `ReviewBanner`
- `ReviewPromptRequest`
- prompt result recording routes

Manual integration still needed:

- decide what counts as a meaningful milestone
- decide which screen should show the review banner
- pass a milestone count or milestone id from your app flow

## `billing-stub`

Reserved for a future overlay. The current skill does not bundle files for this module yet.

When it is implemented, it should still remain a thin shell and not build:

- pricing plans
- tier gates
- usage metering
- subscription enforcement

For now, omit this flag.

## `app-proxy`

Reserved for a future overlay. The current skill does not bundle files for this module yet.

When it is implemented, it should be used when the app needs storefront-facing output or request handling that is not limited to the embedded admin surface.

Good fit for:

- `llm.txt`
- agent-readable feeds
- generated storefront metadata

For now, omit this flag.

## `theme-extension`

Reserved for a future overlay. The current skill does not bundle files for this module yet.

When it is implemented, it should be used when the app needs theme app extension blocks, embeds, or storefront assets shipped through Shopify's extension system rather than an app proxy.

For now, omit this flag.

## UI Guidance

The scaffold uses generic Polaris-based UI helpers for the reusable overlays. Keep the generated app's default structure where possible, and only integrate the overlay UI where it makes sense for the product.
