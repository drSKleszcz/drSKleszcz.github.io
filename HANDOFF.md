# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `main`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude
- **Recenzent:** ChatGPT
- **Gałąź:** autor `claude/home-publications` (z `main` `3e07af1`; `9e258cf` + poprawka P2 `fa89e2d`), review `chatgpt/review-home-publications-fix`
- **Pliki:** `_includes/publication-card.html` (nowy), `_layouts/home.html`, `_layouts/publications.html`, `_data/i18n.yml`, `assets/site.js`, `assets/site.css`, `tests/test_site.py`
- **Cel:** Sławosz poprosił o sekcję Publikacje na stronie głównej zaraz po Projects, z karuzelą kart w tym samym stylu co projekty:
  - nowa sekcja `#publications` między `#projects` a `#about`: nagłówek jak w projektach (etykieta, tytuł, opis, link „Zobacz wszystkie publikacje”), poświata jak w innych sekcjach;
  - karuzela wszystkich 16 prac (lata malejąco) działa jak karuzela projektów: 4 / 2 / 1 karta, strzałki, kropki i przesuwanie palcem na telefonie;
  - karta ma ramkę, hover i układ karty projektu; zamiast obrazka okładka z dużym rokiem (pomarańczowy) i nazwą czasopisma/konferencji; niżej typ, tom/strony, tytuł i autorzy;
  - karta prowadzi do swojej pozycji na `/publications/#publication-...`; pozycja docelowa ma miętową ramkę (`:target`) i nie chowa się pod nagłówkiem;
  - `site.js`: kod karuzeli obsługuje teraz każdą karuzelę na stronie (`[data-carousel]` projektów i nowe `[data-publication-carousel]`); filtr kategorii i linki `?category=` dotyczą tylko projektów; krok kółkiem myszy na desktopie przechodzi z Projects do Publikacji i dalej do About (sekcje z karuzelą mogą być wyższe niż ekran).
- **Do sprawdzenia przez recenzenta (treść):** nowe klucze w `_data/i18n.yml`: `all_publications`, `previous_publication`, `next_publication`, `select_publication`, `swipe_publications_hint` (EN/PL).
- **Testy:** nowy `test_home_publications_carousel_follows_projects`; oczekiwana kolejność sekcji home z `publications`; test kroku kółkiem przechodzi Projects → Publikacje → About; lokatory starych testów karuzeli zawężone do `[data-carousel]` (na home są teraz dwie karuzele). U autora: 104 testy (2 znane błędy środowiska jak na `main`, ich pozostałe asercje przechodzą), axe `--full` 196 skanów bez błędów.

## Review

**Ponowne review · ChatGPT · 2026-10-13 · `fa89e2d`: OK, DO MERGE.**

P2 rozwiązane: minimalna wysokość okładki, mniejsze odstępy i wyłączone kurczenie roku/nazwy zapewniają miejsce na pełne wiersze. Limit trzech wierszy mieści także najdłuższą nazwę. Bez nowych uwag do poprawki CSS i testu regresji. Test obejmuje wszystkie 16 kart przy 1001 i 1040 px w EN oraz PL.

Niezależna weryfikacja: 5 testów treści przeszło, `git diff --check main..HEAD` bez błędów. Izolowany Edge z aktualnym CSS, JS i rzeczywistymi danymi sprawdził wszystkie 16 nazw przy 390, 768, 1001, 1040, 1280 i 1440 px w obu motywach (192 pomiary): brak ucięcia treści i wychodzenia nazwy poza wewnętrzną przestrzeń okładki. Nazwy czasopism są wspólne dla EN/PL. Pełnego buildu Jekyll, testów `_site` i axe nie uruchomiono niezależnie; raport autora pozostaje powyżej. W repo zmieniono wyłącznie `HANDOFF.md`.

Poniżej wcześniejsze review i odpowiedź autora, zachowane dla historii.

**ChatGPT · 2026-10-13 · commit autora `9e258cf` · wynik: POPRAWKI.**

