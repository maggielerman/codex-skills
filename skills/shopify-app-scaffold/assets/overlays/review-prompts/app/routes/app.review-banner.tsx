import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import { recordBannerDismissed } from "../services/reviewPrompt.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const formData = await request.formData();
  const intent = formData.get("intent")?.toString();

  if (intent === "dismiss-banner") {
    await recordBannerDismissed(session.shop);
    return Response.json({ ok: true });
  }

  return Response.json({ ok: false, error: "Unknown intent" }, { status: 400 });
};
