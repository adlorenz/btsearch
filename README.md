# BTSearch v2
Repozytorium zawierające kompletny kod źródłowy serwisu [beta.btsearch.pl](http://beta.btsearch.pl), napisany w języku Python z wykorzystaniem frameworku webowego Django.

## UWAGA! Projekt nie jest aktywnie rozwijany i wspierany

Projekt w obecnej w tym repozytorium postaci nie będzie już rozwijany, z uwagi na przestarzałe i nie wspierane już zależności w kodzie źrodłowym.

Koncepcja rozwojowa zakłada napisanie nowej, relatywnie prostej i rzecz jasna zdockeryzowanej aplikacji `btsearch-core`, której zasadniczym zadaniem będzie przechowywanie i udostępnianie surowych danych o stacjach bazowych. Struktura danych aplikacji będzie w dużej mierze dziedziczyć po obecnej strukturze relacyjnej modeli Locations > Stations > Cells.

Dane te aplikacja `btsearch-core` będzie z kolei udostępniała poprzez API, co otworzy drogę dla wszystkich chętnych developerów do tworzenia własnych aplikacji opartych o dane btsearch (w tym np. nowej wersji mapy lub apki na smartfony).

Surowe dane na początek mogłyby być ręcznie konwertowane i przerzucane z obecnej bazy mysql btsearch.pl do nowej struktury `btsearch-core` (notabene tak to się obecnie dzieje z aktualizacjami danych na mapie). Docelowo jednak potrzebne będzie napisanie UI do kompleksowego zarządzania danymi wewnątrz `btsearch-core`, żeby definitywnie odciąć legacy btsearch.pl, którego początki sięgają roku 2000 (ok boomer!).

Zatem taki jest ogólny koncept. Palec do budki każdego, kto chętny do wsparcia przy jego rozwijaniu. :) 

_Dawid Lorenz (2.02.2024)_

___

## Lokalne środowisko developerskie
Uruchomienie projektu w lokalnym środowisku pozwoli na bezpośrednie grzebanie w kodzie, wdrażanie poprawek, usprawnień czy nowych funkcji. Poniżej zapis kroków, które sam wykonałem, aby projekt lokalnie uruchomić.

Lokalne środowisko osobiście odpalam w Linuxie (Ubuntu-18.04), zainstalowanym ze sklepu Microsoft Store wewnątrz Windowsa 10. To z kolei wymaga aktywacji WSL (Windows Subsystem for Linux) w Windows 10. Jeśli działasz natywnie w Linuxie, oczywiście pomijasz etap związany z uruchomieniem Linuxa w Windowsie.

**TL;DR dla tych bardziej w temacie**

Projekt btsearch wymaga zainstalowania `python` (3.7+), menedżera pakietów pythonowych `pip`, serwera `mysql-server` oraz `virtualenv`. Kod źródłowy klonujemy z własnego forka GitHub. Następnie wewnątrz utworzonego i aktywowanego virtualenv instalujemy projektowe *dependencies*. Następnie za pośrednictwem konsoli Django `manage.py` tworzymy strukturę bazy i odpalamy webserver na porcie 8000.

### Aktywacja WSL oraz instalacja Ubuntu-20.04 wewnątrz Windows 10
Wykonujemy krok po kroku instrukcje z tego przewodnika:

https://docs.microsoft.com/en-us/windows/wsl/install-win10

