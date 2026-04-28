import { createUnsubscribeLink } from "./unsubscribe.server";

export type EmailTemplateName = "welcome" | "feedback" | "review";

type EmailTemplateInput = {
  shop: string;
  toEmail: string;
  appName: string;
  appStoreUrl?: string | null;
};

type RenderedEmail = {
  subject: string;
  html: string;
  text: string;
};

export function renderEmailTemplate(template: EmailTemplateName, input: EmailTemplateInput): RenderedEmail {
  const unsubscribeUrl = createUnsubscribeLink({ shop: input.shop, email: input.toEmail });
  const reviewUrl = input.appStoreUrl ? `${input.appStoreUrl}#modal-show=WriteReviewModal` : null;

  switch (template) {
    case "welcome":
      return {
        subject: `You're all set with ${input.appName}`,
        text: [
          `Thanks for opting in to updates from ${input.appName}.`,
          "Start here:",
          "1) Open the app",
          "2) Configure the first meaningful workflow",
          "3) Validate the result in your store",
          "",
          `Unsubscribe: ${unsubscribeUrl}`,
        ].join("\n"),
        html: `
          <p>Thanks for opting in to updates from <strong>${input.appName}</strong>.</p>
          <p><strong>Start here</strong></p>
          <ol>
            <li>Open the app</li>
            <li>Configure the first meaningful workflow</li>
            <li>Validate the result in your store</li>
          </ol>
          <p><a href="${unsubscribeUrl}">Unsubscribe</a></p>
        `,
      };
    case "feedback":
      return {
        subject: `How is ${input.appName} going so far?`,
        text: [
          `Thanks for using ${input.appName}.`,
          "We would love quick feedback:",
          "- What worked well",
          "- What felt confusing",
          "- What you want next",
          "",
          `Unsubscribe: ${unsubscribeUrl}`,
        ].join("\n"),
        html: `
          <p>Thanks for using <strong>${input.appName}</strong>.</p>
          <p>We would love quick feedback:</p>
          <ul>
            <li>What worked well</li>
            <li>What felt confusing</li>
            <li>What you want next</li>
          </ul>
          <p><a href="${unsubscribeUrl}">Unsubscribe</a></p>
        `,
      };
    case "review":
      return {
        subject: `Could you leave a quick review for ${input.appName}?`,
        text: [
          `If ${input.appName} has been helpful, we would appreciate a quick review on the Shopify App Store.`,
          ...(reviewUrl ? [`Leave a review: ${reviewUrl}`] : []),
          "",
          `Unsubscribe: ${unsubscribeUrl}`,
        ].join("\n"),
        html: `
          <p>If <strong>${input.appName}</strong> has been helpful, we would appreciate a quick review on the Shopify App Store.</p>
          ${reviewUrl ? `<p><a href="${reviewUrl}">Leave a review</a></p>` : ""}
          <p><a href="${unsubscribeUrl}">Unsubscribe</a></p>
        `,
      };
  }
}
