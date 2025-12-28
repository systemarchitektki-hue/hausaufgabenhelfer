"""
Automatischer Webhook-Server für Digistore24/Gumroad
Erstellt automatisch Zugangscodes nach Kauf und sendet E-Mail an Kunden
"""
import os
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional

try:
    from flask import Flask, request, jsonify  # type: ignore
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    from supabase import create_client  # type: ignore
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

if not FLASK_AVAILABLE:
    raise ImportError("Flask nicht installiert. Führe aus: pip install flask")
if not SUPABASE_AVAILABLE:
    raise ImportError("Supabase nicht installiert. Führe aus: pip install supabase")

app = Flask(__name__)

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY", "")
SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER: str = os.getenv("SMTP_USER", "")
SMTP_PASS: str = os.getenv("SMTP_PASS", "")
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "dein-geheimer-key")

def verify_secret(req) -> bool:
    """Verifiziert gemeinsamen Webhook-Secret-Header oder Query-Param."""
    expected = WEBHOOK_SECRET
    if not expected:
        return False
    given = req.headers.get("X-Webhook-Secret") or req.args.get("webhook_secret")
    return bool(given and secrets.compare_digest(given, expected))

def ensure_supabase_ready() -> None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL oder SUPABASE_SERVICE_ROLE_KEY fehlen für Webhook-Verarbeitung")

def generate_code() -> str:
    """Generiert einen zufälligen Zugangscode"""
    chars = string.ascii_uppercase + string.digits
    return f"{''.join(secrets.choice(chars) for _ in range(4))}-{''.join(secrets.choice(chars) for _ in range(4))}-{''.join(secrets.choice(chars) for _ in range(4))}"

def create_access_code(email: str, name: str, product: str = "standard") -> str:
    """Erstellt Zugangscode in Supabase"""
    ensure_supabase_ready()
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    code = generate_code()
    
    expires: Optional[str] = None
    if product == "monthly":
        expires = (datetime.now() + timedelta(days=30)).isoformat()
    elif product == "yearly":
        expires = (datetime.now() + timedelta(days=365)).isoformat()
    
    supabase.table("access_codes").insert({
        "code": code,
        "email": email,
        "name": name,
        "is_active": True,
        "expires_at": expires,
        "notes": f"Auto-generiert: {product}"
    }).execute()
    
    return code

def send_email(to_email: str, name: str, code: str) -> None:
    """Sendet Zugangscode per E-Mail"""
    if not SMTP_USER or not SMTP_PASS:
        raise ValueError("SMTP_USER und SMTP_PASS müssen konfiguriert sein")
    
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = "Dein Zugangscode für Hausaufgabenhelfer Pro"
    
    body = f"""
Hallo {name},

vielen Dank für deinen Kauf!

Dein persönlicher Zugangscode: {code}

So nutzt du die App:
1. Gehe zu https://hausaufgabenhelfer.streamlit.app
2. Gib deinen Zugangscode ein
3. Fertig! Du kannst sofort loslegen.

Bei Fragen antworte einfach auf diese E-Mail.

Viel Erfolg beim Lernen!
System Architekt
"""
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

@app.route("/webhook/digistore", methods=["GET", "POST"])
def digistore_webhook():
    """Webhook für Digistore24"""
    if request.method == "GET":
        return "OK", 200

    if not verify_secret(request):
        return "unauthorized", 401

    data = request.form

    event = data.get("event")
    if event in ["payment", "on_payment"]:
        email = data.get("email", "")
        name = data.get("first_name", "Kunde")
        product = data.get("product_id", "standard")

        try:
            code = create_access_code(email, name, product)
            send_email(email, name, code)
        except Exception as e:
            print(f"Error: {e}")

        return "OK", 200

    return "OK", 200

@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    """Webhook für Gumroad"""
    if not verify_secret(request):
        return jsonify({"success": False, "error": "unauthorized"}), 401

    data = request.json or request.form
    
    email = data.get("email", "")
    name = data.get("full_name", "Kunde")
    product = data.get("product_id", "standard")
    
    try:
        code = create_access_code(email, name, product)
        send_email(email, name, code)
        return jsonify({"success": True, "code": code})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
