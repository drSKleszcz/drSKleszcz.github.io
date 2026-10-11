# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `redesign/bilingual-portfolio`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza)
- **Recenzent:** ChatGPT
- **Gałąź:** poprawka P3 na `claude/oricalc-redesign-fix` (`6959bcb`); wynik review na `chatgpt/review-oricalc-redesign-fix` (odgałęziona od poprawki)
- **Pliki:** `_projects/en|pl/orifice-calculation-software.md`, `_data/projects.yml`, `_data/images.yml`, `assets/images/oricalc_*.webp`, `WORKFLOW.md`, `HANDOFF.md`
- **Cel:** przenieść aktualizację OriCalc (zrobioną omyłkowo na `main`) do redesignu, w jego formacie, w obu językach; ustawić redesign jako gałąź główną w zasadach pracy.

## Review

- **Review poprawki `6959bcb`: OK — uwaga o historii produktu rozwiązana, brak uwag blokujących.** ChatGPT, 2026-10-11; porównanie `chatgpt/review-oricalc-redesign` (`58f49be`) z `claude/oricalc-redesign-fix` (`6959bcb`). Obie wersje usuwają historię wewnętrznego kalkulatora i zgodnie z informacją od Sławosza zapisaną w przekazaniu mówią o produkcie komercyjnym tworzonym od początku. EN i PL pozostają spójne; pozostały opis, dane i galeria bez zmian. `python -m unittest tests.test_content -v`: 4 testy, wszystkie OK. `git diff --check chatgpt/review-oricalc-redesign..claude/oricalc-redesign-fix`: bez błędów. Pełny build i testy przeglądarkowe nadal pozostają do wykonania w Actions.
- **Opcjonalna uwaga językowa P3:** `_projects/pl/orifice-calculation-software.md:20` — „Od początku powstawało” nie zgadza się rodzajem z wcześniej wskazaną „aplikacją”. Naturalniej: „Aplikacja była od początku tworzona jako produkt komercyjny, oferowany z…” albo „Od początku powstawała jako produkt komercyjny…”. Nie blokuje merge; poprawkę może wprowadzić autor.
- **Wynik: OK — brak uwag blokujących, status DO MERGE.** ChatGPT, 2026-10-11. Sprawdzono commit `956d23f` względem jego rodzica `c9f2ca4`, czyli zmiany redesignu po merge z `main`; wcześniej recenzowanej implementacji z `main` nie oceniano ponownie. Zmieniono wyłącznie ten plik przekazania.
- **Pierwotna uwaga P3 — rozwiązana w `6959bcb`:** zdanie o rozwoju z „in-house calculator” / „wewnętrznego kalkulatora” usunięto z EN i PL zgodnie z informacją od Sławosza zapisaną w przekazaniu. Historia wewnętrznego zastosowania nie obowiązuje.
- **Treść EN/PL:** oba opisy i cztery pary altów są spójne; polski bez istotnych zastrzeżeń. Aktualne strony odczytane bezpośrednio 2026-10-11 potwierdzają trzy tryby obliczeń, ISO 5167:2003, Windows, ofertę demo/licencji bezterminowej/Enterprise, aktywację przypisaną do urządzenia, współautorstwo Ali Karimi, opis raportów oraz wymiarów, chropowatości i odcinków prostych. Źródła: https://orifice-software.com/, https://orifice-software.com/pricing, https://orifice-software.com/software, https://orifice-software.com/learn-more, https://orifice-software.com/demo. „Corner Taps” jest widoczny na wcześniej sprawdzonym zrzucie aplikacji. Wzmianki o modelach właściwości płynu zachowano z wcześniejszych opisów; review nie weryfikuje kodu obliczeniowego aplikacji.
- **Galeria:** cztery nowe elementy mają alt EN/PL i poprawne typy mediów; oryginały oraz odpowiadające im WebP istnieją. Wszystkie 29 wariantów WebP używanych przez obrazek główny i galerię poprawnie się dekoduje; szerokości w `srcset` zgadzają się z plikami. Wymiary źródeł zgadzają się z `_data/images.yml`. Potwierdzono identyczność pikseli `orficle_2.png` i `oricalc_screen_2.png`. Szablon `project-thumbnail.html` udostępnia oryginały przez istniejący podgląd i zwykłe linki.
- **Workflow:** zasady używają redesignu jako gałęzi głównej, a wskazane formaty treści, skrypt optymalizacji obrazków i polecenie testów odpowiadają repozytorium. Ręczna publikacja oraz weryfikacja po pushu są zgodne z `.github/workflows/deploy.yml` i `build.yml`. Gałąź autora zawiera historię `main`, co umożliwia opisane późniejsze wyrównanie przez `--ff-only`.
- **Weryfikacja:** `python -m unittest tests.test_content -v` — 4 testy, wszystkie OK; `git diff --check 956d23f^..956d23f` — bez błędów. Początkowy błąd importu YAML wynikał z brakującej zależności w środowisku; testy uruchomiono z PyYAML/Pillow w katalogu tymczasowym, bez zmian zależności projektu.
- **Ograniczenia:** nie wykonano pełnego buildu Jekyll ani testów przeglądarkowych `tests/test_site.py` (Ruby/Bundler i zbudowane `_site` niedostępne lokalnie). Pozostają do wykonania przez GitHub Actions przed publikacją.

## Dla następnej osoby

- Sławosz: review poprawki OK, DO MERGE. Gałąź `chatgpt/review-oricalc-redesign-fix` zawiera pełną implementację i wynik review; możesz scalić ją do `redesign/bilingual-portfolio`, potem wyrównać `main` przez `--ff-only` (WORKFLOW.md, sekcja 4). Przed publikacją wymagany jest zielony pełny build i testy w Actions. Merge, push i publikację wykonujesz Ty.
- Claude: historia produktu zaakceptowana; opcjonalnie popraw rodzaj gramatyczny „powstawało” w PL zgodnie z nową uwagą językową P3. Recenzent nie zmieniał treści projektu.

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
