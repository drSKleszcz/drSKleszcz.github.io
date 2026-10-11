# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `redesign/bilingual-portfolio`.

## Aktualne zadanie

- **Status:** DO REVIEW  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza)
- **Recenzent:** ChatGPT
- **Gałąź:** poprawka P3 na `claude/oricalc-redesign-fix` (od `chatgpt/review-oricalc-redesign`)
- **Pliki:** `_projects/en|pl/orifice-calculation-software.md`, `_data/projects.yml`, `_data/images.yml`, `assets/images/oricalc_*.webp`, `WORKFLOW.md`, `HANDOFF.md`
- **Cel:** przenieść aktualizację OriCalc (zrobioną omyłkowo na `main`) do redesignu, w jego formacie, w obu językach; ustawić redesign jako gałąź główną w zasadach pracy.

## Review

- **Wynik: OK — brak uwag blokujących, status DO MERGE.** ChatGPT, 2026-10-11. Sprawdzono commit `956d23f` względem jego rodzica `c9f2ca4`, czyli zmiany redesignu po merge z `main`; wcześniej recenzowanej implementacji z `main` nie oceniano ponownie. Zmieniono wyłącznie ten plik przekazania.
- **Nieblokująca uwaga P3, do potwierdzenia:** `_projects/en/orifice-calculation-software.md:20` i `_projects/pl/orifice-calculation-software.md:20` — nowe zdanie o rozwoju z „in-house calculator” / „wewnętrznego kalkulatora” nie jest potwierdzone na sprawdzonych stronach produktu ani we wcześniejszym opisie. Nie stwierdzono, że jest nieprawdziwe; autor powinien potwierdzić tę historię u Sławosza lub usunąć dopowiedzenie o wewnętrznym zastosowaniu.
- **Treść EN/PL:** oba opisy i cztery pary altów są spójne; polski bez istotnych zastrzeżeń. Aktualne strony odczytane bezpośrednio 2026-10-11 potwierdzają trzy tryby obliczeń, ISO 5167:2003, Windows, ofertę demo/licencji bezterminowej/Enterprise, aktywację przypisaną do urządzenia, współautorstwo Ali Karimi, opis raportów oraz wymiarów, chropowatości i odcinków prostych. Źródła: https://orifice-software.com/, https://orifice-software.com/pricing, https://orifice-software.com/software, https://orifice-software.com/learn-more, https://orifice-software.com/demo. „Corner Taps” jest widoczny na wcześniej sprawdzonym zrzucie aplikacji. Wzmianki o modelach właściwości płynu zachowano z wcześniejszych opisów; review nie weryfikuje kodu obliczeniowego aplikacji.
- **Galeria:** cztery nowe elementy mają alt EN/PL i poprawne typy mediów; oryginały oraz odpowiadające im WebP istnieją. Wszystkie 29 wariantów WebP używanych przez obrazek główny i galerię poprawnie się dekoduje; szerokości w `srcset` zgadzają się z plikami. Wymiary źródeł zgadzają się z `_data/images.yml`. Potwierdzono identyczność pikseli `orficle_2.png` i `oricalc_screen_2.png`. Szablon `project-thumbnail.html` udostępnia oryginały przez istniejący podgląd i zwykłe linki.
- **Workflow:** zasady używają redesignu jako gałęzi głównej, a wskazane formaty treści, skrypt optymalizacji obrazków i polecenie testów odpowiadają repozytorium. Ręczna publikacja oraz weryfikacja po pushu są zgodne z `.github/workflows/deploy.yml` i `build.yml`. Gałąź autora zawiera historię `main`, co umożliwia opisane późniejsze wyrównanie przez `--ff-only`.
- **Weryfikacja:** `python -m unittest tests.test_content -v` — 4 testy, wszystkie OK; `git diff --check 956d23f^..956d23f` — bez błędów. Początkowy błąd importu YAML wynikał z brakującej zależności w środowisku; testy uruchomiono z PyYAML/Pillow w katalogu tymczasowym, bez zmian zależności projektu.
- **Ograniczenia:** nie wykonano pełnego buildu Jekyll ani testów przeglądarkowych `tests/test_site.py` (Ruby/Bundler i zbudowane `_site` niedostępne lokalnie). Pozostają do wykonania przez GitHub Actions przed publikacją.

## Dla następnej osoby

- ChatGPT: zrób review poprawki P3: `git diff chatgpt/review-oricalc-redesign..claude/oricalc-redesign-fix`. Sławosz potwierdził, że OriCalc był pisany od zera jako produkt (nie z wewnętrznego kalkulatora); zdanie w EN i PL zmieniono na „od początku jako produkt komercyjny”.
- Sławosz: po OK zmerguj gałąź z review do `redesign/bilingual-portfolio`, potem `main` przez `--ff-only` (WORKFLOW.md, sekcja 4).

## Historia

- 2026-10-11 · Claude · `main` (niezacommitowane) · Dodano `WORKFLOW.md` i `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-update` · Przepisano wpis „Orficle Calculation Software” na „OriCalc – Orifice Flow Calculator”: nowy opis, link do strony, nowe zrzuty aplikacji i 3 strony raportu (skopiowane z repo orifice-software.com).
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc` · Review commita `a440277`: OK, status DO MERGE. Sprawdzono aktualną stronę produktu, język, 5 PNG i integrację wpisu; zapisano opcjonalną uwagę o powiększaniu raportów. Do sprawdzenia przed publikacją pozostaje pełny build Jekyll.
- 2026-10-11 · Claude · `claude/oricalc-report-links` · Poprawka P3 z review: miniatury raportu i zrzut wyników klikalne (pełny obraz w nowej karcie). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-report-links` · Review poprawki `a65a592`: P3 rozwiązane, OK, status DO MERGE. Sprawdzono 4 linki do PNG, podpis, strukturę HTML i integrację. Zmieniono wyłącznie `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-redesign` · Okazało się, że oficjalną gałęzią jest `redesign/bilingual-portfolio`, a poprzednia aktualizacja trafiła na `main`. Wmergowano `origin/main` do nowej gałęzi od redesignu (bez konfliktów), przepisano wpis OriCalc w `_projects/en|pl`, dodano galerię (ekran wejściowy + 3 strony raportu) i link do orifice-software.com, wygenerowano webp. `WORKFLOW.md` zaktualizowany: redesign jako gałąź główna, ręczna publikacja przez Actions, nowy format wpisów.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-redesign` · Review `956d23f`: OK, DO MERGE. Sprawdzono opisy EN/PL, bieżącą stronę produktu, galerię, WebP i workflow; 4 testy treści przeszły. Nieblokująca uwaga P3: potwierdzić historię wewnętrznego kalkulatora. Pełny build i testy przeglądarkowe pozostają do wykonania w Actions. Zmieniono tylko `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-redesign-fix` · P3: na podstawie informacji od Sławosza usunięto nieprawdziwe „wyrósł z wewnętrznego kalkulatora”; teraz „od początku tworzony jako produkt komercyjny” (EN/PL). Status DO REVIEW.
