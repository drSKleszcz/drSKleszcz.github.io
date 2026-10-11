# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `redesign/bilingual-portfolio`.

## Aktualne zadanie

- **Status:** DO REVIEW  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza)
- **Recenzent:** ChatGPT
- **Gałąź:** `claude/orifice-website-update` (od `claude/oricalc-cleanup`, która nie jest jeszcze w redesignie; merge tej gałęzi wnosi obie)
- **Pliki:** `_projects/en|pl/orifice-website.md`, `_data/projects.yml`, `_data/images.yml`, `img/portfolio/orifice_website_*.png`, `assets/images/orifice_website_*.webp`, `tests/test_site.py` (oczekiwana galeria)
- **Cel:** zaktualizować wpis o stronie orifice-software.com po redesignie strony (nowe zrzuty i opis).

## Review

- (brak uwag; wyniki poprzednich review są w historii Gita i w sekcji „Historia”)

## Dla następnej osoby

- ChatGPT: zrób review `git diff claude/oricalc-cleanup..claude/orifice-website-update`. Zrzuty (`home`, `software`, `pricing`, `method`, 1440 px) wyrenderowano z szablonów lokalnego repo `C:\Git_hub_local\orifice-software.com` (stan z 2026-10-09), bo z sandboxa Claude strona live jest zablokowana. Porównaj je z https://orifice-software.com/ i sprawdź fakty w tekście EN/PL (redesign 2026, Flask, płatności, demo z linkami, aktywacja licencji, SEO). Galeria ma 3 obrazki + główny; zaktualizowano oczekiwaną listę w `tests/test_site.py:102`. `python -m unittest tests.test_content` przechodzi.
- Sławosz: po OK zmerguj gałąź z review do redesignu, potem `main` przez `--ff-only`.

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
