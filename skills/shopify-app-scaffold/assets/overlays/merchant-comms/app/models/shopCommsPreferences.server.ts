import prisma from "../db.server";

const SHOP_EMAIL_QUERY = `#graphql
  query ShopContactEmail {
    shop {
      email
      contactEmail
    }
  }
`;

function normalizeEmail(value?: string | null) {
  return value?.trim() || null;
}

export async function getShopCommsPreferences(shop: string) {
  return prisma.shopCommsPreferences.findUnique({ where: { shop } });
}

export async function ensureShopCommsPreferences(shop: string, data?: { contactEmail?: string | null }) {
  const contactEmail = normalizeEmail(data?.contactEmail);
  return prisma.shopCommsPreferences.upsert({
    where: { shop },
    create: { shop, contactEmail },
    update: contactEmail ? { contactEmail } : {},
  });
}

export async function ensureShopContactEmail(shop: string, admin: { graphql: (query: string) => Promise<Response> }) {
  const response = await admin.graphql(SHOP_EMAIL_QUERY);
  const json = await response.json();
  const email =
    normalizeEmail(json?.data?.shop?.contactEmail) ??
    normalizeEmail(json?.data?.shop?.email);

  if (!email) {
    return ensureShopCommsPreferences(shop);
  }

  return ensureShopCommsPreferences(shop, { contactEmail: email });
}

export async function setEmailOptIn({
  shop,
  optIn,
  source,
}: {
  shop: string;
  optIn: boolean;
  source?: string;
}) {
  const now = new Date();
  return prisma.shopCommsPreferences.upsert({
    where: { shop },
    create: {
      shop,
      emailOptIn: optIn,
      emailOptInAt: optIn ? now : null,
      emailOptInSource: optIn ? source ?? null : null,
      emailUnsubscribedAt: optIn ? null : now,
    },
    update: {
      emailOptIn: optIn,
      emailOptInAt: optIn ? now : null,
      emailOptInSource: optIn ? source ?? null : null,
      emailUnsubscribedAt: optIn ? null : now,
    },
  });
}

export async function markShopUninstalled(shop: string) {
  const now = new Date();
  return prisma.shopCommsPreferences.upsert({
    where: { shop },
    create: { shop, uninstalledAt: now },
    update: { uninstalledAt: now },
  });
}