Ja u siebie działam na nowszym subsystemie WSL v2. Polecam także aplikację [Windows Terminal](https://www.microsoft.com/pl-pl/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab) z Microsoft Store. Umożliwia wygodniejszą pracę w porównaniu do domyślnej powłoki linuxowej w Windowsie.

### Instalacja niezbędnych pakietów w Ubuntu
Po zainstalowaniu i uruchomieniu Ubuntu-20.04 w Windows 10 instalujemy niezbędne do dalszej pracy pakiety za pomocą `apt-get`.

Aktualizacja repozytoriów z pakietami:
```sh
$ sudo apt-get update
```
Instalacja Pythona 3.x (na nim _jeszcze_ jest oparty projekt):
```sh
$ sudo apt-get install python3
```
Instalacja menedżera pakietów pythonowych `pip`:
```sh
$ sudo apt-get install python3-pip
```

Instalacja wymaganych paczek deweloperskich python3 i mysqlclient
```sh
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

Instalacja serwera mysql:
```sh
$ sudo apt-get install mysql-server
```
Tutaj istotna uwaga - szczególnie jeśli uruchamiasz projekt w WSL/Windows. W trakcie instalacji mysql-server _teoretycznie_ powinna nastąpić wstępna konfiguracja serwera, z podaniem nazwy użytkownika i hasła administratora serwera. U mnie nie wiedzieć czemu to nie nastąpiło. Guglałem za rozwiązaniem problemu, ale poszedłem na skróty i posiłkowałem się hasłem dla systemowego usera `debian-sys-maint`, które podane jest czystym tekstem w pliku `/etc/mysql/debian.cnf`. Z tą kombinacją user/pass zalogowałem się do serwera (klient dowolny - z linii poleceń `mysql`, phpmyadmin, MySQL Workbench - co kto woli) i utworzyłem osobną kombinację user/pass oraz pustą bazę do projektu btsearch.

### Klonowanie kodu źródłowego btsearch z GitHub'a
Następnie tworzymy katalog `/home/USERNAME/dev/` (lub inny wg uznania), do którego sklonujemy repozytorium z kodem źródłowym projektu btsearch. **Uwaga!** Najpierw w GitHub zrób fork repozytorium na swoje konto GH. Wówczas  w miejsce `XYZ` wpisz swój username z GH. Dzięki temu klonujesz swój fork repozytorium z Twojego własnego konta GH.

```sh
$ mkdir dev
$ cd dev
$ git clone git@github.com:XYZ/btsearch.git
$ cd btsearch
```
Po wykonaniu w/w kroków, bieżącą ścieżką powinno być `/home/USERNAME/dev/btsearch/`.

### Utworzenie i aktywacja virtualenv
Pakiety pythonowe niezbędne do uruchomienia projektu btsearch instalujemy wewnątrz virtualenv'a - czyli wirtualnego środowiska pythonowego, niezależnego od pakietów globalnych (widocznych dla całego systemu). Zamykając niezbędne dla projektu pakiety wewnątrz virtualenv nie zaśmiecamy systemu - i potencjalnie innych, sąsiadujących projektów pythonowych - pakietami, które poza uruchomieniem tego konkretnego projektu nie są do niczego potrzebne.

Instalacja i utworzenie virtualenv o nazwie `venv-btsearch` w katalogu `/home/USERNAME/venv-btsearch/`:
```sh
$ pip install virtualenv
$ cd ~
$ virtualenv venv-btsearch
$ . ~/venv-btsearch/bin/activate
```
Po utworzeniu i aktywacji virtualenv'a wg wskazówek powyżej, w przedrostku linii poleceń powinna znaleźć się nazwa aktywowanego virtualenv'a:
```sh
(venv-btsearch) adlorenz@komputer btsearch $
```

### Instalacja projektowych zależności
Po aktywacji virtualenv'a można przystąpić do zainstalowania pakietów pythonowych, niezbędnych do uruchomienia projektu btsearch. Zakładając, że bieżącą ścieżką jest `/home/USERNAME/dev/btsearch/`, odpalamy instalację zależności z pliku `requirements.txt`:
```sh
$ pip install -r src/deploy/requirements.txt
$ pip install -r src/deploy/requirements-dev.txt
```

### Kofiguracja dostępu do bazy danych dla projektu
W pliku `src/conf/local.py.sample` uzupełniamy user/pass/dbname do lokalnej bazy danych mysql, którą konfigurowaliśmy kilka kroków wyżej.
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': '__user__',
        'PASSWORD': '__password__',
        'HOST': 'localhost',
        'NAME': '__dbname__',
    }
}
```
A następnie zapisujemy plik konfiguracyjny pod nazwą `local.py`:
```sh
$ cp src/conf/local.py.sample src/conf/local.py
```

### Uruchomienie konsoli Django
(Przed)ostatni krok to próba uruchomienia konsoli Django `manage.py`. Jeśli otrzymasz wynik jak poniżej - sukces! Projekt jest (prawie) gotowy do lokalnej pracy. :)
```sh
$ cd src
$ ./manage.py --version
3.2.10
```

### Utworzenie struktury bazy danych i uruchomienie webserwera projektowego
Ostatnim krokiem jest utworzenie struktury bazy danych projektu btsearch. Odpalamy komendę `migrate`, która tworzy i migruje strukturę modeli aplikacji btsearch (tabele mysql, w których trzymane są dane BTS, UKE itp.).
W przypadku świeżego projektu
```sh
$ ./manage.py migrate
```

W przypadku posiadania istniejącej bazy danych z wersji `btsearch` opartej na python 2.x i Django 1.5 należy
```sh
$ ./manage.py migrate --fake-initial
$ ./manage.py migrate --fake bts uke
$ ./manage.py migrate
```

Na koniec pozostaje uruchomienie wewnętrznego webservera Django:
```sh
$ ./manage.py runserver
Validating models...

0 errors found
December 19, 2021 - 01:17:20
Django version 3.2.10, using settings 'settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Po ujrzeniu w/w rezultatu, odpalamy przeglądarkę i wpisujemy URL `http://127.0.0.1:8000/`.

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
- Usunięcie hard-kodowanego odwołania do `models.Region.objects.all()` w pliku `src/bts/btsearch/forms.py`, co blokuje uruchomienie projektu. (?)
- Opis struktury projektu, zastosowanych rozwiązań, modeli i logiki do README lub artykułu/-ów wiki.
- Rozkmina potencjału wykorzystania dockera do uruchomienia lokalnego środowiska.

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
