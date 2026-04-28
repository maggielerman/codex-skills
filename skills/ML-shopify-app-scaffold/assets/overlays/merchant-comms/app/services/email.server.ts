import sgMail from "@sendgrid/mail";

type SendEmailInput = {
  to: string;
  subject: string;
  html: string;
  text: string;
  tag?: string;
};

let configured = false;

function configure() {
  const apiKey = process.env.SENDGRID_API_KEY;
  if (!apiKey) return false;
  if (!configured) {
    sgMail.setApiKey(apiKey);
    configured = true;
  }
  return true;
}

export async function sendEmail({ to, subject, html, text, tag }: SendEmailInput) {
  const from = process.env.EMAIL_FROM;
  const ready = configure();

  if (!from || !ready) {
    console.warn("[email] missing EMAIL_FROM or SENDGRID_API_KEY; skipping send");
    return { skipped: true };
  }

  await sgMail.send({
    to,
    from,
    subject,
    html,
    text,
    ...(tag ? { categories: [tag] } : {}),
  });

  return { skipped: false };
}
