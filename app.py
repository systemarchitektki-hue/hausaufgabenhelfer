import os
import base64
import locale
import streamlit as st
from openai import OpenAI
from datetime import datetime

try:
    from supabase import create_client, Client  # type: ignore
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    create_client = None  # type: ignore
    Client = None  # type: ignore

st.set_page_config(
    page_title="Hausaufgabenhelfer Pro - System Architekt",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

try:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

VERSION = "1.0.0"
PRODUCT_NAME = "Hausaufgabenhelfer Pro"
BRAND_NAME = "System Architekt"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
LICENSE_REQUIRED = os.getenv("LICENSE_REQUIRED", "true").lower() == "true"

st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4A574 0%, #C4956A 100%);
        color: #0a0a0a;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 165, 116, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 165, 116, 0.5);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 0.75rem;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #D4A574;
        box-shadow: 0 0 10px rgba(212, 165, 116, 0.3);
    }
    .stSelectbox>div>div>div, .stRadio>div {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 8px;
    }
    h1 {
        color: #D4A574;
        font-weight: 700;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        color: #D4A574;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4A574;
        color: #0a0a0a;
        font-weight: 600;
    }
    .product-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(212, 165, 116, 0.1) 0%, rgba(196, 149, 106, 0.05) 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212, 165, 116, 0.3);
    }
    .feature-box {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #333333;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666666;
        font-size: 0.9rem;
        border-top: 1px solid #333333;
        margin-top: 3rem;
    }
    .stSidebar {
        background-color: #0f0f0f;
    }
    .stSidebar [data-testid="stSidebarContent"] {
        background-color: #0f0f0f;
    }
    .login-box {
        background: linear-gradient(135deg, rgba(212, 165, 116, 0.1) 0%, rgba(196, 149, 106, 0.05) 100%);
        border: 1px solid rgba(212, 165, 116, 0.3);
        border-radius: 12px;
        padding: 2rem;
        max-width: 400px;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

def check_license(code: str) -> dict:
    """Prüft Lizenzcode gegen Supabase"""
    if not SUPABASE_AVAILABLE:
        return {"valid": False, "error": "Supabase nicht installiert"}

    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"valid": False, "error": "Lizenzprüfung nicht konfiguriert"}

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        response = supabase.table("access_codes").select("*").eq("code", code).execute()

        if not response.data:
            return {"valid": False, "error": "Ungültiger Zugangscode"}

        license_data = response.data[0]

        if not license_data.get("is_active", True):
            return {"valid": False, "error": "Dieser Code wurde deaktiviert"}

        if license_data.get("expires_at"):
            expires = datetime.fromisoformat(license_data["expires_at"].replace("Z", "+00:00"))
            if expires < datetime.now(expires.tzinfo):
                return {"valid": False, "error": "Dieser Code ist abgelaufen"}

        if not license_data.get("used_at"):
            supabase.table("access_codes").update({
                "used_at": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat()
            }).eq("code", code).execute()
        else:
            supabase.table("access_codes").update({
                "last_used": datetime.now().isoformat()
            }).eq("code", code).execute()

        return {"valid": True, "data": license_data}

    except Exception as e:
        return {"valid": False, "error": f"Verbindungsfehler: {str(e)}"}

if "licensed" not in st.session_state:
    st.session_state.licensed = False
if "license_code" not in st.session_state:
    st.session_state.license_code = None

