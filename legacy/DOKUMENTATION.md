# Hausaufgabenhelfer Pro - Produktdokumentation

## 📋 Inhaltsverzeichnis
1. [Produktübersicht](#produktübersicht)
2. [Installation](#installation)
3. [Konfiguration](#konfiguration)
4. [Benutzerhandbuch](#benutzerhandbuch)
5. [Admin-Dashboard](#admin-dashboard)
6. [Deployment](#deployment)
7. [Support](#support)

## 🎓 Produktübersicht

**Hausaufgabenhelfer Pro** ist eine KI-gestützte Web-Anwendung, die Schülern aller Klassenstufen bei ihren Hausaufgaben hilft. Die App nutzt OpenAI's GPT-4 Technologie für:

- ✅ Schritt-für-Schritt Erklärungen
- ✅ Bildanalyse von Aufgaben
- ✅ Alle Klassenstufen (1-13)
- ✅ Alle Hauptfächer
- ✅ Anpassbare Detailtiefe

### Zielgruppe
- Schüler (Klasse 1-13)
- Eltern
- Nachhilfelehrer
- Bildungseinrichtungen

### Technologie-Stack
- **Frontend:** Streamlit
- **KI-Engine:** OpenAI GPT-4o-mini
- **Backend:** Supabase (optional für Lizenzverwaltung)
- **Sprache:** Python 3.11+

## 🚀 Installation

### Voraussetzungen
- Python 3.11 oder höher
- OpenAI API-Schlüssel
- (Optional) Supabase Account für Lizenzverwaltung

### Schritt 1: Repository klonen
```bash
git clone https://github.com/IhrUsername/hausaufgabenhelfer.git
cd hausaufgabenhelfer
```

### Schritt 2: Virtuelle Umgebung erstellen
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### Schritt 3: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Schritt 4: Umgebungsvariablen konfigurieren
Erstellen Sie eine `.env` Datei:
```env
OPENAI_API_KEY=sk-your-api-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
ADMIN_PASSWORD=ihr-sicheres-passwort
```

### Schritt 5: App starten
```bash
streamlit run app.py
```

Die App ist nun unter `http://localhost:8501` erreichbar.

## ⚙️ Konfiguration

### OpenAI API-Schlüssel
1. Registrieren Sie sich bei [OpenAI](https://platform.openai.com/)
2. Erstellen Sie einen API-Schlüssel
3. Fügen Sie den Schlüssel in die `.env` Datei ein

### Supabase Setup (Optional)
Für Lizenzverwaltung:

1. Erstellen Sie ein Projekt auf [Supabase](https://supabase.com/)
2. Erstellen Sie eine Tabelle `access_codes`:

```sql
CREATE TABLE access_codes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  license_type TEXT DEFAULT 'Standard',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  used_at TIMESTAMP,
  user_email TEXT
);
```

3. Tragen Sie URL und **Service-Role-Key** in `.env` ein (kein Anon-Key, da Lizenzdaten nicht öffentlich sein sollen)

## 📖 Benutzerhandbuch

### Textfragen stellen

1. Wählen Sie in der Sidebar:
   - **Klassenstufe** (1-2 bis 11-13)
   - **Fach** (Mathematik, Deutsch, etc.)
   - **Antwortlänge** (Kurz, Normal, Sehr ausführlich)

2. Geben Sie Ihre Frage im Tab "Textfrage" ein
3. Klicken Sie auf "Antwort erstellen"
4. Die KI erstellt eine schrittweise Erklärung

**Beispielfragen:**
- "Erkläre mir 3/4 + 1/2 Schritt für Schritt"
- "Was ist Photosynthese?"
- "Wie konjugiere ich 'to be' im Present Perfect?"

### Bildanalyse

1. Wechseln Sie zum Tab "Bildanalyse"
2. Laden Sie ein Foto Ihrer Aufgabe hoch (JPG/PNG)
3. Optional: Geben Sie zusätzliche Hinweise ein
4. Klicken Sie auf "Bild analysieren"
5. Die KI erkennt und löst alle Aufgaben im Bild

**Tipps für beste Ergebnisse:**
- Gute Beleuchtung
- Klare, lesbare Schrift
- Vollständige Aufgabenstellung sichtbar
- Keine Schatten oder Reflexionen

### Verlauf

Im Tab "Verlauf" finden Sie alle bisherigen Fragen und Antworten:
- Chronologische Auflistung
- Filter nach Typ (Text/Bild)
- Zeitstempel und Metadaten
- Löschfunktion

## 🔐 Admin-Dashboard

### Zugriff
```bash
streamlit run admin.py
```

Login mit dem in `.env` konfigurierten `ADMIN_PASSWORD`.

### Funktionen

#### Zugangscodes generieren
1. Wählen Sie Anzahl und Lizenztyp
2. Klicken Sie auf "Codes generieren"
3. Codes werden in Supabase gespeichert
4. Kopieren Sie die Codes für den Verkauf

#### Code-Verwaltung
- Übersicht aller Codes
- Status (Aktiv/Inaktiv)
- Verwendungsdatum
- Löschen von Codes

#### Statistiken
- Gesamtanzahl Codes
- Aktive Codes
- Verwendete Codes
- Nutzungsanalysen

## 🌐 Deployment

### Streamlit Cloud

1. Pushen Sie Ihr Repository zu GitHub
2. Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
3. Verbinden Sie Ihr Repository
4. Konfigurieren Sie Secrets:
   ```toml
   OPENAI_API_KEY = "sk-..."
   SUPABASE_URL = "https://..."
    SUPABASE_SERVICE_ROLE_KEY = "..."
   ADMIN_PASSWORD = "..."
   ```
5. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build und Run:
```bash
docker build -t hausaufgabenhelfer .
docker run -p 8501:8501 --env-file .env hausaufgabenhelfer
```

### Heroku

1. Erstellen Sie `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy:
```bash
heroku create ihr-app-name
git push heroku main
heroku config:set OPENAI_API_KEY=sk-...
```

### Azure App Service

1. Erstellen Sie `startup.sh`:
```bash
#!/bin/bash
streamlit run app.py --server.port=8000 --server.address=0.0.0.0
```

2. Deploy via Azure CLI:
```bash
az webapp up --name hausaufgabenhelfer --runtime "PYTHON:3.11"
```

## 📞 Support

### Häufige Probleme

**Problem:** "OPENAI_API_KEY ist nicht gesetzt"
- **Lösung:** Überprüfen Sie die `.env` Datei oder Streamlit Secrets

**Problem:** Bildanalyse funktioniert nicht
- **Lösung:** Stellen Sie sicher, dass das Bild klar und lesbar ist

**Problem:** Langsame Antworten
- **Lösung:** OpenAI API kann bei hoher Last langsamer sein

### Kontakt
- **Email:** support@hausaufgabenhelfer.de
- **Website:** www.hausaufgabenhelfer.de
- **GitHub:** github.com/IhrUsername/hausaufgabenhelfer

## 📄 Lizenz

© 2024 Hausaufgabenhelfer Pro. Alle Rechte vorbehalten.

Dieses Produkt ist lizenziert für den kommerziellen Verkauf.
