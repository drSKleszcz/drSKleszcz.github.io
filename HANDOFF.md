# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `main`.

## Aktualne zadanie

- **Status:** DO REVIEW  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude
- **Recenzent:** ChatGPT
- **Gałąź:** `claude/sections-refresh` (z `main` `aea42a7`)
- **Pliki:** `assets/site.css`, `tests/test_site.py`
- **Cel:** Sławosz uznał, że hero na home jest dobre, a sekcje niżej i lista All projects są mdłe. Zmiany wyłącznie w CSS, zasada kolorów bez zmian (mięta = klikalne, pomarańcz = etykiety):
  - każda sekcja home (Expertise, Projects, About, Contact) ma delikatną poświatę jak hero, nagłówki sekcji są większe;
  - Expertise: kolumny jako karty z dużymi pomarańczowymi numerami; istniejąca animowana linia zostaje i jest pomarańczowa; karta unosi się po najechaniu;
  - About: zdjęcie z zaokrągloną ramką (bez poświaty), doświadczenie jako karty z pomarańczowym paskiem z lewej;
  - Contact ujednolicony z resztą: tło strony zamiast zielonego gradientu, stopka na panelu; usunięty token `--contact-end`;
  - lista All projects: nagłówek z poświatą, rozdziały z numerami „01 /”, projekty jako karty (unoszą się, miętowa krawędź), organizacja na pomarańczowo, miniatury 200×130 (na telefonie bez zmian);
  - karty projektów na home i strona pojedynczego projektu bez zmian.
- **Testy:** zmienione tylko oczekiwania, które opisywały stary wygląd: kolor sekcji kontaktu i stopki (`test_about_and_contact_complete_the_alternating_section_surfaces`) oraz maks. rozmiar miniatury na liście (161→201, 113→131).

## Review

- (do uzupełnienia przez ChatGPT)

## Dla następnej osoby

- **ChatGPT:** review `main..claude/sections-refresh` na gałęzi `chatgpt/review-sections-refresh`.
- Raport autora (lokalnie, Chromium starszy niż w CI): build OK, 101 testów, z czego 2 znane błędy środowiska (`test_atlas_fragment_focus_and_responsive_themes`, `test_mobile_dropdown_overlays_without_changing_header_or_scroll`), które padają identycznie na czystym `main`; ich pozostałe asercje sprawdzone osobno i przechodzą. Audyt axe `--full`: 188 skanów, 0 błędów.

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
