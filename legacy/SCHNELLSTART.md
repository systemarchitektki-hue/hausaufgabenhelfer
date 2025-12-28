# Hausaufgabenhelfer Pro - Schnellstart-Anleitung

## 🚀 In 5 Minuten einsatzbereit!

### Schritt 1: Dateien entpacken
Entpacken Sie das heruntergeladene ZIP-Archiv in einen Ordner Ihrer Wahl.

### Schritt 2: Python installieren (falls noch nicht vorhanden)
- Laden Sie Python 3.11 oder höher von [python.org](https://www.python.org/downloads/) herunter
- Installieren Sie Python (Wichtig: "Add Python to PATH" aktivieren!)

### Schritt 3: Terminal/Eingabeaufforderung öffnen
**Windows:**
- Drücken Sie `Windows + R`
- Geben Sie `cmd` ein und drücken Sie Enter
- Navigieren Sie zum Projektordner: `cd C:\Pfad\zum\hausaufgabenhelfer`

**Mac/Linux:**
- Öffnen Sie das Terminal
- Navigieren Sie zum Projektordner: `cd /pfad/zum/hausaufgabenhelfer`

### Schritt 4: Virtuelle Umgebung erstellen und aktivieren

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sie sollten nun `(.venv)` vor Ihrer Eingabeaufforderung sehen.

### Schritt 5: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

Dies dauert 1-2 Minuten. Warten Sie, bis die Installation abgeschlossen ist.

### Schritt 6: OpenAI API-Schlüssel einrichten

1. Gehen Sie zu [platform.openai.com](https://platform.openai.com/)
2. Registrieren Sie sich oder melden Sie sich an
3. Gehen Sie zu "API Keys" und erstellen Sie einen neuen Schlüssel
4. Kopieren Sie den Schlüssel (beginnt mit `sk-...`)

5. Erstellen Sie eine `.env` Datei im Projektordner:
   - Kopieren Sie `.env.example` und benennen Sie die Kopie in `.env` um
   - Öffnen Sie `.env` mit einem Texteditor (z.B. Notepad)
   - Ersetzen Sie `sk-your-openai-api-key-here` mit Ihrem echten API-Schlüssel
   - Speichern Sie die Datei

**Beispiel .env Datei:**
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...
ADMIN_PASSWORD=MeinSicheresPasswort123
```

### Schritt 7: App starten
```bash
streamlit run app.py
```

Die App öffnet sich automatisch in Ihrem Browser unter `http://localhost:8501`

**Falls sich der Browser nicht automatisch öffnet:**
- Öffnen Sie manuell: `http://localhost:8501`

### Schritt 8: Erste Schritte in der App

1. **Einstellungen wählen** (linke Sidebar):
   - Klassenstufe: z.B. "5-6"
   - Fach: z.B. "Mathematik"
   - Antwortlänge: z.B. "Normal"

2. **Textfrage stellen**:
   - Wechseln Sie zum Tab "Textfrage"
   - Geben Sie eine Frage ein: "Erkläre mir 3/4 + 1/2"
   - Klicken Sie auf "Antwort erstellen"
   - Warten Sie 5-10 Sekunden auf die Antwort

3. **Bildanalyse testen**:
   - Wechseln Sie zum Tab "Bildanalyse"
   - Laden Sie ein Foto einer Hausaufgabe hoch
   - Klicken Sie auf "Bild analysieren"
   - Die KI erkennt und löst die Aufgaben

### Schritt 9: Admin-Dashboard (Optional)

Öffnen Sie ein neues Terminal/Eingabeaufforderung:

```bash
cd C:\Pfad\zum\hausaufgabenhelfer
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
streamlit run admin.py
```

Login mit dem Passwort aus Ihrer `.env` Datei.

---

## ❓ Häufige Probleme und Lösungen

### Problem: "python ist nicht als interner oder externer Befehl erkannt"
**Lösung:** Python ist nicht im PATH. Installieren Sie Python neu und aktivieren Sie "Add Python to PATH".

### Problem: "OPENAI_API_KEY ist nicht gesetzt"
**Lösung:** 
1. Überprüfen Sie, ob die `.env` Datei existiert
2. Überprüfen Sie, ob der API-Key korrekt eingetragen ist
3. Starten Sie die App neu

### Problem: "ModuleNotFoundError: No module named 'streamlit'"
**Lösung:** 
1. Stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist (Sie sollten `(.venv)` sehen)
2. Führen Sie erneut aus: `pip install -r requirements.txt`

### Problem: App lädt sehr langsam
**Lösung:** 
- OpenAI API kann bei hoher Last langsamer sein
- Überprüfen Sie Ihre Internetverbindung
- Warten Sie 30-60 Sekunden

### Problem: Bildanalyse funktioniert nicht
**Lösung:**
- Stellen Sie sicher, dass das Bild klar und lesbar ist
- Unterstützte Formate: JPG, JPEG, PNG
- Maximale Dateigröße: 10 MB

### Problem: "Port 8501 is already in use"
**Lösung:**
- Eine andere Streamlit-App läuft bereits
- Schließen Sie alle anderen Streamlit-Apps
- Oder verwenden Sie einen anderen Port: `streamlit run app.py --server.port=8502`

---

## 💡 Tipps für beste Ergebnisse

1. **Präzise Fragen stellen**
   - Gut: "Erkläre mir Schritt für Schritt, wie ich 3/4 + 1/2 rechne"
   - Schlecht: "Mathe"

2. **Klassenstufe anpassen**
   - Die KI passt die Erklärungen an die gewählte Klassenstufe an
   - Wählen Sie die richtige Stufe für optimale Ergebnisse

3. **Antwortlänge wählen**
   - "Kurz": Schnelle Antworten, weniger Details
   - "Normal": Ausgewogene Erklärungen (empfohlen)
   - "Sehr ausführlich": Detaillierte Erklärungen mit Beispielen

4. **Gute Fotos machen**
   - Gute Beleuchtung
   - Klare, lesbare Schrift
   - Keine Schatten oder Reflexionen
   - Vollständige Aufgabenstellung sichtbar

5. **Verlauf nutzen**
   - Alle Fragen werden im Tab "Verlauf" gespeichert
   - Perfekt zum Nachschlagen und Wiederholen

---

## 📞 Support

Bei weiteren Fragen:
- **E-Mail:** support@hausaufgabenhelfer.de
- **Dokumentation:** Siehe `DOKUMENTATION.md`
- **FAQ:** Siehe `README.md`

---

## 🎉 Viel Erfolg!

Sie sind jetzt bereit, den Hausaufgabenhelfer Pro zu nutzen!

**Nächste Schritte:**
- [ ] Erste Testfrage stellen
- [ ] Bildanalyse ausprobieren
- [ ] Admin-Dashboard erkunden (optional)
- [ ] Dokumentation lesen für erweiterte Features
- [ ] Bei Gefallen: Bewertung hinterlassen ⭐

---

© 2024 Hausaufgabenhelfer Pro
