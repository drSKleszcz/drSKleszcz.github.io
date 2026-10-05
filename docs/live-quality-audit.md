# Live production audit - 5 October 2026

Target: https://www.drskleszcz.pl, including both languages and all 18 project pairs.
The design, content, layout and animation system are preserved. Two source fixes
are verified locally and have not been published.

## Findings and fixes

- **Contact validation (medium):** reproduced on the live site. Editing one field
  erased the shared error explanation while other fields remained invalid. An
  invalid email also lost its invalid state before correction. The explanation
  and associated states now persist until the affected fields are valid. Existing
  copy, geometry, native fallback and delivery behavior are unchanged.
- **Portrait delivery (low):** Lighthouse identified an inaccurate `sizes` hint.
  It now matches the actual portrait column and its desktop height breakpoint.
  At 412px / DPR 1.75, fresh browser contexts in both languages select the existing
  480px image instead of 640px: **20,982 to 12,480 bytes (40.5% smaller)**. Display
  bounds remain the same within one pixel. The larger desktop portrait also gets
  sufficient resolution. Original files, framing and compression are unchanged.

Both regressions failed before their fixes and passed afterward.

## Live evidence

Lighthouse 13.5.0 / Chromium 153, cold mobile navigations, 412 x 823 / DPR 1.75,
simulated 150ms RTT, 1638.4kbps throughput and 4x CPU slowdown. Homepage values
are medians and ranges from three equivalent runs, before the local fixes.

| Signal | Live homepage |
| --- | --- |
| LCP | 1.095s (0.975-1.286s) |
| CLS | 0 in all runs |
| Total Blocking Time | 0ms in all runs |
| FCP | 1.071s (0.947-1.257s) |
| Transfer size | 124,117 bytes (124,115-124,125) |
| Lighthouse Performance / Accessibility / Best Practices / SEO | 100 / 100 / 100 / 100 in all runs |

Single diagnostic runs on `/pl/projects/` and
`/pl/projects/energy-techno-economics/` also scored 100 in all four categories,
with LCP 1.137s and 1.024s respectively, CLS 0 and TBT 0ms.

These are lab results, not real-user Core Web Vitals or WCAG conformance. The
PageSpeed API returned quota error 429, so field LCP, CLS and INP are unverified.
TBT is not INP. No ranking or indexation outcome is claimed.

## Verification

- All 40 sitemap URLs return 200. The 36 case studies have matching language
  destinations; canonicals, titles, descriptions, language attributes, social
  metadata, robots, internal fragments and 58 referenced asset URLs passed.
  Both explicit 404 pages load; missing routes return real HTTP 404 responses.
- HTTPS works; HTTP and the apex domain resolve to the canonical HTTPS `www`
  site. CSS and JavaScript are gzip-compressed. Development documentation,
  requirements, the old mail handler and `.git/config` return 404.
- **212 live axe scans passed:** 180 covering every rendered route in both
  themes at 390px and 1440px, including open menus and representative dialogs;
  32 additional responsive scans. Automated scans did not detect the form bug.
- **668 live layout checks passed:** both languages/themes, all case studies,
  widths 320-3840px, landscape, laptop-scale equivalents and 200% text resizing.
  No horizontal overflow, header overlap, broken loaded images or runtime
  exceptions were observed. Selected mobile and laptop screenshots were inspected.
- Keyboard skip-link operation, mobile-menu Escape/focus return, image-dialog
  keyboard opening, modal focus isolation, Escape and focus return passed on
  both live and local sites. These journeys logged no console errors or failed
  requests. Native browser controls can receive Tab focus outside the document.
- Fresh production Jekyll build and **75 tests passed**, including bilingual
  content/assets/navigation, anchors, carousels, no-JavaScript fallbacks, theme
  persistence/storage failures, motion interruption and mocked form responses.
  No real contact messages were sent.
- **180 post-fix local axe scans passed.** A local candidate Lighthouse diagnostic
  scored 100 in all categories, LCP 1.804s, CLS 0 and TBT 0ms. Local transport is
  uncompressed and differs from GitHub Pages; this is not a before/after speed
  comparison. The measured optimization is portrait asset selection and bytes.
- OSV returned no known vulnerability matches for 40 checked locked Ruby and
  direct Python package versions. No browser library or external font was added.

Raw JSON and screenshots are in ignored `artifacts/quality-audit/live/`, with
Lighthouse reports in `artifacts/quality-audit/live-*.json` and
`audit-candidate-home.json`. Local final axe output is `artifacts/accessibility.json`.

## Remaining checks and hosting limits

Physical devices, Safari/Firefox and a human screen-reader review remain outside
this Chromium audit. OS scaling was represented by available CSS viewport sizes,
not by changing Windows settings. Search Console and real-user metrics require
separate access/data after deployment.

GitHub Pages sends HSTS and a 600-second asset cache lifetime. Lighthouse flags
the short TTL, but changing it or adding response policies such as CSP
`frame-ancestors` / `X-Content-Type-Options` requires hosting/CDN control, not
Jekyll markup. No speculative preload, service worker or policy rollout was added.
One reference returned 200; ScienceDirect returned 403 to the automated request,
so that publisher page's human access was not established. No broken link was
inferred from an access refusal.

Push and deploy the reviewed fixes separately, then recheck the two affected
flows on the public domain. The local preview is http://127.0.0.1:4173/.
