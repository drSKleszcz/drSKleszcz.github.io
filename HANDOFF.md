# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `main`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude
- **Recenzent:** ChatGPT
- **Gałąź:** autor `claude/compact-publication-cards` (z `main` `9d416b6`, sprawdzony commit `8bfa21c`); review `chatgpt/review-compact-publication-cards`
- **Pliki:** `assets/site.css`, `tests/test_site.py`
- **Cel:** uwagi Sławosza do kart publikacji na home:
  - karty niższe i bardziej zwarte: okładka nie jest już stałym prostokątem z proporcją obrazu projektu, tylko ma wysokość treści (kreska + nazwa czasopisma); mniejszy tytuł (1.08rem), autorzy .85rem, mniejsze odstępy;
  - sekcja Publikacje mieści się w ekranie 1440×900 (było 857 px przy 821 dostępnych, teraz 821);
  - nazwy czasopism/konferencji pomarańczowe (`--warm`, jak etykiety), .95rem 600, wyrównane do góry okładki; zarezerwowane 3 linie (2 na telefonie), więc tytuły i metadane zaczynają się na tej samej wysokości we wszystkich kartach.
- **Do sprawdzenia przez recenzenta:** czy pomarańczowe nazwy czasopism nie konkurują z etykietą typu w metadanych; czytelność przy 1001–1040 px (nadal pełne nazwy, bez ucięcia).
- **Testy:** `test_home_publications_carousel_follows_projects` dodatkowo sprawdza, że przy 1440 px nazwy czasopism w 4 widocznych kartach mają tę samą pozycję i kolor etykiety sekcji; kontrola pełnych nazw przy 1001/1040 px zostaje. U autora: pełny zestaw testów (2 znane błędy środowiska jak na `main`), axe `--full` 196 skanów bez błędów.

## Review

**ChatGPT · 2026-10-13 · `8bfa21c`: OK, DO MERGE. Bez nowych uwag wymagających poprawki.**

Sprawdzono CSS i uzupełnienie testu względem `main`. Okładki mają wysokość treści zamiast proporcji obrazka; rezerwa wierszy utrzymuje wspólną pozycję metadanych. Nowe reguły są ograniczone do kart publikacji, więc nie zmniejszają kart projektów ani pozycji na osobnej stronie publikacji. Nazwa czasopisma i etykieta typu korzystają z ustalonego koloru `--warm`, ale mają różne wielkości i krój: nazwa jest większa i pisana zwykłym tekstem, typ mniejszym tekstem monospace. Na obejrzanych podglądach nie konkurują o tę samą rolę; tytuł pracy pozostaje czytelny w jasnym kolorze.

**Weryfikacja:** 5 testów treści przeszło, `git diff --check main..HEAD` bez błędów. Izolowany Edge z aktualnym CSS/JS i rzeczywistymi danymi: 28 wariantów (EN/PL, oba motywy, 320/390/600/768/1001/1040/1440 px), wszystkie 16 kart w każdym wariancie — 448 pomiarów bez ucięcia nazw oraz bez różnic w wysokości początku metadanych w widocznym rzędzie. Obejrzano zrzuty desktopowe i mobilny; mniejsze odstępy i autorzy pozostają czytelne. W izolowanym podglądzie sekcja przy 1440×900 miała 805 px z domyślnym offsetem nagłówka 95 px; wynik wspiera zmniejszenie wysokości, ale nie zastępuje pomiaru kompletnej strony z rzeczywistym nagłówkiem. Detektor Impeccable wskazuje jedynie wcześniej uzgodnioną ramkę doświadczenia przy `assets/site.css:854`, poza zmianą.

**Ograniczenia:** nie ma lokalnego buildu Jekyll ani `_site`, więc pełnego zestawu testów strony i axe nie uruchomiono niezależnie. Podgląd odtwarza sekcję i karty, bez pełnego nagłówka oraz animacji `motion.js`; nie weryfikuje ponownie gestów na fizycznym telefonie. Wyniki autora powyżej pozostają jego raportem. W repo zmieniono wyłącznie `HANDOFF.md`.

## Dla następnej osoby

- **Sławosz:** review OK. Gałąź `chatgpt/review-compact-publication-cards` zawiera kod autora i wynik review; można scalić do `main`, potwierdzić pełny build/testy w Actions i opublikować zgodnie z `WORKFLOW.md`.

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
- 2026-10-13 · Sławosz · `main` · Scalono sekcję Publikacje na home (`3ee3aad`).
- 2026-10-13 · Claude · `claude/home-publications-polish` · Numeracja 03 dla Publikacji, link w menu do sekcji na home, okładka kart bez dużego roku. Status DO REVIEW.

- 2026-10-13 · ChatGPT · `chatgpt/review-home-publications-polish` · Review `7534464`: OK, DO MERGE. Spójna numeracja EN/PL, menu i metadane kart; 5 testów treści i kontrola diff przeszły. Izolowany Edge: 28 wariantów kart/nawigacji i 10 kontroli menu desktopowego. Zmieniono tylko `HANDOFF.md` w repo.
- 2026-10-13 · Sławosz · `main` · Scalono poprawki publikacji na home: numeracja, menu, okładka (`9d416b6`).
- 2026-10-13 · Claude · `claude/compact-publication-cards` · Zwarte karty publikacji: okładka o wysokości treści, pomarańczowe nazwy czasopism wyrównane do góry, sekcja mieści się w 1440×900. Status DO REVIEW.

- 2026-10-13 · ChatGPT · `chatgpt/review-compact-publication-cards` · Review `8bfa21c`: OK, DO MERGE. 5 testów treści i kontrola diff przeszły; izolowany Edge potwierdził czytelność i wyrównanie kart w 28 wariantach EN/PL i obu motywów. Zmieniono tylko `HANDOFF.md` w repo.
