import os
import base64
from openai import OpenAI

# OpenAI-Client erstellen – nutzt deinen gespeicherten API-Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Optional aber empfohlen: Früh prüfen, ob der Key da ist
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY ist nicht gesetzt. "
        "Setze ihn in den Umgebungsvariablen und starte VS Code danach neu."
    )


def modus_waehlen():
    print("\nWas möchtest du machen?")
    print("  (t) Textfrage stellen")
    print("  (b) Bild analysieren")
    print("  (q) Programm beenden")

    return input("Bitte t, b oder q eingeben: ").lower().strip()


def frage_eingeben():
    return input("Welche Frage soll beantwortet werden? ").strip()


def frage_verarbeiten(frage: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein freundlicher, kindgerechter Hausaufgabenhelfer. "
                    "Erkläre immer Schritt für Schritt in einfachem Deutsch. "
                    "Schreibe Brüche wie 3/4 oder 5/4, aber benutze KEIN LaTeX, "
                    "keine Backslashes und keine Formeln mit \\frac oder ähnlichem. "
                    "Formatierung: nur normaler Text mit nummerierten Schritten."
                ),
            },
            {"role": "user", "content": frage},
        ],
    )
    return response.choices[0].message.content


def antwort_ausgeben(antwort: str):
    print("\nAntwort der App:")
    print(antwort)


def bild_als_data_url(dateipfad: str) -> str:
    ext = os.path.splitext(dateipfad.lower())[1]
    mime = "image/jpeg"
    if ext == ".png":
        mime = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        # Fallback (meist ok)
        mime = "image/jpeg"

    with open(dateipfad, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{b64}"


def bild_verarbeiten(dateipfad: str) -> str:
    if not os.path.isfile(dateipfad):
        raise FileNotFoundError(f"Datei nicht gefunden: {dateipfad}")

    data_url = bild_als_data_url(dateipfad)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein freundlicher, kindgerechter Hausaufgabenhelfer. "
                    "Analysiere das Bild, erkenne alle Aufgaben darauf und erkläre Schritt für Schritt, "
                    "wie man sie löst. Benutze KEIN LaTeX und schreibe alles in einfachem Deutsch. "
                    "Formatierung: nur normaler Text mit nummerierten Schritten."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bitte analysiere dieses Bild und erkläre die Aufgaben."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
    )

    return response.choices[0].message.content


def main():
    print("Hausaufgabenhelfer (Konsole) gestartet.")

    while True:
        modus = modus_waehlen()

        if modus in ["q", "quit", "exit"]:
            print("\nProgramm beendet. Bis zum nächsten Mal!")
            break

        if modus == "t":
            frage = frage_eingeben()
            if frage.lower() in ["stop", "exit", "ende", "quit"]:
                print("\nProgramm beendet. Bis zum nächsten Mal!")
                break

            antwort = frage_verarbeiten(frage)
            antwort_ausgeben(antwort)

        elif modus == "b":
            dateipfad = input(
                "\nBitte den Bildpfad eingeben (z.B. C:\\Users\\Stefan\\Desktop\\blatt.jpg): "
            ).strip().strip('"')

            try:
                antwort = bild_verarbeiten(dateipfad)
                antwort_ausgeben(antwort)

            except FileNotFoundError:
                print("\nFehler: Datei nicht gefunden. Bitte prüfe den Pfad.")

            except Exception as e:
                print("\nEs ist ein Fehler aufgetreten:")
                print(e)

        else:
            print("\nUngültige Eingabe, bitte t, b oder q verwenden.\n")


if __name__ == "__main__":
    main()
