
- # Hausaufgabenhelfer Pro

Serverseitige Streamlit-App zur Lizenz-basierten Nutzung deines Hausaufgabenhelfers plus Admin-Panel und Webhook-Anbindung für Digistore/Gumroad.

## Quickstart (lokal)
- Python 3.11, `pip install -r requirements.txt`
- `.env` anlegen (siehe `.env.example`) – nutze den **Service-Role-Key** deiner Supabase-Instanz.
- Supabase-Schema aus `supabase/schema.sql` im SQL-Editor ausführen.
- App starten: `streamlit run app.py`
- Admin-Dashboard: `streamlit run admin.py` (mit `ADMIN_PASSWORD` aus `.env`).

## Container
- Build: `docker build -t hausaufgabenhelfer .`
- Run: `docker run -p 8501:8501 --env-file .env hausaufgabenhelfer`
- Compose: `docker-compose up --build`

## Webhook-Server (optional Verkäufe automatisieren)
- `.env` muss `WEBHOOK_SECRET`, `SMTP_*`, `SUPABASE_SERVICE_ROLE_KEY` enthalten.
- Start: `python webhook_server.py`
- Endpunkte: `/webhook/digistore` (GET/POST), `/webhook/gumroad` (POST), `/health`
- Alle POST-Requests benötigen Header `X-Webhook-Secret: <WEBHOOK_SECRET>`.

## Supabase
- Tabelle `access_codes` per `supabase/schema.sql` anlegen.
- RLS: anonyme Rechte werden entzogen; verwende Service-Role-Key serverseitig.
- Edge Functions: `supabase/functions/validate_access_code` (Code prüfen) und `generate_access_code` (Codes generieren & mailen).

## Sicherheit/Verkauf-Checklist
- ✅ `ADMIN_PASSWORD` auf starken Wert setzen; `ADMIN_MAX_LOGIN_ATTEMPTS` nutzen.
- ✅ `SUPABASE_SERVICE_ROLE_KEY` statt Anon-Key verwenden; .env nicht einchecken.
- ✅ `WEBHOOK_SECRET` setzen und im Payment-Provider hinterlegen.
- ✅ SMTP nur mit App-Passwort/API-Key verwenden.
- ✅ Lizenzen: `LICENSE_REQUIRED=true` für Produktion; Beispielcodes im Schema nach Tests entfernen.

## Support
- Healthcheck: `GET /health` beim Webhook; Streamlit besitzt `_stcore/health`.
- Logs: siehe Streamlit/Flask-Ausgaben im Container/Procfile.
