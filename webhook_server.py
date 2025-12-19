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
from flask import Flask, request, jsonify
from supabase import create_client
from datetime import datetime, timedelta

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dein-geheimer-key")

def generate_code():
    """Generiert einen zufälligen Zugangscode"""
    chars = string.ascii_uppercase + string.digits
    return f"{''.join(secrets.choice(chars) for _ in range(4))}-{''.join(secrets.choice(chars) for _ in range(4))}-{''.join(secrets.choice(chars) for _ in range(4))}"

def create_access_code(email: str, name: str, product: str = "standard"):
    """Erstellt Zugangscode in Supabase"""
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    code = generate_code()
    
    expires = None
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

def send_email(to_email: str, name: str, code: str):
    """Sendet Zugangscode per E-Mail"""
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

@app.route("/webhook/digistore", methods=["POST"])
def digistore_webhook():
    """Webhook für Digistore24"""
    data = request.form
    
    if data.get("sha_sign") != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid signature"}), 401
    
    event = data.get("event")
    if event == "payment":
        email = data.get("email")
        name = data.get("first_name", "Kunde")
        product = data.get("product_id", "standard")
        
        code = create_access_code(email, name, product)
        send_email(email, name, code)
        
        return jsonify({"success": True, "code": code})
    
    return jsonify({"success": True})

@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    """Webhook für Gumroad"""
    data = request.json or request.form
    
    email = data.get("email")
    name = data.get("full_name", "Kunde")
    product = data.get("product_id", "standard")
    
    code = create_access_code(email, name, product)
    send_email(email, name, code)
    
    return jsonify({"success": True, "code": code})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
