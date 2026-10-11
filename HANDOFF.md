# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza, mimo że `_posts/` to obszar ChatGPT)
- **Recenzent:** ChatGPT
- **Gałąź:** `claude/oricalc-update` (implementacja: `a440277`); review na `chatgpt/review-oricalc` (odgałęziona od implementacji)
- **Pliki:** `_posts/2014-07-18-project-software-5.markdown`, nowe `img/portfolio/oricalc_*.png`
- **Cel:** zaktualizować wpis o OriCalc pod nową stronę orifice-software.com

## Review

- **Wynik: OK — brak uwag blokujących merge.** Review: ChatGPT, 2026-10-11; porównanie `main` (`d0a5780`) z `claude/oricalc-update` (`a440277`). Wpis i obrazki pozostawiono bez zmian.
- **Opcjonalnie, P3:** `_posts/2014-07-18-project-software-5.markdown:49–51` — trzy strony raportu są wyświetlane z szerokością 31% (minimum 160 px), bez możliwości powiększenia. Tekst i podpisy wykresów są przez to trudne do odczytania. Warto opakować miniatury w linki do pełnych PNG lub pokazać raporty na pełną szerokość.
- **Fakty:** aktualne strony produktu odczytane bezpośrednio 2026-10-11 potwierdzają trzy tryby obliczeń, Windows, darmowe demo, licencję bezterminową, ofertę Enterprise, aktywację przypisaną do urządzenia, współautorstwo Ali Karimi oraz opis interfejsu i raportów. Źródła: https://orifice-software.com/, https://orifice-software.com/pricing, https://orifice-software.com/demo, https://orifice-software.com/software, https://orifice-software.com/learn-more. Wariant „Corner Taps” jest widoczny na `oricalc_screen_1.png`, choć strona główna go nie wymienia. Wyniki wyszukiwarki zawierały starszą wersję regulaminu; aktualny regulamin demo potwierdza licencję bezterminową.
- **Kontrole:** angielski bez istotnych zastrzeżeń; wszystkie 5 nowych PNG poprawnie się otwiera i odpowiada opisom; odwołania do obrazków istnieją; kontrola CRC PNG poprawna; `modal-id: 4` pozostaje unikalny; `git diff --check main..claude/oricalc-update` bez błędów. Statyczna kontrola HTML i integracji z szablonem nie wykazała nowych problemów.
- **Ograniczenia:** nie wykonano pełnego buildu Jekyll ani podglądu strony w przeglądarce — `bundle exec jekyll build` nie może się uruchomić, ponieważ Bundler nie jest dostępny. Nie wykonano niezależnego parsowania YAML (brak PyYAML). Review potwierdza treść i zasoby, nie poprawność obliczeń wewnątrz aplikacji OriCalc.

## Dla następnej osoby

- Sławosz: review OK; możesz wykonać merge i push. Gałąź `chatgpt/review-oricalc` zawiera implementację Claude oraz commit z wynikiem review w tym pliku. Przed publikacją warto uruchomić lokalny build w środowisku z Ruby/Bundler.
- Claude: opcjonalna poprawka miniatur raportu jest opisana w „Review”; nie blokuje obecnego merge. W razie dalszych zmian przekaż je ponownie do review.

## Historia

- 2026-10-11 · Claude · `main` (niezacommitowane) · Dodano `WORKFLOW.md` i `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-update` · Przepisano wpis „Orficle Calculation Software” na „OriCalc – Orifice Flow Calculator”: nowy opis, link do strony, nowe zrzuty aplikacji i 3 strony raportu (skopiowane z repo orifice-software.com).
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc` · Review commita `a440277`: OK, status DO MERGE. Sprawdzono aktualną stronę produktu, język, 5 PNG i integrację wpisu; zapisano opcjonalną uwagę o powiększaniu raportów. Do sprawdzenia przed publikacją pozostaje pełny build Jekyll.
