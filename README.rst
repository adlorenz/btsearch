BTSearch v2
===========

Kompletny kod źródłowy serwisu beta.btsearch.pl_, napisany w języku Python z wykorzystaniem frameworku webowego Django.

Update w sprawie dalszego rozwoju projektu BTSearch
---------------------------------------------------

**Przeszłość**

Serwis btsearch.pl założyłem jako prostą bazę danych o BTS'ach w województwie lubuskim jakieś, hmmm... 20 lat temu. Wow, właśnie sobie uświadomiłem jaka to kupa czasu, no cóż. ;) 

Natomiast projekt **BTSearch v2** (czyli mapka BTS'ów i pozwoleń UKE napisana w Pythonie z UI opartym o Google Maps i Bootstrap) powstał jako *side-project* w czasach, gdy pracowałem jako pełnoetatowy web developer. 

Jednakże jakiś czas temu ścieżka mojego rozwoju zawodowego nieco zmieniła swój kurs i od kilku lat nie zajmuję się już programowaniem - ani zawodowo, ani hobbystycznie. To niestety odbiło się na rozwoju projektu - co zresztą widać, słychać i czuć. 

Choć nie latam już z netmonitorem w ręku w poszukiwaniu nowych BTS, ani nie zbieram i uzupełniam danych - wciąż mam do BTSearch ogromny sentyment.

**Teraźniejszość**

Rozwój projektu de facto utknął w martwym punkcie, a problemy związane z bieżącym funkcjonowaniem serwisu widać gołym okiem. 

Poczynając od engine'u Google Maps, który nie ładuje się poprawnie z uwagi na wprowadzone przez Google restrykcyjne limity, poprzez niepoprawnie wyświetlane, zasłaniające UI reklamy Adsense (z których dochód *częściowo* pokrywa koszty związane z utrzymywaniem serwisu), kończąc na braku obsługi nowych danych UKE - np. lokalizacji stacji bazowych 5G.

Te wszystkie problemy wymagają praktycznie natychmiastowej interwencji, ale z tym jest jeden zasadniczy problem - ja sam. 

Kod źródłowy projektu jest teoretycznie otwarty dla każdego w Githubie i teoretycznie każdy zainteresowany może dołożyć swoją cegiełkę do rozwoju serwisu. Niestety kod jest przy tym napisany w sposób kompletnie niesprzyjający jakiejkolwiek kolaboracji. 

Na przestrzeni czasu otrzymywałem sygnały od developerów skłonnych pomóc przy rozwoju kodu, ale ostatecznie sprawa rozbijała się o brak konkretnej reakcji z mojej strony. Przepraszam.

**Przyszłość**

Akcja pod roboczym kryptonimem *btsearch-resurrection* zakłada następujący *plan minimum*:

1. Odtworzenie lokalnego środowiska developerskiego i odpalenie projektu.
2. Opisanie procesu postawienia środowiska projektowego w pliku README, a przez to ułatwienie quick-startu z btsearch innym chętnym developerom.
3. Naprawa najbardziej palących problemów, np. korekta wyświetlania reklam Adsense, wdrożenie wyświetlania lokalizacji 5G.
4. Rewizja kodu źródłowego i rozważenie alternatywnego rozwiązania dla podkładu Google Maps.

Lekko nie będzie, bowiem moja wiedza z zakresu Pythona, Django, JavaScript, serwerów - czy programowania webowego ogólnie - bardzo mocno zardzewiała. No ale nie od razu Rzym zbudowano. ;)

--
Dawid Lorenz (20.06.2020)

PS. Wielkie podziękowania dla Krzysztofa Niemczyka oraz rzeszy łowców BTS z całej Polski, bez których BTSearch by dziś już dawno nie istniał. Dziękuję!

.. _beta.btsearch.pl: http://beta.btsearch.pl
