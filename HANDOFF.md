# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.
Gałąź główna: `redesign/bilingual-portfolio`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza)
- **Recenzent:** ChatGPT
- **Gałąź:** `claude/orifice-website-update` (`a5b0857`, od `claude/oricalc-cleanup`); wynik review na `chatgpt/review-orifice-website` (zawiera również cleanup OriCalc)
- **Pliki:** `_projects/en|pl/orifice-website.md`, `_data/projects.yml`, `_data/images.yml`, `img/portfolio/orifice_website_*.png`, `assets/images/orifice_website_*.webp`, `tests/test_site.py` (oczekiwana galeria)
- **Cel:** zaktualizować wpis o stronie orifice-software.com po redesignie strony (nowe zrzuty i opis).

## Review

- **Wynik: OK — brak uwag, status DO MERGE.** ChatGPT, 2026-10-11; porównanie `claude/oricalc-cleanup` (`a95936f`) z `claude/orifice-website-update` (`a5b0857`). Recenzent nie zmieniał opisów, danych, obrazków ani testów; zapisano wyłącznie wynik w `HANDOFF.md`.
- **Zrzuty i strona live:** otwarto https://orifice-software.com/, https://orifice-software.com/software, https://orifice-software.com/pricing i https://orifice-software.com/learn-more w przeglądarce i porównano z czterema PNG. Treść, nawigacja, ciemny wygląd, sfera cząsteczek, przycisk pauzy, cennik oraz renderowane równania odpowiadają aktualnej stronie. Różnice w rozłożeniu treści wynikają z szerokości widoku, a sfera jest animowana; nie stwierdzono rozbieżności wymagających wymiany zrzutów.
- **Fakty EN/PL:** opisy są spójne i bez istotnych zastrzeżeń językowych. W lokalnym repo produktu potwierdzono Flask (`main.py:73`), obsługę płatności (`stripe_handlers.py:47,83,203`), demo z podpisanymi i wygasającymi linkami (`main.py:424–437`, `download.py:19–59`), aktywację przypisaną do urządzenia (`main.py:515–552`), metadane i sitemap (`website_support.py:39–59`, `templates/base.html:6–17`), cache i kompresję odpowiednich tekstowych zasobów statycznych (`website_support.py:70–89`). Historia szablonów i animacji z 7–8 października 2026 potwierdza rok redesignu. Ścieżki dotyczą `C:\Git_hub_local\orifice-software.com\orifice-software.com\public_python\`; repo produktu wykorzystano tylko jako źródło, bez zmian i bez wykonywania kodu.
- **Galeria:** główny obrazek i trzy elementy galerii istnieją, PNG mają 1440 × 900 px, wszystkie nowe elementy mają alt EN/PL i typ `screen`. Wszystkie 28 używanych wariantów WebP poprawnie się dekoduje, wymiary źródeł i szerokości `srcset` zgadzają się z `_data/images.yml`. Kolejność `home`, `method`, `software`, `pricing` odpowiada zmienionej liście w `tests/test_site.py:102`; sprawdzono ją statycznie z danych YAML i kodu testu.
- **Weryfikacja:** `python -m unittest tests.test_content -v` — 4 testy, wszystkie OK. `git diff --check claude/oricalc-cleanup..claude/orifice-website-update` — bez błędów. Sprawdzono również wniesioną poprawkę językową OriCalc w `claude/oricalc-cleanup`: „powstawała” rozwiązuje poprzednią uwagę P3.
- **Ograniczenia:** nie wykonano pełnego buildu Jekyll ani całego `tests/test_site.py` (brak lokalnego Ruby/Bundler i `_site`); pozostają do wykonania w Actions przed publikacją. Przegląd strony produktu i jej źródeł nie obejmował wykonywania prawdziwych płatności, wysyłki e-maili ani aktywacji licencji; nie potwierdza ich konfiguracji produkcyjnej.

## Dla następnej osoby

- Sławosz: review OK. Gałąź `chatgpt/review-orifice-website` zawiera aktualizację strony, wcześniejszy cleanup OriCalc i zapis review. Możesz scalić ją do redesignu, następnie wyrównać `main` przez `--ff-only` zgodnie z `WORKFLOW.md`. Publikację uruchom po zielonym pełnym buildzie i testach w Actions. Merge, push i publikację wykonujesz Ty.
- Claude: zakres zaakceptowany, brak dalszych uwag.

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
