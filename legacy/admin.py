import os
import secrets
import string
import streamlit as st
from supabase import create_client, Client
from datetime import datetime

st.set_page_config(
    page_title="Hausaufgabenhelfer Pro - Admin Dashboard",
    page_icon="🔐",
    layout="wide"
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
MAX_LOGIN_ATTEMPTS = int(os.getenv("ADMIN_MAX_LOGIN_ATTEMPTS", "5"))

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase-Konfiguration fehlt. Bitte SUPABASE_URL und SUPABASE_SERVICE_ROLE_KEY in .env setzen.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

WEAK_PASSWORDS = {"admin123", "password", "changeme", "123456"}
if ADMIN_PASSWORD in WEAK_PASSWORDS:
    st.error("⚠️ ADMIN_PASSWORD ist zu schwach. Bitte in .env auf ein starkes, einzigartiges Passwort setzen.")
    st.stop()

def generate_secure_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    raw = "".join(secrets.choice(alphabet) for _ in range(12))
    return "-".join([raw[i:i+4] for i in range(0, len(raw), 4)])

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #00ff88;
    }
    .metric-card {
        background-color: #1a1f3a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2a3f5f;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
        color: #0a0e27;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if not st.session_state.authenticated:
    st.title("🔐 Admin Login")
    password = st.text_input("Passwort", type="password")
    if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
        st.error("Zu viele Fehlversuche. Bitte später erneut versuchen.")
        st.stop()

    if st.button("Anmelden"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.session_state.login_attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
            msg = "❌ Falsches Passwort"
            if remaining > 0:
                msg += f" ({remaining} Versuch(e) übrig)"
            else:
                msg += " (gesperrt)"
            st.error(msg)
    st.stop()

st.title("🎓 Hausaufgabenhelfer Pro - Admin Dashboard")

tab1, tab2, tab3 = st.tabs(["📊 Übersicht", "🔑 Zugangscodes", "📈 Statistiken"])

with tab1:
    st.header("Dashboard Übersicht")
    
    try:
        response = supabase.table("access_codes").select("*").execute()
        codes = response.data
        
        total_codes = len(codes)
        active_codes = len([c for c in codes if c.get("is_active", True)])
        used_codes = len([c for c in codes if c.get("used_at")])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{total_codes}</h2>
                <p>Gesamt Codes</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{active_codes}</h2>
                <p>Aktive Codes</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{used_codes}</h2>
                <p>Verwendete Codes</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {str(e)}")

with tab2:
    st.header("Zugangscodes verwalten")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Neuen Code erstellen")
        num_codes = st.number_input("Anzahl Codes", min_value=1, max_value=100, value=1)
        license_type = st.selectbox("Lizenztyp", ["Standard", "Premium", "Enterprise"])
        
        if st.button("Codes generieren", type="primary"):
            try:
                new_codes = []
                for _ in range(num_codes):
                    code = generate_secure_code()
                    new_codes.append({
                        "code": code,
                        "license_type": license_type,
                        "is_active": True,
                        "created_at": datetime.now().isoformat()
                    })
                
                supabase.table("access_codes").insert(new_codes).execute()
                st.success(f"✅ {num_codes} Code(s) erfolgreich erstellt!")
                
                for code_data in new_codes:
                    st.code(code_data["code"])
            except Exception as e:
                st.error(f"Fehler: {str(e)}")
    
    with col2:
        st.subheader("Code-Statistiken")
        st.metric("Heute erstellt", "0")
        st.metric("Diese Woche", "0")
    
    st.markdown("---")
    st.subheader("Alle Zugangscodes")
    
    try:
        response = supabase.table("access_codes").select("*").order("created_at", desc=True).execute()
        codes = response.data
        
        if codes:
            for code in codes[:20]:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.text(code.get("code", "N/A"))
                with col2:
                    st.text(code.get("license_type", "Standard"))
                with col3:
                    status = "✅ Aktiv" if code.get("is_active", True) else "❌ Inaktiv"
                    st.text(status)
                with col4:
                    if st.button("🗑️", key=f"del_{code.get('id')}"):
                        supabase.table("access_codes").delete().eq("id", code.get("id")).execute()
                        st.rerun()
        else:
            st.info("Noch keine Codes vorhanden.")
    except Exception as e:
        st.error(f"Fehler: {str(e)}")

with tab3:
    st.header("Nutzungsstatistiken")
    st.info("Statistiken werden in einer zukünftigen Version verfügbar sein.")

if st.sidebar.button("🚪 Abmelden"):
    st.session_state.authenticated = False
    st.rerun()
