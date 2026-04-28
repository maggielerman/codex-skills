import { getShopCommsPreferences } from "../models/shopCommsPreferences.server";
import { scheduleEmail } from "./emailQueue.server";
import type { EmailTemplateName } from "./emailTemplates.server";

const WELCOME_DELAY_MS = 60 * 60 * 1000;
const FEEDBACK_DELAY_MS = 5 * 24 * 60 * 60 * 1000;
const REVIEW_DELAY_MS = 7 * 24 * 60 * 60 * 1000;

async function scheduleLifecycleEmail(shop: string, template: EmailTemplateName, delayMs: number) {
  const prefs = await getShopCommsPreferences(shop);
  if (!prefs || !prefs.emailOptIn || prefs.emailUnsubscribedAt || prefs.uninstalledAt) {
    return null;
  }

  if (!prefs.contactEmail) {
    return null;
  }

  return scheduleEmail({
    shop,
    toEmail: prefs.contactEmail,
    template,
    scheduledAt: new Date(Date.now() + delayMs),
  });
}

export async function scheduleWelcomeEmail(shop: string) {
  return scheduleLifecycleEmail(shop, "welcome", WELCOME_DELAY_MS);
}

export async function scheduleFeedbackEmail(shop: string) {
  return scheduleLifecycleEmail(shop, "feedback", FEEDBACK_DELAY_MS);
}

export async function scheduleReviewEmail(shop: string) {
  return scheduleLifecycleEmail(shop, "review", REVIEW_DELAY_MS);
}
