# BTSearch v2
Repozytorium zawierające kompletny kod źródłowy serwisu [beta.btsearch.pl](http://beta.btsearch.pl), napisany w języku Python z wykorzystaniem frameworku webowego Django.

## Lokalne środowisko developerskie
Uruchomienie projektu w lokalnym środowisku pozwoli na bezpośrednie grzebanie w kodzie, wdrażanie poprawek, usprawnień czy nowych funkcji. Poniżej zapis kroków, które sam wykonałem, aby projekt lokalnie uruchomić.

Odpalenie projektu odbywa się w ramach Docker-a. Docker działa pod Windows, Linux i macOS

```sh
docker compose up -d
```

### Utworzenie struktury bazy danych i uruchomienie webserwera projektowego
Ostatnim krokiem jest utworzenie struktury bazy danych projektu btsearch. Odpalamy dwie komendy - `syncdb` tworzy domyślną strukturę i tabele wspólne dla Django, natomiast `migrate` tworzy i migruje strukturę modeli aplikacji btsearch (tabele mysql, w których trzymane są dane BTS, UKE itp.).

Po ujrzeniu w/w rezultatu, odpalamy przeglądarkę i wpisujemy URL `http://localhost:8000/`.

Voila!

## Pro-tipy

**Jak się dostać do linuxowego systemu plików w Windowsie?**

Podając taką ścieżkę, np. w Eksploratorze Windows: `\\wsl$\DISTRONAME\`, czyli np. `\\wsl$\Ubuntu-18.04\`

Więcej na ten temat przeczytasz tutaj: https://devblogs.microsoft.com/commandline/whats-new-for-wsl-in-windows-10-version-1903/

**Po restarcie Ubuntu projekt się nie odpala!**

Tak, bo każdorazowo należy ponownie aktywować virtualenv poleceniem:
```sh
$ . ~/venv-btsearch/bin/activate
```
Pamiętaj, że virtualenv zawiera pakiety niezbędne do wystartowania projektu i konsoli Django.

## Co dalej?
Na tym etapie mamy w pełni skonfigurowany i odpalony lokalnie projekt btsearch, który ładnie ładuje się w przeglądarce - aczkolwiek baza danych jest pusta, więc na mapce nie wyświetlają się żadne dane. W planach na uporządkowanie kodu źródłowego w bliżej nieokreślonej przyszłości mam m.in.:

- Rozwiązanie problemu z dostępem do lokalnego panelu administracyjnego Django (`TemplateDoesNotExist at /btsadmin/`).
- Przygotowanie testowych danych do bazy danych dla środowiska lokalnego.
- Rozwiązanie problemu z instalacją uwsgi.
- Usunięcie hard-kodowanego odwołania do `models.Region.objects.all()` w pliku `src/bts/btsearch/forms.py`, co blokuje uruchomienie projektu.
- Uaktualnienie zależności projektowych (`requirements.txt`) - obecne są bardzo przestarzałe i już od dawna nie wspierane, np. Django 1.5.
- Opis struktury projektu, zastosowanych rozwiązań, modeli i logiki do README lub artykułu/-ów wiki.
- Rozkmina potencjału wykorzystania dockera do uruchomienia lokalnego środowiska.
- Migracja do Python 3.x.

## Rozwój merytoryczny btsearch
Powyższe modernizacje mają charakter stricte techniczny / developerski i są "niewidzialne" dla zwykłego usera korzystającego z serwisu. Pod kątem merytorycznym, najbardziej palące aktualnie (wg stanu na lipiec-sierpień 2020) problemy do rozwiązania, to:

- Korekta wyświetlania reklam Adsense na mapie (aktualnie zasłaniają one istotne elementy UI).
- Wdrożenie wyświetlania pozwoleń UKE dotyczących stacji bazowych 5G.
- Rozważenie alternatyw dla Google Maps jako podstawowego engine'u renderowania mapy.

Dalsza perspektywa rozwojowa projektu zakłada koncepcję rozdzielenia warstwy danych od UI/UX poprzez API. W dużym uproszczeniu odrębna, relatywnie prosta i lekka aplikacja - nazwijmy ją roboczo `btsearch-core` - odpowiadałaby jedynie za dostarczanie danych poprzez interfejs REST API. Dane te konsumowałaby dowolna aplikacja zewnętrzna - np. `btsearch-map` - i następnie na swój indywidualny sposób je prezentowała. Czy to w formie mapki, czy to tabelarycznie, czy też renderowała do jakiejś aplikacji w smartfonie.

## Kolaboracja i kontakt
Jeśli dobrnąłeś/-aś z sukcesem do tego momentu i masz projekt btsearch lokalnie odpalony w przeglądarce pod adresem `http://127.0.0.1:8000`, to znaczy, że jesteś gotowy/-a do samodzielnego wdrażania poprawek, usprawnień i zmian w kodzie źródłowym.

Gorąco zatem zachęcam do wsparcia i kolaboracji przy projekcie. Kontaktujcie się na maila d.lorenz@btsearch.pl lub poprzez GitHub (Issues). Dzięki z góry!

Dawid Lorenz
