import { useEffect, useRef } from "react";
import { useFetcher } from "react-router";
import { useOptionalAppBridge } from "../lib/useOptionalAppBridge";

type ReviewPromptRequestProps = {
  shouldRequest: boolean;
  milestoneId?: string | null;
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

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : String(error);
}

export function ReviewPromptRequest({ shouldRequest, milestoneId }: ReviewPromptRequestProps) {
  const app = useOptionalAppBridge<ReviewRequestAppBridge>();
  const fetcher = useFetcher();
  const requestedRef = useRef(false);

  useEffect(() => {
    if (!shouldRequest || requestedRef.current) return;
    const requestReview = app?.reviews?.request;
    if (!requestReview) return;

    requestedRef.current = true;

    const run = async () => {
      try {
        const result = await requestReview();
        fetcher.submit(
          new URLSearchParams({
            milestoneId: milestoneId ?? "",
            code: result.success ? "success" : result.code ?? "",
            message: result.message ?? "",
          }),
          { method: "post", action: "/app/review-prompt" },
        );
      } catch (error: unknown) {
        fetcher.submit(
          new URLSearchParams({
            milestoneId: milestoneId ?? "",
            code: "error",
            message: getErrorMessage(error),
          }),
          { method: "post", action: "/app/review-prompt" },
        );
      }
    };

    run();
  }, [app, fetcher, milestoneId, shouldRequest]);

  return null;
}
