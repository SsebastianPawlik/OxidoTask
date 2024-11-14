# OxidoTask
Aplikacja do generowania kodu HTML artykułu z wykorzystaniem OpenAI API
Opis projektu
Aplikacja generuje kod HTML na podstawie dostarczonego artykułu tekstowego, strukturyzując treść przy użyciu odpowiednich tagów HTML. Do generowania treści HTML używane jest API OpenAI. Aplikacja umożliwia również wygenerowanie podglądu artykułu w formie HTML na podstawie dostarczonego szablonu.

Funkcjonalności
Odczyt artykułu z pliku .txt
Przetworzenie treści artykułu za pomocą API OpenAI na kod HTML zgodny z wytycznymi
Zapis wygenerowanego kodu HTML w pliku artykul.html
Tworzenie podglądu artykułu w pliku podglad.html na podstawie szablonu szablon.html

Instalacja
1. Sklonuj repozytorium:
   git clone [<URL-repozytorium>](https://github.com/SsebastianPawlik/OxidoTask.git)
   cd <nazwa-folderu>
2. Zainstaluj zależności:
   pip install -r requirements.txt
3. Utwórz plik .env z kluczem do API OpenAI:
   OPENAI_API_KEY=Twój_klucz_API

Użycie
Uruchom aplikację używając poniższego polecenia w terminalu:
python main.py --article ścieżka/do/artykul.txt --output_html artykul.html --template szablon.html --preview podglad.html

Argumenty
--article: Ścieżka do pliku z artykułem (domyślnie artykul.txt)
--output_html: Ścieżka do wygenerowanego pliku HTML artykułu (domyślnie artykul.html)
--template: Ścieżka do szablonu HTML do podglądu artykułu (domyślnie szablon.html)
--preview: Ścieżka do wygenerowanego pliku podglądu HTML (domyślnie podglad.html)

