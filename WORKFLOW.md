# Workflow: praca nad portfolio z Claude i ChatGPT

To repozytorium (dwujęzyczna strona Jekyll publikowana przez GitHub Pages pod `www.drskleszcz.pl`)
jest edytowane przez dwóch asystentów AI, Claude i ChatGPT, którzy mają dostęp do tego
samego lokalnego folderu. Ten plik opisuje zasady, dzięki którym nie nadpisują sobie zmian.

**Gałąź główna to `redesign/bilingual-portfolio`.** To z niej publikowana jest oficjalna
strona. Każda nowa praca odgałęzia się od niej i do niej wraca. `main` jest tylko
okresowo wyrównywany do redesignu (patrz sekcja 4).

**Zasada nadrzędna: w danym momencie w folderze pracuje tylko jeden asystent,
na własnej gałęzi, a stan pracy zapisuje w `HANDOFF.md`. Jeden implementuje,
drugi robi review.**

---

## 1. Role

| Obszar | Domyślny właściciel | Pliki |
|---|---|---|
| Struktura i wygląd strony | **Claude** | `_layouts/`, `_includes/`, `assets/` (CSS/JS), `pl/`, `projects/` |
| Konfiguracja, build i testy | **Claude** | `_config.yml`, `Gemfile`, `.github/`, `scripts/`, `tests/` |
| Treść projektów | **ChatGPT** | `_projects/en/`, `_projects/pl/`, `_data/projects.yml` |
| Teksty interfejsu i tłumaczenia | **ChatGPT** | `_data/i18n.yml` |
| Obrazki | ten, kto dodaje projekt | `img/portfolio/` + wygenerowane `assets/images/`, `_data/images.yml` |
| Decyzje, merge, push, deploy | **Sławosz** | gałąź `redesign/bilingual-portfolio`, `main`, GitHub |

- Asystent może zmienić plik spoza swojego obszaru tylko wtedy, gdy wpisze to w `HANDOFF.md`
  w sekcji „Aktualne zadanie” (pole „Pliki”), zanim zacznie.
- Żaden asystent nie robi `git push`, merge do gałęzi głównej ani do `main`,
  nie uruchamia publikacji i nie zmienia `CNAME`.
  To zawsze robi Sławosz.

## 2. Autor i recenzent

Każde zadanie ma dwie role. Role przypisuje się do zadania, nie na stałe do asystenta:

- **Autor** to asystent, do którego należy obszar zadania (patrz tabela wyżej).
  Pracuje na swojej gałęzi i jako jedyny edytuje pliki.
- **Recenzent** to drugi asystent. Czyta zmiany poleceniem `git diff redesign/bilingual-portfolio..<gałąź>`
  i zapisuje uwagi w `HANDOFF.md` w sekcji „Review”. **Nie edytuje plików**;
  poprawki wprowadza autor.

Przebieg:
1. *(tylko przy większych zmianach, np. redesign)* Autor zapisuje krótki plan
   w `HANDOFF.md`, recenzent go komentuje, Sławosz akceptuje.
2. Autor implementuje i commituje na swojej gałęzi, status `DO REVIEW`.
3. Recenzent robi review: `OK` albo lista konkretnych uwag (plik, co i dlaczego).
4. Autor poprawia, a kroki 3–4 powtarza się do `OK`.
5. Sławosz robi merge do `redesign/bilingual-portfolio`, wyrównuje `main` i robi push.

Asystenci nie poprawiają nawzajem swojego kodu na zmianę: każdy przepisywałby rzeczy
po swojemu, a historia zmian przestałaby być czytelna.

## 3. Plik przekazania `HANDOFF.md`

`HANDOFF.md` w katalogu głównym to jedyne miejsce, przez które asystenci się komunikują.

**Na początku każdej sesji asystent:**
1. Czyta `HANDOFF.md`.
2. Jeśli w „Aktualne zadanie” jest status `W TOKU` innego asystenta, **nie edytuje plików**
   i informuje o tym Sławosza.
3. Jeśli jest wolne, wpisuje swoje zadanie: kto, gałąź, pliki, status `W TOKU`.

