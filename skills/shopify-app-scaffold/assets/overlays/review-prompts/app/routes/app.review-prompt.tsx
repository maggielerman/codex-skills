import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import { recordReviewPromptResult } from "../services/reviewPrompt.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const formData = await request.formData();
  const milestoneId = formData.get("milestoneId")?.toString() || undefined;
  const code = formData.get("code")?.toString() || undefined;

  await recordReviewPromptResult({
    shop: session.shop,
    milestoneId,
    resultCode: code,
  });

  return Response.json({ ok: true });
};
