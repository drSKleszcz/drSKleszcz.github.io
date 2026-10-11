# HANDOFF

Plik przekazania pracy między Claude i ChatGPT. Zasady w `WORKFLOW.md`.

## Aktualne zadanie

- **Status:** DO MERGE  <!-- WOLNE / W TOKU / DO REVIEW / POPRAWKI / DO MERGE -->
- **Autor:** Claude (na prośbę Sławosza, mimo że `_posts/` to obszar ChatGPT)
- **Recenzent:** ChatGPT
- **Gałąź:** poprawka P3 na `claude/oricalc-report-links` (`a65a592`, zawiera wcześniejszą implementację i review); wynik ponownego review na `chatgpt/review-oricalc-report-links` (odgałęziona od poprawki)
- **Pliki:** `_posts/2014-07-18-project-software-5.markdown`, nowe `img/portfolio/oricalc_*.png`
- **Cel:** zaktualizować wpis o OriCalc pod nową stronę orifice-software.com

## Review

- **Ponowne review: OK — P3 rozwiązane, brak nowych uwag.** ChatGPT, 2026-10-11; porównanie `chatgpt/review-oricalc` (`2d7d6d3`) z `claude/oricalc-report-links` (`a65a592`). Wszystkie cztery nowe linki obejmują właściwy obrazek, wskazują na istniejący PNG o tej samej nazwie i mają `target="_blank"` oraz `rel="noopener"`. Podpis po angielsku jest poprawny. Rozmiary miniaturek przeniesiono na elementy linków, zachowując układ flex i zawijanie. Sprawdzono strukturę linków parserem HTML, ścieżki plików i `git diff --check`; skrypt przewijania strony nie przechwytuje tych linków. Review statyczne — bez buildu Jekyll i testu w przeglądarce; Bundler nadal niedostępny. W tej poprawce nie zmieniano faktów o produkcie ani plików obrazków.
- **Wynik: OK — brak uwag blokujących merge.** Review: ChatGPT, 2026-10-11; porównanie `main` (`d0a5780`) z `claude/oricalc-update` (`a440277`). Wpis i obrazki pozostawiono bez zmian.
- **P3 — rozwiązane w `a65a592`:** pierwotna uwaga dotyczyła braku możliwości powiększania miniaturek raportu. Claude dodał linki do pełnych PNG dla trzech stron raportu i zrzutu wyników oraz podpis „Click an image to open it in full size.”.
- **Fakty:** aktualne strony produktu odczytane bezpośrednio 2026-10-11 potwierdzają trzy tryby obliczeń, Windows, darmowe demo, licencję bezterminową, ofertę Enterprise, aktywację przypisaną do urządzenia, współautorstwo Ali Karimi oraz opis interfejsu i raportów. Źródła: https://orifice-software.com/, https://orifice-software.com/pricing, https://orifice-software.com/demo, https://orifice-software.com/software, https://orifice-software.com/learn-more. Wariant „Corner Taps” jest widoczny na `oricalc_screen_1.png`, choć strona główna go nie wymienia. Wyniki wyszukiwarki zawierały starszą wersję regulaminu; aktualny regulamin demo potwierdza licencję bezterminową.
- **Kontrole:** angielski bez istotnych zastrzeżeń; wszystkie 5 nowych PNG poprawnie się otwiera i odpowiada opisom; odwołania do obrazków istnieją; kontrola CRC PNG poprawna; `modal-id: 4` pozostaje unikalny; `git diff --check main..claude/oricalc-update` bez błędów. Statyczna kontrola HTML i integracji z szablonem nie wykazała nowych problemów.
- **Ograniczenia:** nie wykonano pełnego buildu Jekyll ani podglądu strony w przeglądarce — `bundle exec jekyll build` nie może się uruchomić, ponieważ Bundler nie jest dostępny. Nie wykonano niezależnego parsowania YAML (brak PyYAML). Review potwierdza treść i zasoby, nie poprawność obliczeń wewnątrz aplikacji OriCalc.

## Dla następnej osoby

- Sławosz: review poprawki OK, status DO MERGE. `claude/oricalc-report-links` zawiera pełną implementację. `chatgpt/review-oricalc-report-links` zawiera dodatkowo commit z wynikiem tego review; jeśli wynik ma trafić do `main`, scal tę gałąź albo przenieś jej commit z `HANDOFF.md` na gałąź autora przed scaleniem. Merge i push wykonujesz Ty. Przed publikacją pozostaje sprawdzenie pełnego buildu w środowisku z Ruby/Bundler.
- Claude: poprawka P3 zaakceptowana; brak dalszych uwag do obecnego zakresu.

## Historia

- 2026-10-11 · Claude · `main` (niezacommitowane) · Dodano `WORKFLOW.md` i `HANDOFF.md`.
- 2026-10-11 · Claude · `claude/oricalc-update` · Przepisano wpis „Orficle Calculation Software” na „OriCalc – Orifice Flow Calculator”: nowy opis, link do strony, nowe zrzuty aplikacji i 3 strony raportu (skopiowane z repo orifice-software.com).
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc` · Review commita `a440277`: OK, status DO MERGE. Sprawdzono aktualną stronę produktu, język, 5 PNG i integrację wpisu; zapisano opcjonalną uwagę o powiększaniu raportów. Do sprawdzenia przed publikacją pozostaje pełny build Jekyll.
- 2026-10-11 · Claude · `claude/oricalc-report-links` · Poprawka P3 z review: miniatury raportu i zrzut wyników klikalne (pełny obraz w nowej karcie). Status DO REVIEW.
- 2026-10-11 · ChatGPT · `chatgpt/review-oricalc-report-links` · Review poprawki `a65a592`: P3 rozwiązane, OK, status DO MERGE. Sprawdzono 4 linki do PNG, podpis, strukturę HTML i integrację. Zmieniono wyłącznie `HANDOFF.md`.
