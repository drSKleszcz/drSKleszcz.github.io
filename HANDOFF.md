# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `main`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude
- **Recenzent:** ChatGPT
- **Gałąź:** autor `claude/gallery-navigation` (`8ea3919`), review `chatgpt/review-gallery-navigation-fix`
- **Pliki:** `_layouts/project.html`, `assets/site.js`, `assets/site.css`, `_data/i18n.yml`, `tests/test_site.py`
- **Cel:** W powiększonym zdjęciu projektu można przechodzić do kolejnych bez zamykania: strzałki ← → w oknie, klawisze strzałek, licznik „2 / 4”, a na telefonie przesunięcie palcem (obraz podąża za palcem; pionowe gesty i pinch-zoom zostają przeglądarce). Po zamknięciu fokus wraca na miniaturę ostatnio oglądanego zdjęcia. Nowe klucze i18n: `previous_image`, `next_image` (EN/PL). Nowy test przeglądarkowy `test_image_viewer_steps_through_gallery_with_buttons_keys_and_swipe`.

## Review

| Before | After | Why |
|---|---|---|
| P2: trwająca animacja przesłaniała ruch obrazu przy szybkim kolejnym geście. | `assets/site.js:518–524` odczytuje bieżącą pozycję, anuluje animacje i kontynuuje gest od tej pozycji. | Izolowany test Chrome potwierdził brak skoku przy przejęciu i zgodność dalszego ruchu obrazu z ruchem palca, również podczas animacji powrotu. |

- **Werdykt: OK / Approve, status DO MERGE.** Ponowne review poprawki `8ea3919` względem `8cb3aba`, z uwzględnieniem wcześniejszego review pełnej zmiany `main..claude/gallery-navigation`. P2 rozwiązane; brak nowych potwierdzonych uwag wymagających zmian.
- Test przeglądarkowy recenzenta używał aktualnego kodu galerii, mechanizmu motion i CSS w izolowanej stronie. Przy przejęciu animacji pozycja pozostała 4,58552 px, potem ruch palca o −25 px przesunął obraz do −20,4145 px; aktywnych animacji było 0. Przejęcie animacji powrotu także zachowało pozycję i śledziło dalszy ruch. Krótki gest zakończył się powrotem do `transform: none`. Nawigacja klawiaturą i przy ograniczeniu ruchu nie uruchamiała animacji.
- Nowy test regresji sprawdza computed transform, brak aktywnej animacji podczas gestu i powrót po krótkim przesunięciu. Raport autora potwierdza, że test pada na poprzednim kodzie i przechodzi na poprawionym.
- Walidacja recenzenta: 4 testy `tests.test_content`, kontrola składni `assets/site.js` i `git diff --check main..HEAD` przeszły. Pełnego buildu Jekyll i `tests.test_site` nie uruchomiono tutaj (brak Ruby/Bundler i `_site`). Wynik 29 testów galerii/podglądu/karuzeli pochodzi z raportu autora.

## Dla następnej osoby

- **Sławosz:** review OK. Gałąź `chatgpt/review-gallery-navigation-fix` zawiera kod autora i wynik obu review; można ją scalić do `main`. Przed publikacją sprawdź pełny build i testy strony w Actions. Merge, push i publikację wykonuje Sławosz zgodnie z `WORKFLOW.md`.
- Recenzent zmienił wyłącznie `HANDOFF.md`.

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
