import openai
import os
from dotenv import load_dotenv
import argparse

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Utwórz instancję klienta OpenAI
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def parse_args():
    parser = argparse.ArgumentParser(description="Generowanie artykułu i podglądu HTML.")
    parser.add_argument('--article', default='artykul.txt', help='Ścieżka do pliku z artykułem.')
    parser.add_argument('--output_html', default='artykul.html', help='Ścieżka do pliku HTML artykułu.')
    parser.add_argument('--template', default='szablon.html', help='Ścieżka do szablonu HTML.')
    parser.add_argument('--preview', default='podglad.html', help='Ścieżka do pliku podglądu HTML.')
    return parser.parse_args()

def read_article(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Plik '{file_path}' nie został znaleziony.")
        exit(1)

def generate_html(article_content):
    prompt = (
    "Przekształć poniższy artykuł w czysty kod HTML, przestrzegając dokładnie poniższych wytycznych:\n\n"
    "1. Struktura i Semantyka HTML:\n"
    "   - Użyj odpowiednich tagów HTML do strukturyzacji treści, takich jak:\n"
    "     - <h1> dla głównego tytułu artykułu.\n"
    "     - <h2>, <h3>, itd. dla nagłówków sekcji i podsekcji.\n"
    "     - <p> dla paragrafów tekstu.\n"
    "     - <ul>, <ol> oraz <li> dla list nieuporządkowanych i uporządkowanych.\n"
    "     - <blockquote> dla cytatów.\n"
    "     - <strong> lub <em> dla wyróżnień tekstu.\n\n"
    "2. Grafiki:\n"
    "   - W każdym paragrafie wstaw opis grafiki jaka powinna się tam znajdować, użyj tagu <figure> zawierającego:\n"
    "     - Tag <img> z atrybutem src=\"image_placeholder.jpg\".\n"
    "     - Atrybut alt w tagu <img>, zawierający bardzo dokładny opis który posłuży do wygenerowania grafiki.\n"
    "     - Tag <figcaption> poniżej <img>, zawierający podpis grafiki.\n\n"
    "3. Formatowanie:\n"
    "   - Nie używaj żadnych stylów CSS ani skryptów JavaScript.\n"
    "   - Kod HTML powinien zawierać tylko zawartość między <body> a </body>.\n"
    "   - Zachowaj poprawne wcięcia i formatowanie kodu HTML dla lepszej czytelności.\n\n"
    "4. Przykłady Struktur:\n"
    "   - Tytuł Artykułu:\n"
    "     <h1>Tytuł Artykułu</h1>\n"
    "   - Sekcja z Podtytułem:\n"
    "     <h2>Podtytuł Sekcji</h2>\n"
    "     <p>Treść paragrafu...</p>\n"
    "   - Grafika z Podpisem:\n"
    "     <figure>\n"
    "         <img src=\"image_placeholder.jpg\" alt=\"Opis obrazka do wygenerowania: [dokładny opis]\">\n"
    "         <figcaption>Podpis grafiki</figcaption>\n"
    "     </figure>\n\n"
    "5. Artykuł:\n"
    f"{article_content}\n\n"
    "6. Dodatkowe Wymagania:\n"
    "   - Upewnij się, że cały wygenerowany kod jest zgodny z semantyką HTML5.\n"
    "   - Unikaj duplikacji tagów i zapewnij poprawną hierarchię nagłówków.\n"
    "   - W miejscach, gdzie nie jest wymagana grafika, nie dodawaj tagów <figure> ani <img>.\n\n"
    "Proszę o zwrócenie tylko samego kodu HTML w postaci czystego tekstu bez dodatkowych komentarzy czy wyjaśnień oraz bez pisania ```html i tego ```."
)

    print("Wysyłam zapytanie do OpenAI API...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Jesteś odpowiedzialny za przekształcanie artykułów w czysty kod HTML uwzględniając podane wytyczne."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.2,
        )
        print("Otrzymano odpowiedź od OpenAI.")
    except openai.OpenAIError as e:
        print(f"Error podczas komunikacji z API OpenAI: {e}")
        exit(1)

    html_content = response.choices[0].message.content.strip()
    print("Zwracam wygenerowany kod HTML.")
    return html_content

def save_html(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Plik '{file_path}' został pomyślnie wygenerowany.")
    except IOError as e:
        print(f"Error podczas zapisywania pliku '{file_path}': {e}")
        exit(1)

def create_preview(template_path, content_path, preview_path):
    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()
    except FileNotFoundError:
        print(f"Error: Plik '{template_path}' nie został znaleziony.")
        exit(1)

    try:
        with open(content_path, 'r', encoding='utf-8') as content_file:
            content = content_file.read()
    except FileNotFoundError:
        print(f"Error: Plik '{content_path}' nie został znaleziony.")
        exit(1)

    placeholder = '<!-- Wklej tutaj wygenerowany kod HTML artykułu -->'
    if placeholder not in template:
        print(f"Error: Placeholder '{placeholder}' w szablonie HTML nie został znaleziony.")
        exit(1)

    preview = template.replace(placeholder, content)

    try:
        with open(preview_path, 'w', encoding='utf-8') as preview_file:
            preview_file.write(preview)
        print(f"Plik '{preview_path}' został pomyślnie wygenerowany.")
    except IOError as e:
        print(f"Error podczas zapisywania pliku '{preview_path}': {e}")
        exit(1)

def main():
    args = parse_args()

    # Odczytanie artykułu
    article = read_article(args.article)

    # Generowanie HTML artykułu
    html_code = generate_html(article)
    save_html(html_code, args.output_html)

    # Generowanie podglądu
    create_preview(args.template, args.output_html, args.preview)

if __name__ == "__main__":
    main()
