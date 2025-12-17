import os
import base64
import locale
import streamlit as st
from openai import OpenAI

# ---------------------------------
# Streamlit Config (muss sehr früh kommen)
# ---------------------------------
st.set_page_config(page_title="Hausaufgabenhelfer", page_icon="🎓", layout="centered")

# ---------------------------------
# Locale (optional)
# ---------------------------------
try:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
except Exception:
    pass

# Optional: API-Key via .env laden (lokal)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ---------------------------------
# Custom CSS für Dark Mode mit Neon Accents
# ---------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0a0e27;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #1a1f3a;
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 4px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #00ff88;
        color: #0a0e27;
        border: 1px solid #00ff88;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1f3a;
        color: #e0e0e0;
        border: 1px solid #2a3f5f;
    }
    .stSelectbox>div>div>div, .stRadio>div {
        background-color: #1a1f3a;
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #00ff88;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1f3a;
    }
    .stTabs [data-baseweb="tab"] {
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        color: #00ff88;
        border-bottom-color: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Header
# ---------------------------------
st.title("Hausaufgabenhelfer")
st.markdown(
    "Professionelle Unterstützung für Ihre schulischen Aufgaben. "
    "Wählen Sie die gewünschten Parameter für eine präzise Erklärung."
)

# ---------------------------------
# API Key Check
# ---------------------------------
if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY ist nicht gesetzt.\n\n"
        "Option A (Windows): setx OPENAI_API_KEY \"IHR_KEY\" und VS Code neu starten.\n"
        "Option B (.env): Legen Sie eine Datei .env im Projektordner an mit:\n"
        "OPENAI_API_KEY=IHR_KEY\n\n"
        "In Streamlit Cloud: Settings → Secrets → OPENAI_API_KEY setzen."
    )
    st.stop()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------
# Prompt Builder
# ---------------------------------
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

# ---------------------------------
# OpenAI Calls
# ---------------------------------
def ask_text(question: str, klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_text(klassenstufe, fach, antwort_laenge)},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content

def ask_image(image_bytes: bytes, mime: str, prompt: str, klassenstufe: str, fach: str, antwort_laenge: str) -> str:
    data_url = bytes_to_data_url(image_bytes, mime)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
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
    return resp.choices[0].message.content

# ---------------------------------
# UI Controls
# ---------------------------------
colA, colB = st.columns(2)
with colA:
    klassenstufe = st.selectbox(
        "Klassenstufe",
        ["1–2", "3–4", "5–6", "7–8", "9–10", "11–13"],
        index=1,
    )
with colB:
    fach = st.selectbox(
        "Fach",
        ["Mathe", "Deutsch", "Englisch", "Sachkunde", "Physik", "Chemie", "Biologie", "Geschichte", "Sonstiges"],
        index=0,
    )

antwort_laenge = st.radio(
    "Antwortlänge",
    ["Kurz", "Normal", "Sehr ausführlich"],
    horizontal=True,
    index=1,
)

# Session-State für Verlauf
if "history" not in st.session_state:
    st.session_state.history = []

tab1, tab2 = st.tabs(["Textfrage", "Bildanalyse"])

# ---------------------------------
# Tab 1: Textfrage
# ---------------------------------
with tab1:
    st.subheader("Textfrage stellen")
    question = st.text_area(
        "Ihre Frage:",
        placeholder="z.B. Erkläre mir 3/4 + 1/2 Schritt für Schritt.",
        height=120,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        ask_btn = st.button("Antwort erstellen", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("Verlauf löschen", use_container_width=True)

    if clear_btn:
        st.session_state.history = []
        st.rerun()

    if ask_btn:
        if not question.strip():
            st.warning("Bitte geben Sie eine Frage ein.")
        else:
            with st.spinner("Ich analysiere Ihre Frage und erstelle eine detaillierte Erklärung …"):
                answer = ask_text(question.strip(), klassenstufe, fach, antwort_laenge)
            st.session_state.history.insert(0, ("Text", question.strip(), answer))

# ---------------------------------
# Tab 2: Bildanalyse
# ---------------------------------
with tab2:
    st.subheader("Bild hochladen und Aufgaben lösen")
    uploaded = st.file_uploader("Bild auswählen (JPG/PNG)", type=["jpg", "jpeg", "png"])

    prompt = st.text_input(
        "Hinweis an die KI (optional)",
        value="Erkenne alle Aufgaben im Bild und löse sie Schritt für Schritt.",
    )

    run_img = st.button("Bild analysieren", type="primary", use_container_width=True)

    if run_img:
        if uploaded is None:
            st.warning("Bitte laden Sie zuerst ein Bild hoch.")
        else:
            mime = uploaded.type or "image/jpeg"
            image_bytes = uploaded.read()

            st.image(image_bytes, caption="Hochgeladenes Bild", use_container_width=True)

            with st.spinner("Bildanalyse läuft..."):
                answer = ask_image(
                    image_bytes=image_bytes,
                    mime=mime,
                    prompt=prompt.strip() or "Löse die Aufgaben im Bild.",
                    klassenstufe=klassenstufe,
                    fach=fach,
                    antwort_laenge=antwort_laenge,
                )

            st.markdown("### Ergebnis")
            st.write(answer)
