import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { Resend } from "https://esm.sh/resend@3.2.0";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors() });
  }

  try {
    // 1) Webhook-Schutz (Tentary -> Supabase)
    const given = req.headers.get("X-Webhook-Secret") || "";
    const expected = Deno.env.get("TENTARY_WEBHOOK_SECRET") || "";
    if (!expected || given !== expected) {
      return json({ ok: false, error: "unauthorized" }, 401);
    }

    // 2) Payload lesen (order_id + email)
    const payload = await req.json().catch(() => ({}));

    const order_id =
      payload.order_id ??
      payload.orderId ??
      payload.id ??
      null;

    const email =
      payload.email ??
      payload.customer_email ??
      payload.customer?.email ??
      null;

    if (!email) {
      return json({ ok: false, error: "missing_email" }, 400);
    }

    // 3) Code erzeugen
    const code = generateCode();

    // 4) In DB speichern (Service Role)
    const projectUrl = Deno.env.get("PROJECT_URL") || "";
    const serviceRoleKey = Deno.env.get("SERVICE_ROLE_KEY") || "";
    if (!projectUrl || !serviceRoleKey) {
      throw new Error("Missing PROJECT_URL or SERVICE_ROLE_KEY");
    }

    const supabase = createClient(projectUrl, serviceRoleKey);

    const { error } = await supabase.from("access_codes").insert({
      code,
      kind: "paid",
      active: true,
      tentary_order_id: order_id,
      buyer_email: email,
    });

    if (error) throw error;

    // 5) E-Mail versenden (Resend)
    await sendAccessCodeEmail(email, code);

    return json({ ok: true, code });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
}, { verifyJwt: false });

function generateCode() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const part = (n: number) =>
    Array.from({ length: n }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
  return `${part(4)}-${part(4)}-${part(4)}`;
}

async function sendAccessCodeEmail(to: string, code: string) {
  const apiKey = Deno.env.get("RESEND_API_KEY") || "";
  const from = Deno.env.get("EMAIL_FROM") || "";

  if (!apiKey) throw new Error("Missing RESEND_API_KEY");
  if (!from) throw new Error("Missing EMAIL_FROM");

  const resend = new Resend(apiKey);

  const subject = "Dein Zugangscode – Hausaufgabenhelfer (lebenslang)";

  const text = `
Vielen Dank für deinen Kauf!

Dein persönlicher Zugangscode (lebenslang gültig):
${code}

So funktioniert es:
1) App öffnen
2) Zugangscode eingeben
3) Loslegen

Dieser Zugangscode ist durch deine Einmalzahlung lebenslang gültig.
`;

  const html = `
<p>Vielen Dank für deinen Kauf!</p>

<p><b>Dein persönlicher Zugangscode (lebenslang gültig):</b><br>
<code style="font-size:18px">${code}</code></p>

<p><b>So funktioniert es:</b></p>
<ol>
  <li>App öffnen</li>
  <li>Zugangscode eingeben</li>
  <li>Loslegen</li>
</ol>

<p><b>Hinweis:</b> Dieser Zugangscode ist lebenslang gültig.</p>
`;

  await resend.emails.send({
    from,
    to,
    subject,
    text,
    html,
  });
}

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...cors() },
  });
}

function cors() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type, X-Webhook-Secret",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
  };
}