if LICENSE_REQUIRED and not st.session_state.licensed:
    st.markdown(f"""
    <div class="product-header">
        <h1>📐 {PRODUCT_NAME}</h1>
        <p style="font-size: 1rem; color: #888888; margin-top: 0.5rem;">
            by {BRAND_NAME}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 Zugang erforderlich")
    st.markdown("Bitte geben Sie Ihren Zugangscode ein, um die App zu nutzen.")

    with st.form("license_form"):
        code = st.text_input("Zugangscode", placeholder="XXX-XXX-XXX", type="password")
        submit = st.form_submit_button("Zugang freischalten", type="primary", use_container_width=True)

        if submit:
            if not code.strip():
                st.error("Bitte geben Sie einen Zugangscode ein.")
            else:
                result = check_license(code.strip())
                if result["valid"]:
                    st.session_state.licensed = True
                    st.session_state.license_code = code.strip()
                    st.success("✅ Zugang freigeschaltet!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666666; font-size: 0.9rem;">
        <p>Noch keinen Zugangscode?</p>
        <p>Kontaktieren Sie uns für eine Lizenz.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.markdown(f"""
<div class="product-header">
    <h1>📐 {PRODUCT_NAME}</h1>
    <p style="font-size: 1rem; color: #888888; margin-top: 0.5rem;">
        by {BRAND_NAME}
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Einstellungen")

    klassenstufe = st.selectbox(
        "📚 Klassenstufe",
        ["1–2", "3–4", "5–6", "7–8", "9–10", "11–13"],
        index=2,
    )

    fach = st.selectbox(
        "📖 Fach",
        ["Mathematik", "Deutsch", "Englisch", "Sachkunde", "Physik", "Chemie", "Biologie", "Geschichte", "Geographie", "Informatik", "Sonstiges"],
        index=0,
    )

    antwort_laenge = st.radio(
        "📏 Antwortlänge",
        ["Kurz", "Normal", "Sehr ausführlich"],
        index=1,
    )

    st.markdown("---")

    if LICENSE_REQUIRED and st.session_state.licensed:
        if st.button("🚪 Abmelden", use_container_width=True):
            st.session_state.licensed = False
            st.session_state.license_code = None
            st.rerun()

    st.markdown(f"<p style='color: #666666; font-size: 0.8rem;'>© 2024 {BRAND_NAME}</p>", unsafe_allow_html=True)

if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "⚠️ **OPENAI_API_KEY ist nicht konfiguriert**\n\n"
        "Bitte setzen Sie Ihren OpenAI API-Schlüssel:\n\n"
        "**Lokal (.env Datei):**\n"
        "```\nOPENAI_API_KEY=sk-...\n```\n\n"
        "**Streamlit Cloud:**\n"
        "Settings → Secrets → OPENAI_API_KEY hinzufügen"
    )
    st.stop()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_system_text(klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    laenge_map = {
        "Kurz": "Antworte sehr kurz, aber vollständig. Maximal 5 Schritte.",
        "Normal": "Antworte in klaren, nummerierten Schritten.",
        "Sehr ausführlich": "Antworte sehr ausführlich, mit kleinen Zwischen-Erklärungen und Beispielen.",
    }
    return (
        "Du bist ein professioneller Hausaufgabenhelfer. "
        f"Zielgruppe: Klasse {klassenstufe}. Fach: {fach}. "
        "Erkläre immer Schritt für Schritt in klarem Deutsch. "
        "Schreibe Brüche wie 3/4 oder 5/4, aber benutze KEIN LaTeX, "
        "keine Backslashes und keine Formeln mit \\frac oder ähnlichem. "
        "Formatierung: nur normaler Text mit nummerierten Schritten. "
        + laenge_map.get(antwort_laenge, "")
    )

def build_system_image(klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    return build_system_text(klassenstufe, fach, antwort_laenge) + (
        " Erkenne alle SCHULAUFGABEN im Bild und löse sie Schritt für Schritt. "
        "Falls keine Aufgaben vorhanden sind, sage das klar."
    )

def bytes_to_data_url(file_bytes: bytes, mime: str) -> str:
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def ask_text(question: str, klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_text(klassenstufe, fach, antwort_laenge)},
            {"role": "user", "content": question},
        ],
    )
    content = resp.choices[0].message.content
    return content if content else "Keine Antwort erhalten."

def ask_image(image_bytes: bytes, mime: str, prompt: str, klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    data_url = bytes_to_data_url(image_bytes, mime)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": build_system_image(klassenstufe, fach, antwort_laenge)},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
    )
    content = resp.choices[0].message.content
    return content if content else "Keine Antwort erhalten."

if "history" not in st.session_state:
    st.session_state.history = []

tab1, tab2, tab3 = st.tabs(["💬 Textfrage", "🖼️ Bildanalyse", "📜 Verlauf"])

