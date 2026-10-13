# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `main`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude
- **Recenzent:** ChatGPT
- **Gałąź:** autor `claude/publications` (`448f720`, z `main` `0f005e3`), review `chatgpt/review-publications`
- **Pliki:** `_data/publications.yml` (nowy), `_layouts/publications.html` (nowy), `publications/index.html` i `pl/publications/index.html` (nowe), `_data/i18n.yml`, `_includes/site-nav.html`, `assets/site.css`, `tests/test_site.py`, `tests/test_content.py`
- **Cel:** Sławosz poprosił o zakładkę z dorobkiem naukowym. Nowa strona `/publications/` i `/pl/publications/` w menu (między Projects a About):
  - linki do profili Google Scholar, BaDAP AGH i ORCID, liczniki (wszystkie prace, artykuły, referaty, wystąpienia);
  - 16 prac pogrupowanych latami (malejąco): 6 artykułów, 8 referatów, 1 rozdział, 1 rozprawa doktorska; typ i miejsce publikacji na pomarańczowo, „S. Kleszcz” pogrubione, link DOI miętowy;
  - osobna lista 9 wystąpień konferencyjnych bez publikacji;
  - dane połączone z eksportu Scholar (CSV) i raportu BaDAP (PDF) z 13.10.2026; linkowane są tylko DOI potwierdzone w doi.org;
  - pominięto pozycję Scholar „A numerical analysis of a HYBRID PV+ WT power system” (Sławosz nie jest autorem);
  - rozprawa doktorska ma tytuł PL w wersji PL i tytuł EN (podany przez Sławosza) w wersji EN (`title_en`);
  - menu na 901–1180 px ma mniejsze odstępy (bez tego PL wychodził poza ekran przy 901 px).
- **Dane do sprawdzenia przez recenzenta (treść):** nazwy i opisy w `_data/i18n.yml` (klucze `publications_*`, `publication_types`, `contributions_*`) oraz poprawność wpisów w `_data/publications.yml`. Bez DOI: Energy Reports 2023, Polityka Energetyczna 2019, IOP MSE 1294 012057, EPJ WoC 269 01027, MATEC 240 02003, rozdział Sciendo, rozprawa.
- **Testy:** nowe `test_publications_page_lists_research_in_both_languages` i `test_publications_are_complete_and_ordered`; nawigacja ma 6 pozycji; sitemap 44 adresy (było 42). U autora: 103 testy (2 znane błędy środowiska jak na `main`), axe `--full` 196 skanów bez błędów.

## Review

- **Werdykt: OK, status DO MERGE.** Review `main` (`0f005e3`) → `claude/publications` (`448f720`); brak potwierdzonych uwag wymagających zmian.
- Sprawdzono szablon Liquid, klucze i opisy EN/PL, lata i typy prac, liczniki, wyróżnienie autora, tytuł rozprawy zależny od języka, układ DOI, aktywną pozycję menu, mapowanie wersji językowych przez istniejący layout oraz zmiany testów/sitemap. Dane zawierają 16 prac (6 artykułów, 8 referatów, rozdział i rozprawę) oraz 9 wystąpień; nie znaleziono duplikatów tytuł+typ ani DOI.
- Wybrane dane porównano ze źródłami pierwotnymi: [BaDAP — Energy Reports 2023](https://badap.agh.edu.pl/publikacja/146044), [Measurement 2022](https://www.sciencedirect.com/science/article/pii/S0263224122001919), [Energy Conversion and Management: X 2024](https://www.sciencedirect.com/science/article/pii/S2590174524000382), [BaDAP — Thermal Science 2019](https://badap.agh.edu.pl/publikacja/124783), [repozytorium UiS — praca o bezpieczeństwie wodoru](https://uis.brage.unit.no/uis-xmlui/bitstream/handle/11250/3123582/Kleszcz_2023_IOP_Conf._Ser.__Mater._Sci._Eng._1294_012057.pdf?isAllowed=y&sequence=1). Nie znaleziono rozbieżności w sprawdzonych tytułach, latach, miejscach publikacji i autorstwie.
- Ograniczenia treści: eksport Scholar CSV i raport BaDAP PDF nie są zapisane w repo, więc recenzent nie potwierdza kompletności wszystkich pozycji ani wszystkich wystąpień. Nie zweryfikowano niezależnie autorstwa usuniętej pozycji HYBRID ani pochodzenia angielskiego tytułu rozprawy — są opisane jako ustalenia autora z użytkownikiem. Część bezpośrednich odczytów doi.org nie powiodła się w narzędziu web; nie oznacza to niedziałających linków. Rozwiązywanie wszystkich DOI pozostaje raportem autora.
- Izolowany test Edge z bieżącym CSS i treścią z YAML, w strukturze odpowiadającej szablonowi: EN/PL × dark/light × 320/390/901/1040/1180/1440 px (24 warianty). Brak poziomego przepełnienia i obcięcia kart/liczników; menu desktopowe jest widoczne od 901 px. To kontrola układu na fixture, nie wykonanie buildu Liquid/Jekyll ani pełnych interakcji menu.
- Walidacja recenzenta: 5 testów `tests.test_content` i `git diff --check main..claude/publications` przeszły. Pełnego buildu, testów strony i audytu axe nie uruchomiono tutaj (brak `_site`); 103 testy z dwoma znanymi błędami i 196 skanów axe bez błędów pozostają raportem autora.

## Dla następnej osoby

- **Sławosz:** review OK. Gałąź `chatgpt/review-publications` zawiera zmiany autora i wynik review; można ją scalić do `main`. Przed publikacją sprawdź pełny build, testy strony i audyt dostępności w Actions. Merge, push i publikację wykonuje Sławosz zgodnie z `WORKFLOW.md`.
- Recenzent zmienił wyłącznie `HANDOFF.md` w repozytorium.

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
