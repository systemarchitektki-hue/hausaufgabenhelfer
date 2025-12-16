import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204 });
  }

  try {
    const { code } = await req.json();

    if (!code) {
      return json({ valid: false, reason: "no_code" }, 400);
    }

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

const { data, error } = await supabase
  .from("access_codes")
  .select("*")
  .eq("Code", code)      // <- wichtig: Großes C wie in deiner Tabelle
  .eq("aktiv", true)     // <- wichtig: aktiv
  .maybeSingle();

if (error || !data) {
  return json({ valid: false, reason: "not_found" });
}

if (data.expires_at) {
  const now = new Date();
  const expires = new Date(data.expires_at);
  if (expires < now) {
    return json({ valid: false, reason: "expired" });
  }
}

return json({ valid: true });

  } catch (e) {
    return json({ valid: false, reason: "error" }, 500);
  }
});

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
