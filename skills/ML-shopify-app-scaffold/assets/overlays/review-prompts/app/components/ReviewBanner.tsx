import { Banner, Button, InlineStack } from "@shopify/polaris";
import { useFetcher } from "react-router";
import { useCallback, useState } from "react";
import { useOptionalAppBridge } from "../lib/useOptionalAppBridge";

type ReviewBannerProps = {
  appName?: string;
  reviewUrl?: string | null;
};

type ReviewRequestResult = {
  success: boolean;
  code?: string;
  message?: string;
};

type ReviewRequestAppBridge = {
  reviews?: {
    request?: () => Promise<ReviewRequestResult>;
  };
};

export function ReviewBanner({ appName = "this app", reviewUrl }: ReviewBannerProps) {
  const app = useOptionalAppBridge<ReviewRequestAppBridge>();
  const fetcher = useFetcher();
  const [hidden, setHidden] = useState(false);

  const handleLeaveReview = useCallback(async () => {
    const requestReview = app?.reviews?.request;

    if (requestReview) {
      try {
        const result = await requestReview();
        fetcher.submit(
          new URLSearchParams({
            code: result.success ? "success" : result.code ?? "",
            message: result.message ?? "",
          }),
          { method: "post", action: "/app/review-prompt" },
        );

        if (!result.success && result.code === "rate-limited" && reviewUrl) {
          window.open(reviewUrl, "_blank");
        }
        setHidden(true);
        return;
      } catch {
        if (reviewUrl) {
          window.open(reviewUrl, "_blank");
        }
        setHidden(true);
        return;
      }
    }

    if (reviewUrl) {
      window.open(reviewUrl, "_blank");
      setHidden(true);
    }
  }, [app, fetcher, reviewUrl]);

  const handleDismiss = useCallback(() => {
    fetcher.submit(
      new URLSearchParams({ intent: "dismiss-banner" }),
      { method: "post", action: "/app/review-banner" },
    );
    setHidden(true);
  }, [fetcher]);

  if (hidden) {
    return null;
  }

  return (
    <Banner title={`Enjoying ${appName}?`} tone="info" onDismiss={handleDismiss}>
      <p>Your feedback helps other merchants discover helpful apps.</p>
      <InlineStack gap="200">
        <Button onClick={handleLeaveReview}>Leave a review</Button>
        <Button variant="plain" onClick={handleDismiss}>
          Maybe later
        </Button>
      </InlineStack>
    </Banner>
  );
}
