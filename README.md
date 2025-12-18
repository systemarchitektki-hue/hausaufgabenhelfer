# Hausaufgabenhelfer Pro

![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-Commercial-orange)
![AI](https://img.shields.io/badge/AI-GPT--4-purple)

## 🎓 Professionelle KI-gestützte Lernhilfe

**Hausaufgabenhelfer Pro** ist eine moderne Web-Anwendung, die Schülern aller Klassenstufen bei ihren Hausaufgaben hilft. Powered by OpenAI's GPT-4 Technologie.

![Hausaufgabenhelfer Pro](Produktfoto%20Hausaufgabenhelfer_Tentary.png)

## ✨ Features

- 🤖 **KI-gestützte Erklärungen** - Schritt-für-Schritt Lösungen mit GPT-4
- 📸 **Bildanalyse** - Fotografieren Sie Aufgaben und erhalten Sie sofortige Lösungen
- 📚 **Alle Klassenstufen** - Von Grundschule bis Abitur (Klasse 1-13)
- 📖 **Alle Hauptfächer** - Mathematik, Deutsch, Englisch, Physik, Chemie, Biologie, Geschichte, etc.
- 🎯 **Anpassbare Detailtiefe** - Kurze, normale oder sehr ausführliche Erklärungen
- 📜 **Verlaufsfunktion** - Alle Fragen und Antworten werden gespeichert
- 🎨 **Modernes Design** - Benutzerfreundliche Oberfläche mit Dark Mode
- 🔐 **Admin-Dashboard** - Lizenzverwaltung und Statistiken
- 🌐 **Multi-Platform** - Funktioniert auf PC, Tablet und Smartphone

## 🚀 Quick Start

### Voraussetzungen

- Python 3.11 oder höher
- OpenAI API-Schlüssel
- (Optional) Supabase Account für Lizenzverwaltung

### Installation

```bash
# Repository klonen
git clone https://github.com/IhrUsername/hausaufgabenhelfer.git
cd hausaufgabenhelfer

# Virtuelle Umgebung erstellen
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeiten Sie .env und fügen Sie Ihre API-Keys ein

# App starten
streamlit run app.py
```

Die App ist nun unter `http://localhost:8501` erreichbar.

## 📦 Projektstruktur

```
hausaufgabenhelfer/
├── app.py                  # Hauptanwendung
├── admin.py                # Admin-Dashboard
├── requirements.txt        # Python-Abhängigkeiten
├── .env                    # Umgebungsvariablen (nicht im Repo)
├── .env.example            # Beispiel für Umgebungsvariablen
├── Dockerfile              # Docker-Container
├── docker-compose.yml      # Docker Compose Konfiguration
├── Procfile                # Heroku Deployment
├── startup.sh              # Azure/Linux Startup-Script
├── .streamlit/
│   └── config.toml         # Streamlit-Konfiguration
├── supabase/
│   ├── config.toml         # Supabase-Konfiguration
│   └── functions/          # Edge Functions
├── DOKUMENTATION.md        # Vollständige Dokumentation
├── MARKETING.md            # Marketing-Materialien
└── README.md               # Diese Datei
```

## 🔧 Konfiguration

### Umgebungsvariablen

Erstellen Sie eine `.env` Datei im Projektverzeichnis:

```env
# OpenAI API
OPENAI_API_KEY=sk-your-api-key-here

# Supabase (Optional für Lizenzverwaltung)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Admin-Dashboard
ADMIN_PASSWORD=ihr-sicheres-passwort
```

### Supabase Setup (Optional)

Für die Lizenzverwaltung benötigen Sie eine Supabase-Datenbank:

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

## 🌐 Deployment

### Streamlit Cloud

1. Pushen Sie Ihr Repository zu GitHub
2. Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
3. Verbinden Sie Ihr Repository
4. Konfigurieren Sie Secrets in den App-Einstellungen
5. Deploy!

### Docker

```bash
# Image bauen
docker build -t hausaufgabenhelfer .

# Container starten
docker run -p 8501:8501 --env-file .env hausaufgabenhelfer

# Oder mit Docker Compose
docker-compose up -d
```

### Heroku

```bash
# Heroku App erstellen
heroku create ihr-app-name

# Umgebungsvariablen setzen
heroku config:set OPENAI_API_KEY=sk-...

# Deployen
git push heroku main
```

### Azure App Service

```bash
# Azure CLI Login
az login

# Web App erstellen und deployen
az webapp up --name hausaufgabenhelfer --runtime "PYTHON:3.11"

# Umgebungsvariablen setzen
az webapp config appsettings set --name hausaufgabenhelfer --settings OPENAI_API_KEY=sk-...
```

## 📖 Verwendung

### Textfragen

1. Wählen Sie Klassenstufe, Fach und Antwortlänge in der Sidebar
2. Geben Sie Ihre Frage im Tab "Textfrage" ein
3. Klicken Sie auf "Antwort erstellen"
4. Erhalten Sie eine detaillierte, schrittweise Erklärung

### Bildanalyse

1. Wechseln Sie zum Tab "Bildanalyse"
2. Laden Sie ein Foto Ihrer Aufgabe hoch (JPG/PNG)
3. Optional: Geben Sie zusätzliche Hinweise ein
4. Klicken Sie auf "Bild analysieren"
5. Die KI erkennt und löst alle Aufgaben im Bild

### Admin-Dashboard

```bash
streamlit run admin.py
```

Verwalten Sie Zugangscodes, Lizenzen und Statistiken.

## 🛠️ Technologie-Stack

- **Frontend:** Streamlit 1.29+
- **KI-Engine:** OpenAI GPT-4o-mini
- **Backend:** Supabase (optional)
- **Sprache:** Python 3.11+
- **Deployment:** Docker, Heroku, Azure, Streamlit Cloud

## 📊 Lizenzmodelle

### Standard-Lizenz - 299€
- Vollständige Web-App
- Dokumentation
- E-Mail Support (30 Tage)
- Updates (6 Monate)

### Premium-Lizenz - 499€
- Alles aus Standard
- Admin-Dashboard
- Prioritäts-Support (90 Tage)
- Updates (12 Monate)
- Anpassungsberatung (2 Stunden)

### Enterprise-Lizenz - 999€
- Alles aus Premium
- White-Label Option
- Unbegrenzter Support
- Lebenslange Updates
- Individuelle Anpassungen (5 Stunden)
- Deployment-Unterstützung

## 📚 Dokumentation

- [Vollständige Dokumentation](DOKUMENTATION.md)
- [Marketing-Materialien](MARKETING.md)
- [API-Dokumentation](https://platform.openai.com/docs)
- [Streamlit-Dokumentation](https://docs.streamlit.io)

## 🤝 Support

- **E-Mail:** support@hausaufgabenhelfer.de
- **Website:** www.hausaufgabenhelfer.de
- **GitHub Issues:** [Issues](https://github.com/IhrUsername/hausaufgabenhelfer/issues)

## 🔒 Sicherheit

- Alle API-Schlüssel werden sicher in Umgebungsvariablen gespeichert
- Keine Speicherung sensibler Daten ohne Zustimmung
- HTTPS-Verschlüsselung bei Deployment
- Regelmäßige Sicherheitsupdates

## 📈 Roadmap

- [ ] Multi-Sprachen Support (Englisch, Französisch, Spanisch)
- [ ] Spracherkennung für mündliche Fragen
- [ ] Erweiterte Statistiken und Analytics
- [ ] Mobile Apps (iOS/Android)
- [ ] Integration mit Lernplattformen (Moodle, etc.)
- [ ] Gamification-Elemente
- [ ] Lehrer-Dashboard

## 🙏 Credits

- **KI-Technologie:** OpenAI GPT-4
- **Framework:** Streamlit
- **Backend:** Supabase
- **Icons:** Emoji

## 📄 Lizenz

© 2024 Hausaufgabenhelfer Pro. Alle Rechte vorbehalten.

Dieses Produkt ist für den kommerziellen Verkauf lizenziert. Käufer erhalten das Recht zur Nutzung und zum Weiterverkauf gemäß der erworbenen Lizenz.

## 🌟 Testimonials

> "Der Hausaufgabenhelfer hat meinem Sohn enorm geholfen. Die Erklärungen sind klar und verständlich!"
> - Sandra M., Mutter von zwei Kindern

> "Als Nachhilfelehrer nutze ich das Tool täglich. Es spart mir Stunden an Vorbereitungszeit."
> - Michael K., Nachhilfelehrer

> "Perfekt für mein EdTech-Startup. Die White-Label Option war genau das, was ich brauchte."
> - Lisa T., Unternehmerin

---

**Entwickelt mit ❤️ für besseres Lernen**

[Website](https://hausaufgabenhelfer.de) | [Demo](https://demo.hausaufgabenhelfer.de) | [Kaufen](https://shop.hausaufgabenhelfer.de)