1. **[P2] Nazwa czasopisma jest ucięta w połowie wiersza na wąskim desktopie** — `assets/site.css:930–932`. Przy szerokości okna 1001 px karuzela pokazuje cztery karty, ale okładka zachowuje proporcje obrazka projektu. Rok, pionowy padding i odstęp zostawiają za mało miejsca na dwa wiersze nazwy. Element `.publication-venue` kurczy się do 29,19 px przy wysokości wiersza 18 px; `overflow: hidden` ucina drugi wiersz m.in. „Energy Conversion and Management: X” oraz „IOP Conference Series: Materials Science and Engineering”. Przy 1040 px ma 34,92 px zamiast potrzebnych 36 px; przy 1280 px problem nie występuje. Potwierdzono pomiarem i zrzutem izolowanego układu z rzeczywistym CSS i danymi publikacji. Zapewnić miejsce na pełne wiersze (np. minimalna wysokość okładki lub dostosowanie odstępów przy czterech wąskich kartach) i zapobiec kurczeniu nazwy do części wiersza. Dodać kontrolę okładek w okolicach 1001–1040 px; samo sprawdzenie braku poziomego overflow nie wykrywa tego problemu.

**Sprawdzone:** diff względem `main`, szablony i klucze EN/PL; 5 testów treści przeszło, składnia `site.js` i `git diff --check` bez błędów. Izolowany podgląd Edge z rzeczywistym CSS, JS i danymi potwierdził układ 4 / 2 / 1 karty przy 1001, 1040, 1280, 768 i 390 px oraz niezależność obu karuzel. Strzałki i kropki działają; emulowany gest dotykowy zmienia publikację 1 → 2 bez zmiany karuzeli projektów. Szablony karty i pozycji docelowej używają tego samego identyfikatora; pomocnicza kontrola slugów nie wykazała kolizji dla 16 prac.

**Ograniczenia:** brak lokalnego buildu Jekyll i `_site`, więc pełnych testów strony, przejść kółkiem, rzeczywistego przejścia do kotwicy i audytu axe nie uruchomiono niezależnie. Izolowany podgląd nie obejmuje całej strony ani animacji z `motion.js`. Wyniki 104 testów i 196 skanów axe powyżej pozostają raportem autora. W repo zmieniono wyłącznie `HANDOFF.md`.

**Odpowiedź autora (Claude) na P2:** poprawione. Okładka karty publikacji ma `min-height: 168px` i padding 20 px, rok i nazwa nie kurczą się (`flex-shrink: 0`), nazwa mieści do 3 wierszy (`-webkit-line-clamp: 3`). Najdłuższa nazwa („New Trends in Production Engineering, Pt. 2 (Sciendo)”) zajmuje przy 1001 px 3 wiersze; przy 1040–1280 px okładki mają 168 px, przy 1440 px bez zmian (proporcje obrazka). `test_home_publications_carousel_follows_projects` sprawdza teraz przy 1001 i 1040 px, w EN i PL, wszystkie 16 kart (przewijając karuzelę), że żadna nazwa nie jest ucięta; test bez poprawki CSS nie przechodzi. U autora: 104 testy (2 znane błędy środowiska), axe `--full` 196 skanów bez błędów.

## Dla następnej osoby

- **Sławosz:** review OK; gałąź `chatgpt/review-home-publications-fix` zawiera kod autora, poprawkę `fa89e2d` i wynik review. Można scalić do `main`, sprawdzić pełny build/testy w Actions i opublikować zgodnie z `WORKFLOW.md`.

## Historia

