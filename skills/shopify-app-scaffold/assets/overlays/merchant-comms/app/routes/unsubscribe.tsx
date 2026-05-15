import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { Card, Page, Text, BlockStack } from "@shopify/polaris";
import { setEmailOptIn } from "../models/shopCommsPreferences.server";
import { verifyUnsubscribeToken } from "../services/unsubscribe.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const token = url.searchParams.get("token");

  if (!token) {
    return { ok: false, message: "Missing token." };
  }

  const payload = verifyUnsubscribeToken(token);
  if (!payload) {
    return { ok: false, message: "Invalid or expired token." };
  }

  await setEmailOptIn({ shop: payload.shop, optIn: false, source: "unsubscribe" });
  return { ok: true, message: "You are unsubscribed." };
};

export default function UnsubscribePage() {
  const data = useLoaderData<typeof loader>();

  return (
    <Page title="Email preferences">
      <Card>
        <BlockStack gap="200">
          <Text as="p" variant="bodyMd">
            {data.message}
          </Text>
          {data.ok ? (
            <Text as="p" variant="bodySm" tone="subdued">
              You can re-enable emails later from your app settings.
            </Text>
          ) : null}
        </BlockStack>
      </Card>
    </Page>
  );
}
