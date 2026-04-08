import type { Prisma } from "@prisma/client";
import prisma from "../db.server";
import { sendEmail } from "./email.server";
import { renderEmailTemplate, type EmailTemplateName } from "./emailTemplates.server";

const EMAIL_QUEUE_LOCK_ID = "email-queue";
const EMAIL_QUEUE_TTL_MS = 5 * 60 * 1000;
const EMAIL_QUEUE_INTERVAL_MS = 5 * 60 * 1000;

let started = false;
let processing = false;
let fallbackTimer: NodeJS.Timeout | null = null;
const lockOwner = `${process.pid}-${Math.random().toString(36).slice(2)}`;

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : String(error);
}

export async function scheduleEmail({
  shop,
  toEmail,
  template,
  payload,
  scheduledAt,
}: {
  shop: string;
  toEmail: string;
  template: EmailTemplateName;
  payload?: Prisma.InputJsonValue;
  scheduledAt: Date;
}) {
  const existing = await prisma.emailQueueItem.findFirst({
    where: {
      shop,
      template,
      cancelledAt: null,
      sentAt: null,
    },
  });

  if (existing) {
    return existing;
  }

  return prisma.emailQueueItem.create({
    data: {
      shop,
      toEmail,
      template,
      payload: payload ?? {},
      scheduledAt,
    },
  });
}

export async function cancelScheduledEmailsForShop(shop: string) {
  await prisma.emailQueueItem.updateMany({
    where: { shop, sentAt: null, cancelledAt: null },
    data: { cancelledAt: new Date() },
  });
}

export function startEmailQueue() {
  if (process.env.EMAIL_QUEUE_ENABLED === "0") {
    console.info("[emailQueue] disabled via EMAIL_QUEUE_ENABLED=0");
    return;
  }
  if (started) return;
  started = true;
  processEmailQueue().catch((err) => console.error("[emailQueue] startup failed", err));
  scheduleFallback();
}

function scheduleFallback() {
  if (fallbackTimer) clearTimeout(fallbackTimer);
  fallbackTimer = setTimeout(() => {
    if (processing) {
      scheduleFallback();
      return;
    }
    processEmailQueue().catch((err) => console.error("[emailQueue] fallback failed", err));
  }, EMAIL_QUEUE_INTERVAL_MS);
  fallbackTimer.unref?.();
}

async function processEmailQueue() {
  if (processing) return;
  processing = true;
  let heldLock = false;

  try {
    heldLock = await acquireLock();
    if (!heldLock) {
      return;
    }

    const due = await prisma.emailQueueItem.findMany({
      where: {
        sentAt: null,
        cancelledAt: null,
        scheduledAt: { lte: new Date() },
      },
      orderBy: { scheduledAt: "asc" },
      take: 25,
    });

    for (const item of due) {
      const prefs = await prisma.shopCommsPreferences.findUnique({ where: { shop: item.shop } });
      if (!prefs || !prefs.emailOptIn || prefs.emailUnsubscribedAt || prefs.uninstalledAt) {
        await prisma.emailQueueItem.update({
          where: { id: item.id },
          data: { cancelledAt: new Date() },
        });
        continue;
      }

      try {
        const rendered = renderEmailTemplate(item.template as EmailTemplateName, {
          shop: item.shop,
          toEmail: item.toEmail,
          appName: process.env.APP_NAME || "Shopify App",
          appStoreUrl: process.env.SHOPIFY_APP_STORE_URL || null,
        });

        const result = await sendEmail({
          to: item.toEmail,
          subject: rendered.subject,
          html: rendered.html,
          text: rendered.text,
          tag: item.template,
        });

        await prisma.emailQueueItem.update({
          where: { id: item.id },
          data: result.skipped ? { lastError: "Email provider not configured" } : { sentAt: new Date(), lastError: null },
        });
      } catch (error: unknown) {
        await prisma.emailQueueItem.update({
          where: { id: item.id },
          data: { lastError: getErrorMessage(error) },
        });
      }
    }
  } finally {
    if (heldLock) {
      await releaseLock();
    }
    processing = false;
    scheduleFallback();
  }
}

async function acquireLock(): Promise<boolean> {
  const result = await prisma.$queryRaw<{ owner: string }[]>`
    INSERT INTO "JobLock" ("id", "owner", "lockedAt", "expiresAt")
    VALUES (${EMAIL_QUEUE_LOCK_ID}, ${lockOwner}, NOW(), NOW() + INTERVAL '${Math.floor(EMAIL_QUEUE_TTL_MS / 1000)} seconds')
    ON CONFLICT ("id") DO UPDATE
    SET "owner" = EXCLUDED."owner",
        "lockedAt" = NOW(),
        "expiresAt" = EXCLUDED."expiresAt"
    WHERE "JobLock"."expiresAt" < NOW() OR "JobLock"."owner" = EXCLUDED."owner"
    RETURNING "owner"
  `;

  return Array.isArray(result) && result.length > 0 && result[0].owner === lockOwner;
}

async function releaseLock() {
  await prisma.$executeRaw`
    UPDATE "JobLock"
    SET "expiresAt" = NOW() - INTERVAL '1 seconds'
    WHERE "id" = ${EMAIL_QUEUE_LOCK_ID} AND "owner" = ${lockOwner}
  `;
}