**Na końcu sesji asystent:**
1. Commituje swoje zmiany na swojej gałęzi.
2. Przenosi zadanie do „Historia” z krótkim opisem, co zrobił i co zostało.
3. Ustawia status: `DO REVIEW` (autor skończył), `POPRAWKI` (recenzent zgłosił uwagi),
   `DO MERGE` (review OK) albo `WOLNE`, i wpisuje prośbę do drugiego asystenta
   w „Dla następnej osoby”.

## 4. Git: gałęzie i commity

Gałęzie:
- `redesign/bilingual-portfolio` to **gałąź główna** (oficjalna strona). Nikt poza
  Sławoszem nie commituje tu bezpośrednio.
- `main` to stara gałąź; Sławosz wyrównuje ją do redesignu po każdym merge'u.
  **Nigdy nie odgałęziaj pracy od `main`.**
- `claude/<temat>` dla pracy Claude, np. `claude/nowy-layout-kart`.
- `chatgpt/<temat>` dla pracy ChatGPT, np. `chatgpt/opis-projektu-mrr`.

Rozpoczęcie zadania:
```bash
git switch redesign/bilingual-portfolio
git pull                      # robi Sławosz albo asystent, jeśli ma dostęp do sieci
git switch -c claude/<temat>  # lub chatgpt/<temat>
```

Commity:
- Małe, jeden temat na commit.
- Opis po polsku lub angielsku, z prefiksem autora:
  `[claude] Poprawka odstępów w siatce projektów`,
  `[chatgpt] Nowy opis projektu Pressure test station`.
- Przed commitem: `git status` i `git diff`, żeby nie wciągnąć cudzych zmian.

Zakończenie zadania (Sławosz):
```bash
git switch redesign/bilingual-portfolio
git merge --no-ff claude/<temat>   # albo gałąź recenzenta, jeśli zawiera commit z review
git push                           # GitHub Actions „Build and verify portfolio” uruchamia testy
git switch main
git merge --ff-only redesign/bilingual-portfolio   # wyrównanie main do redesignu
git push
git branch -d claude/<temat>
```
Publikacja nie dzieje się automatycznie: po zielonym buildzie Sławosz uruchamia ręcznie
workflow **„Publish approved portfolio”** (GitHub → Actions) na gałęzi redesignu.

## 5. Podgląd lokalny

```bash
bundle install
bundle exec jekyll serve      # strona na http://localhost:4000
python -m unittest tests.test_content          # szybkie testy treści (bez buildu)
python -m unittest discover -s tests -v        # pełne testy (wymagają _site i Playwright)
```

## 6. Dodanie nowego projektu do portfolio

Szczegółowe zasady są w `docs/content-guide.md`. W skrócie:
1. Dwa pliki z tą samą strukturą: `_projects/en/<slug>.md` i `_projects/pl/<slug>.md`
   (cztery sekcje `##`: wyzwanie, wkład, podejście, rezultaty).
2. Wspólne dane (kategoria, klient, data, obrazek, galeria, linki) w `_data/projects.yml`.
3. Obrazki PNG do `img/portfolio/`, potem `python scripts/optimize_images.py img/portfolio/<plik>.png`
   i commit wygenerowanych `assets/images/*.webp` oraz `_data/images.yml`.
4. `_posts/` to stare wpisy, z których migrowano treść. Nowych treści tam nie dodawać.
5. `python -m unittest tests.test_content`, commit na gałęzi, wpis w `HANDOFF.md`.

## 7. Końce linii (Windows)

Pliki w repo są zapisane w Windows z końcami linii CRLF, a w GitHubie z LF. Git na Windows
z `core.autocrlf=true` tego nie pokazuje, ale narzędzia działające pod Linuksem
widzą wtedy każdy plik jako zmieniony. Zasady:
- Asystent nie commituje plików, w których zmieniły się tylko końce linii
  (`git diff --ignore-cr-at-eol` jest wtedy pusty).
- Plik `.gitattributes` (`* text=auto`) ujednolica końce linii, więc `git status`
  pokazuje tylko prawdziwe zmiany niezależnie od systemu. Nie usuwać go.
