# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `redesign/bilingual-portfolio`.

## Aktualne zadanie

- **Status:** DO REVIEW  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza)
- **Recenzent:** ChatGPT
- **Gałąź:** `claude/oricalc-redesign` (od `redesign/bilingual-portfolio`, z wmergowanym `origin/main`)
- **Pliki:** `_projects/en|pl/orifice-calculation-software.md`, `_data/projects.yml`, `_data/images.yml`, `assets/images/oricalc_*.webp`, `WORKFLOW.md`, `HANDOFF.md`
- **Cel:** przenieść aktualizację OriCalc (zrobioną omyłkowo na `main`) do redesignu, w jego formacie, w obu językach; ustawić redesign jako gałąź główną w zasadach pracy.

## Review

- (brak uwag)

## Dla następnej osoby

- ChatGPT: zrób review `git diff origin/redesign/bilingual-portfolio..claude/oricalc-redesign` z pominięciem commita merge z `main` (jego treść była już recenzowana). Sprawdź: fakty w EN i PL względem https://orifice-software.com/, jakość polskiego, galerię w `_data/projects.yml` (4 obrazki z alt EN/PL), poprawki `WORKFLOW.md` (redesign jako gałąź główna). `python -m unittest tests.test_content` przechodzi; pełne testy (`tests/test_site.py`) puści GitHub Actions po pushu.
- Uwaga: obrazek główny został `orficle_2.png`, bo jest identyczny z nowym ekranem wyników (`oricalc_screen_2.png`) i używają go testy.
- Sławosz: po OK — merge do redesignu, push, potem `main` przez `--ff-only` (komendy w `WORKFLOW.md`, sekcja 4).

## Historia

- 2026-10-11 · Claude · `main` (niezacommitowane) · Dodano `WORKFLOW.md` i `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-update` · Przepisano wpis „Orficle Calculation Software” na „OriCalc – Orifice Flow Calculator”: nowy opis, link do strony, nowe zrzuty aplikacji i 3 strony raportu (skopiowane z repo orifice-software.com).
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc` · Review commita `a440277`: OK, status DO MERGE. Sprawdzono aktualną stronę produktu, język, 5 PNG i integrację wpisu; zapisano opcjonalną uwagę o powiększaniu raportów. Do sprawdzenia przed publikacją pozostaje pełny build Jekyll.
- 2026-10-11 · Claude · `claude/oricalc-report-links` · Poprawka P3 z review: miniatury raportu i zrzut wyników klikalne (pełny obraz w nowej karcie). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-report-links` · Review poprawki `a65a592`: P3 rozwiązane, OK, status DO MERGE. Sprawdzono 4 linki do PNG, podpis, strukturę HTML i integrację. Zmieniono wyłącznie `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-redesign` · Okazało się, że oficjalną gałęzią jest `redesign/bilingual-portfolio`, a poprzednia aktualizacja trafiła na `main`. Wmergowano `origin/main` do nowej gałęzi od redesignu (bez konfliktów), przepisano wpis OriCalc w `_projects/en|pl`, dodano galerię (ekran wejściowy + 3 strony raportu) i link do orifice-software.com, wygenerowano webp. `WORKFLOW.md` zaktualizowany: redesign jako gałąź główna, ręczna publikacja przez Actions, nowy format wpisów.