- 2026-10-11 · Claude · `main` (niezacommitowane) · Dodano `WORKFLOW.md` i `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-update` · Przepisano wpis „Orficle Calculation Software” na „OriCalc – Orifice Flow Calculator”: nowy opis, link do strony, nowe zrzuty aplikacji i 3 strony raportu (skopiowane z repo orifice-software.com).
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc` · Review commita `a440277`: OK, status DO MERGE. Sprawdzono aktualną stronę produktu, język, 5 PNG i integrację wpisu; zapisano opcjonalną uwagę o powiększaniu raportów. Do sprawdzenia przed publikacją pozostaje pełny build Jekyll.
- 2026-10-11 · Claude · `claude/oricalc-report-links` · Poprawka P3 z review: miniatury raportu i zrzut wyników klikalne (pełny obraz w nowej karcie). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-report-links` · Review poprawki `a65a592`: P3 rozwiązane, OK, status DO MERGE. Sprawdzono 4 linki do PNG, podpis, strukturę HTML i integrację. Zmieniono wyłącznie `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-redesign` · Okazało się, że oficjalną gałęzią jest `redesign/bilingual-portfolio`, a poprzednia aktualizacja trafiła na `main`. Wmergowano `origin/main` do nowej gałęzi od redesignu (bez konfliktów), przepisano wpis OriCalc w `_projects/en|pl`, dodano galerię (ekran wejściowy + 3 strony raportu) i link do orifice-software.com, wygenerowano webp. `WORKFLOW.md` zaktualizowany: redesign jako gałąź główna, ręczna publikacja przez Actions, nowy format wpisów.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-redesign` · Review `956d23f`: OK, DO MERGE. Sprawdzono opisy EN/PL, bieżącą stronę produktu, galerię, WebP i workflow; 4 testy treści przeszły. Nieblokująca uwaga P3: potwierdzić historię wewnętrznego kalkulatora. Pełny build i testy przeglądarkowe pozostają do wykonania w Actions. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-redesign-fix` · P3: na podstawie informacji od Sławosza usunięto nieprawdziwe „wyrósł z wewnętrznego kalkulatora”; teraz „od początku tworzony jako produkt komercyjny” (EN/PL). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-redesign-fix` · Review `6959bcb`: historia produktu poprawiona w EN/PL, OK, DO MERGE; 4 testy treści przeszły. Opcjonalna uwaga językowa: „powstawało” → „powstawała” w PL. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `redesign/bilingual-portfolio` + `main` · Zmergowano aktualizację OriCalc (`b62db15`); `main` wyrównany do redesignu.
- 2026-10-11 · Claude · `claude/oricalc-cleanup` · Poprawka językowa z review („powstawała”) i zamknięcie zadania OriCalc (status WOLNE).
- 2026-10-11 · Claude · `claude/orifice-website-update` · Wpis „Orifice software website” zaktualizowany po redesignie strony: nowe zrzuty strony głównej i metody, dodane zrzuty podstrony programu i cennika, nowy opis EN/PL. Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-orifice-website` · Review `a5b0857`: OK, DO MERGE, bez uwag. Porównano cztery zrzuty ze stroną live, sprawdzono fakty w źródłach produktu i EN/PL, galerię i 28 WebP; 4 testy treści przeszły. Pełny build i testy strony pozostają do wykonania w Actions. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `main` · Zmergowano aktualizację wpisu o stronie (`e547343`); gałąź `redesign/bilingual-portfolio` usunięta, gałęzią główną znów jest `main`.
- 2026-10-11 · Claude · `claude/workflow-main` · `WORKFLOW.md` i `HANDOFF.md` przełączone na `main` jako gałąź główną; status WOLNE.
- 2026-10-11 · Claude · `claude/gallery-navigation` · Nawigacja między zdjęciami w podglądzie (przyciski, klawisze, swipe na telefonie) + test. Lokalny build Jekyll i testy: wszystkie testy podglądu/galerii/karuzeli przechodzą; 2 testy (`test_atlas_fragment_focus_and_responsive_themes`, `test_mobile_dropdown_overlays_without_changing_header_or_scroll`) padają w środowisku Claude także na czystym `main`, więc nie są związane ze zmianą. Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-gallery-navigation` · Review `a926155`: POPRAWKI, potwierdzone P2 — trwająca animacja blokuje podążanie obrazu za palcem podczas szybkiego kolejnego gestu. Izolowany test Chrome odtworzył problem; 4 testy treści, składnia JS i kontrola diff przeszły. Pełny build i testy strony nieuruchomione u recenzenta. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/gallery-navigation` · Poprawka P2: swipe przejmuje trwającą animację od bieżącej pozycji; test szybkiego drugiego gestu (pada na starym kodzie, przechodzi na nowym). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-gallery-navigation-fix` · Re-review `8ea3919`: P2 rozwiązane, OK, DO MERGE. Izolowany test Chrome potwierdził płynne przejęcie animacji zmiany i powrotu, podążanie za palcem, klawiaturę i ograniczenie ruchu; 4 testy treści, składnia JS i kontrola diff przeszły. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `main` · Scalono nawigację w galerii (`28ec9ca`).
- 2026-10-11 · Claude · `claude/gallery-arrows-side` · Strzałki podglądu obok zdjęcia na komputerze, ukryte na ekranach dotykowych (tylko swipe). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-gallery-arrows-side` · Review `dc9d41f`: OK, DO MERGE. Izolowany test Chrome: 15 wariantów szerokości/proporcji i sposobu wskazywania; strzałki poza obrazem na komputerze, ukryte przy emulacji dotyku. 4 testy treści, składnia JS, kontrola diff i detektor przeszły. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `main` · Scalono strzałki obok zdjęcia (`84c04c3`).
- 2026-10-11 · Claude · `claude/color-refresh` · Odświeżenie kolorów: paleta C, wtopiony pasek, kolory kategorii, kolorowe kompetencje, kontakt + stopka jako jeden blok. Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-color-refresh` · Review `9efb34d`: OK, DO MERGE. Sprawdzono oba motywy, dziedziczenie kategorii, gradient i zmiany testów. Izolowany test Chrome: kontrast wybranych tekstów, hover przycisku i układ 390/1280 px przeszły; 4 testy treści, kontrola diff i detektor także. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `main` · Scalono odświeżenie kolorów (`6b791e4`); build w Actions czerwony (test menu mobilnego).
- 2026-10-11 · Claude · `claude/mobile-header-fix` · Naprawa: niższy pasek tylko na desktopie, mobilny pasek wraca do 81 px. Status DO REVIEW.
- 2026-10-11 · Sławosz · `main` · Scalono poprawkę paska (`940360b`), strona opublikowana.
- 2026-10-11 · Claude · `claude/color-coherence` · Spójność kolorów: mięta = klikalne, pomarańcz = etykiety; usunięte kolory kategorii i kolumn. Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-color-coherence` · Review `f9b9031`: OK, DO MERGE. Sprawdzono role kolorów, usunięte tokeny, oba motywy i granicę 900/901 px. Izolowany test Chrome, kontrast wybranych tekstów, 4 testy treści, kontrola diff i detektor przeszły. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Sławosz · `main` · Scalono spójność kolorów (`aea42a7`).
- 2026-10-11 · Claude · `claude/sections-refresh` · Ożywione sekcje home i lista All projects (poświaty, karty, ujednolicony Contact). Status DO REVIEW.
- 2026-10-12 · ChatGPT · `chatgpt/review-sections-refresh` · Review `0e7bf6d`: OK, DO MERGE. Sprawdzono CSS i zmiany oczekiwań testów; izolowany test Edge potwierdził układ listy w obu motywach, miniatury, widoczność poświaty i ograniczenie ruchu. 4 testy treści i kontrola diff przeszły. Zmieniono tylko `HANDOFF.md`.
- 2026-10-12 · Sławosz · `main` · Scalono ożywione sekcje i listę projektów (`0f005e3`), opublikowane.
- 2026-10-13 · Claude · `claude/publications` · Nowa zakładka Publikacje / Publications (dorobek naukowy EN/PL z Scholar i BaDAP). Status DO REVIEW.
- 2026-10-13 · ChatGPT · `chatgpt/review-publications` · Review `448f720`: OK, DO MERGE. Sprawdzono szablon, EN/PL, wybrane dane w źródłach pierwotnych, testy i 24 warianty izolowanego układu Edge. 5 testów treści i kontrola diff przeszły; kompletność eksportów i pełny build niezweryfikowane niezależnie. Zmieniono tylko `HANDOFF.md` w repo.
- 2026-10-13 · Sławosz · `main` · Scalono zakładkę Publikacje (`3e07af1`).
- 2026-10-13 · Claude · `claude/home-publications` · Sekcja Publikacje na home z karuzelą kart w stylu projektów. Status DO REVIEW.

- 2026-10-13 · ChatGPT · `chatgpt/review-home-publications` · Review `9e258cf`: POPRAWKI, P2 — nazwy czasopism ucięte w połowie wiersza przy 1001–1040 px. 5 testów treści, składnia JS i kontrola diff przeszły; izolowany Edge potwierdził układ, niezależne sterowanie, kropki i gest dotykowy. Zmieniono tylko `HANDOFF.md` w repo.
- 2026-10-13 · Claude · `claude/home-publications` · Poprawka P2: pełne nazwy czasopism na okładkach kart przy 1001–1040 px, test w EN/PL. Status DO REVIEW.

- 2026-10-13 · ChatGPT · `chatgpt/review-home-publications-fix` · Ponowne review `fa89e2d`: P2 rozwiązane, OK, DO MERGE. 5 testów treści i kontrola diff przeszły; izolowany Edge: 192 pomiary nazw bez ucięcia przy 6 szerokościach w obu motywach. Zmieniono tylko `HANDOFF.md` w repo.
