import prisma from "../db.server";

const REVIEW_PROMPT_MIN_MILESTONES = 2;
const REVIEW_PROMPT_COOLDOWN_DAYS = 90;
const REVIEW_BANNER_COOLDOWN_DAYS = 14;

type ReviewPromptState = {
  dismissed?: boolean | null;
  lastRequestedAt?: Date | null;
  lastResultCode?: string | null;
  lastMilestoneId?: string | null;
};

type ReviewPromptDecision = {
  shouldRequest: boolean;
  reason?: string;
};

function daysBetween(start: Date, end: Date) {
  return (end.getTime() - start.getTime()) / (24 * 60 * 60 * 1000);
}

export function evaluateReviewPromptEligibility({
  milestoneCount,
  milestoneId,
  state,
  now = new Date(),
}: {
  milestoneCount: number;
  milestoneId?: string | null;
  state: ReviewPromptState | null;
  now?: Date;
}): ReviewPromptDecision {
  if (milestoneCount < REVIEW_PROMPT_MIN_MILESTONES) {
    return { shouldRequest: false, reason: "not-enough-milestones" };
  }

  if (state?.dismissed) {
    return { shouldRequest: false, reason: "dismissed" };
  }

  if (state?.lastResultCode === "already-reviewed") {
    return { shouldRequest: false, reason: "already-reviewed" };
  }

  if (milestoneId && state?.lastMilestoneId === milestoneId) {
    return { shouldRequest: false, reason: "already-prompted-milestone" };
  }

  if (state?.lastRequestedAt && daysBetween(state.lastRequestedAt, now) < REVIEW_PROMPT_COOLDOWN_DAYS) {
    return { shouldRequest: false, reason: "cooldown" };
  }

  return { shouldRequest: true };
}

export async function getReviewPromptState(shop: string) {
  return prisma.shopReviewState.findUnique({ where: { shop } });
}

export async function shouldPromptForReview({
  shop,
  milestoneCount,
  milestoneId,
}: {
  shop: string;
  milestoneCount: number;
  milestoneId?: string | null;
}) {
  const state = await getReviewPromptState(shop);
  return evaluateReviewPromptEligibility({ milestoneCount, milestoneId, state });
}

export async function shouldShowReviewBanner(shop: string, milestoneCount: number) {
  const state = await getReviewPromptState(shop);

  if (milestoneCount < REVIEW_PROMPT_MIN_MILESTONES) {
    return { show: false, reason: "not-enough-milestones" };
  }

  if (state?.dismissed) {
    return { show: false, reason: "dismissed" };
  }

  if (state?.lastResultCode === "already-reviewed") {
    return { show: false, reason: "already-reviewed" };
  }

  if (state?.lastRequestedAt && daysBetween(state.lastRequestedAt, new Date()) < REVIEW_BANNER_COOLDOWN_DAYS) {
    return { show: false, reason: "cooldown" };
  }

  return { show: true };
}

export async function recordReviewPromptResult({
  shop,
  milestoneId,
  resultCode,
}: {
  shop: string;
  milestoneId?: string | null;
  resultCode?: string | null;
}) {
  const now = new Date();
  const normalizedCode = resultCode || "unknown";
  const dismissed = normalizedCode === "already-reviewed";

  await prisma.shopReviewState.upsert({
    where: { shop },
    create: {
      shop,
      dismissed,
      lastRequestedAt: now,
      lastResultCode: normalizedCode,
      lastMilestoneId: milestoneId ?? null,
    },
    update: {
      dismissed: dismissed ? true : undefined,
      lastRequestedAt: now,
      lastResultCode: normalizedCode,
      lastMilestoneId: milestoneId ?? undefined,
    },
  });
}

export async function setReviewPromptDismissed(shop: string, dismissed: boolean) {
  await prisma.shopReviewState.upsert({
    where: { shop },
    create: { shop, dismissed },
    update: { dismissed },
  });
}

export async function recordBannerDismissed(shop: string) {
  await prisma.shopReviewState.upsert({
    where: { shop },
    create: {
      shop,
      lastRequestedAt: new Date(),
      lastResultCode: "banner-dismissed",
    },
    update: {
      lastRequestedAt: new Date(),
      lastResultCode: "banner-dismissed",
    },
  });
}
