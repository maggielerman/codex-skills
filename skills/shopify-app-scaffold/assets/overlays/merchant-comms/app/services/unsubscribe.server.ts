import crypto from "crypto";

const TOKEN_SEPARATOR = ".";

function getSecret() {
  return process.env.EMAIL_UNSUBSCRIBE_SECRET || process.env.SHOPIFY_API_SECRET || "missing-secret";
}

export function createUnsubscribeToken({ shop, email }: { shop: string; email: string }) {
  const payload = Buffer.from(JSON.stringify({ shop, email })).toString("base64url");
  const signature = crypto.createHmac("sha256", getSecret()).update(payload).digest("hex");
  return `${payload}${TOKEN_SEPARATOR}${signature}`;
}

export function verifyUnsubscribeToken(token: string) {
  const [payload, signature] = token.split(TOKEN_SEPARATOR);
  if (!payload || !signature) return null;

  const expected = crypto.createHmac("sha256", getSecret()).update(payload).digest("hex");
  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
    return null;
  }

  try {
    const decoded = JSON.parse(Buffer.from(payload, "base64url").toString("utf-8"));
    if (!decoded?.shop || !decoded?.email) return null;
    return decoded as { shop: string; email: string };
  } catch {
    return null;
  }
}

export function createUnsubscribeLink({ shop, email }: { shop: string; email: string }) {
  const appUrl = process.env.SHOPIFY_APP_URL || "";
  const token = createUnsubscribeToken({ shop, email });
  return `${appUrl}/unsubscribe?token=${encodeURIComponent(token)}`;
}