with tab1:
    st.markdown("### Stellen Sie Ihre Frage")
    st.markdown("Geben Sie Ihre Hausaufgabenfrage ein und erhalten Sie eine detaillierte, schrittweise Erklärung.")
    
    question = st.text_area(
        "Ihre Frage:",
        placeholder="z.B. Erkläre mir 3/4 + 1/2 Schritt für Schritt.",
        height=150,
        help="Formulieren Sie Ihre Frage so präzise wie möglich für die beste Antwort."
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        ask_btn = st.button("🚀 Antwort erstellen", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Löschen", use_container_width=True)

    if clear_btn:
        st.session_state.history = []
        st.success("Verlauf wurde gelöscht!")
        st.rerun()

    if ask_btn:
        if not question.strip():
            st.warning("⚠️ Bitte geben Sie eine Frage ein.")
        else:
            with st.spinner("🤖 KI analysiert Ihre Frage und erstellt eine detaillierte Erklärung..."):
                try:
                    answer = ask_text(question.strip(), klassenstufe, fach, antwort_laenge)
                    st.session_state.history.insert(0, {
                        "type": "Text",
                        "question": question.strip(),
                        "answer": answer,
                        "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "klassenstufe": klassenstufe,
                        "fach": fach
                    })
                    st.success("✅ Antwort erfolgreich erstellt!")
                    st.markdown("### 📝 Antwort")
                    st.markdown(f"<div class='feature-box'>{answer}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Fehler bei der Verarbeitung: {str(e)}")

with tab2:
    st.markdown("### Laden Sie ein Bild Ihrer Aufgabe hoch")
    st.markdown("Die KI erkennt automatisch alle Aufgaben im Bild und löst sie Schritt für Schritt.")
    
    uploaded = st.file_uploader(
        "📸 Bild auswählen",
        type=["jpg", "jpeg", "png"],
        help="Unterstützte Formate: JPG, JPEG, PNG"
    )

    prompt = st.text_input(
        "Zusätzlicher Hinweis (optional)",
        value="Erkenne alle Aufgaben im Bild und löse sie Schritt für Schritt.",
        help="Geben Sie spezifische Anweisungen für die Bildanalyse"
    )

    run_img = st.button("🔍 Bild analysieren", type="primary", use_container_width=True)

    if run_img:
        if uploaded is None:
            st.warning("⚠️ Bitte laden Sie zuerst ein Bild hoch.")
        else:
            mime = uploaded.type or "image/jpeg"
            image_bytes = uploaded.read()

            st.image(image_bytes, caption="📷 Hochgeladenes Bild", use_container_width=True)

            with st.spinner("🔍 Bildanalyse läuft... Dies kann einen Moment dauern."):
                try:
                    answer = ask_image(
                        image_bytes=image_bytes,
                        mime=mime,
                        prompt=prompt.strip() or "Löse die Aufgaben im Bild.",
                        klassenstufe=klassenstufe,
                        fach=fach,
                        antwort_laenge=antwort_laenge,
                    )
                    
                    st.session_state.history.insert(0, {
                        "type": "Bild",
                        "question": "Bildanalyse",
                        "answer": answer,
                        "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "klassenstufe": klassenstufe,
                        "fach": fach
                    })
                    
                    st.success("✅ Bildanalyse abgeschlossen!")
                    st.markdown("### 📝 Ergebnis")
                    st.markdown(f"<div class='feature-box'>{answer}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Fehler bei der Bildanalyse: {str(e)}")

with tab3:
    st.markdown("### Ihr Frageverlauf")
    
    if not st.session_state.history:
        st.info("📭 Noch keine Fragen gestellt. Beginnen Sie in den Tabs 'Textfrage' oder 'Bildanalyse'.")
    else:
        st.markdown(f"**{len(st.session_state.history)} Einträge im Verlauf**")
        
        if st.button("🗑️ Gesamten Verlauf löschen", type="secondary"):
            st.session_state.history = []
            st.rerun()
        
        st.markdown("---")
        
        for idx, entry in enumerate(st.session_state.history):
            with st.expander(f"{'📝' if entry['type'] == 'Text' else '🖼️'} {entry['type']} - {entry['timestamp']} | {entry['fach']} (Klasse {entry['klassenstufe']})"):
                st.markdown(f"**Frage:** {entry['question']}")
                st.markdown("**Antwort:**")
                st.markdown(f"<div class='feature-box'>{entry['answer']}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <p><strong>{PRODUCT_NAME}</strong> - Version {VERSION}</p>
    <p>by {BRAND_NAME}</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        © 2024 {BRAND_NAME} |
        <a href="#" style="color: #D4A574;">Datenschutz</a> |
        <a href="#" style="color: #D4A574;">Nutzungsbedingungen</a> |
        <a href="#" style="color: #D4A574;">Support</a>
    </p>
</div>
""", unsafe_allow_html=True)
