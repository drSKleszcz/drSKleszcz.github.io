# Production quality audit - 5 October 2026

The finished design, content, routes, themes and animation sequences are preserved.
The production build and local preview are verified. Nothing was published.

## Evidence

Target: `http://127.0.0.1:4173/`, its bilingual collection and case-study pages.
Lighthouse 13.5.0, Chromium 153, mobile 412 × 823 at DPR 1.75, cold storage/cache,
simulated 150ms RTT / 1638.4kbps throughput / 4× CPU slowdown. No authentication.
Homepage values below are medians of three equivalent navigations, with ranges.
The Windows audit browser was closed between final runs to avoid accumulated
background browser processes. Host load still varies; these are lab measurements.

| Homepage signal | Baseline | Final |
| --- | --- | --- |
| LCP | 2.031s (2.028–2.045) | 1.770s (1.744–1.860) |
| CLS | 0.1588 in all runs | 0 in all runs |
| Total downloaded bytes | 609,956 | 209,250 |
| FCP | 1.056s (1.053–1.070) | 1.523s (1.467–1.632) |
| Total Blocking Time | 0ms | 90ms (87–115) |
| Performance score | 92–93 | 98–99 |

Download weight fell by 65.7%. FCP and TBT increased in the final measurements;
they are reported rather than hidden behind the higher overall score. Final FCP
remains below 1.8s and TBT below 200ms. TBT is a loading diagnostic, **not INP**.
No claim is made about real-user Core Web Vitals or search rankings.

Representative secondary routes received one diagnostic run each:

| Route | LCP baseline → final | CLS baseline → final | Bytes baseline → final |
| --- | --- | --- | --- |
| `/projects/` | 2.103s → 2.036s | 0.1588 → 0 | 535,561 → 329,932 |
| `/pl/projects/energy-techno-economics/` | 1.878s → 1.771s | 0.1586 → 0 | 321,478 → 178,292 |

Final Lighthouse Accessibility, SEO and Best Practices scores were 100 on all five
final runs. Scores cover automated checks, not complete accessibility conformance.
Earlier snapshots occasionally sampled a workflow label during its approved fade;
the settled-content axe checks also passed, without removing the animation.

Raw reports: `artifacts/quality-audit/baseline-*.json` and
`artifacts/quality-audit/production-*.json` (local, ignored artifacts).

## Findings fixed

- **Loading stability:** a delayed-script browser observation confirmed that the
  mobile header shrank from about 155px to 81px. The enhanced header now reserves
  its final geometry before first paint. The collection filter bar also reserves
  its space. Inactive controls remain hidden until handlers are available;
  disabling JavaScript still exposes the native navigation and project links.
- **Accessible navigation names:** the brand now includes its visible role in its
  accessible name, with a real word boundary between the name and role. Language
  switch names include the visible EN/PL codes. Redundant project-link image names
  are decorative; gallery previews and the portrait keep meaningful alternatives.
- **Tablet navigation:** menu reset now uses the same 901px breakpoint as the
  desktop layout, avoiding stale expanded state after resizing.
- **Image delivery:** 160/320/640/768px variants support compact plates and phone
  screens. The portrait uses responsive WebP delivery; related cards declare their
  actual layout sizes, and FedEx crop sizing accounts for the larger source image.
  Initial mobile carousel visibility prevents fetching three hidden opening cards.
  Source images, technical canvases, crops and final thumbnail geometry are retained.
- **Image-viewer usability:** Ctrl/Command/Shift-click keeps native original-image
  link behavior. Full-resolution dimensions now reserve the dialog's final size
  before the image arrives. A deliberately delayed original reproduced the former
  expansion, and the regression now checks stable size and position on phones
  and desktop.
- **Regression coverage:** the build workflow adds an integrity-checked, pinned
  axe audit, including WCAG 2.2, best-practice and Label in Name checks. Open mobile
  menus and representative dialogs are included. No runtime dependency was added.

## Verification completed

- Production Jekyll build passed; **72 content and browser tests passed**.
  Coverage includes all 18 project pairs, internal assets/links, language destinations,
  filters, carousels, native fallbacks, theme storage failures, wheel navigation,
  motion interruption and mocked form validation/success/failure/duplicate prevention.
  No contact messages were sent.
- **180 axe scans passed**: all 42 rendered pages in both themes at 390px and
  1440px, plus open-menu and open-dialog states. Artifact: `artifacts/accessibility.json`.
- An additional **48 responsive/runtime states** passed at 320, 390, 768, 900,
  901 and 1440px: no horizontal overflow or JavaScript/console errors. English and
  Polish, both themes, enlarged text, keyboard focus and forced colors were checked
  through browser tests and visual inspection.
- Dialog keyboard opening, Escape, focus return and complete original-image
  proportions passed in eight language/theme/viewport combinations. Mobile and
  desktop screenshots were inspected; the portrait and existing image frames retain
  their approved appearance.
- All 42 pages passed duplicate-ID, nested-interactive-element and mixed-content
  checks. The 40 indexable pages have unique titles. Canonicals, descriptions,
  language attributes, hreflang destinations, social-image paths, sitemap coverage
  and both noindex 404 pages passed the rendered content suite. No SEO rewrite or
  speculative schema was necessary.
- OSV returned no known vulnerability matches for the 40 checked locked Ruby and
  direct Python build/test package versions. Report: `artifacts/quality-audit/dependencies.json`.
  The site ships no third-party client library or downloaded font.
- CI YAML and the pinned axe download checksum were validated locally. The new
  audit command passed locally; the remote GitHub runner has not been executed here.

## Production-only and human checks

The public domain still serves the earlier site. Its HTTPS response returned 200
with HSTS and a 600-second cache policy. This does not verify the redesigned release.
Keep GitHub Pages HTTPS enforcement enabled; see
[GitHub's HTTPS guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).

CrUX/real-user INP and post-release Core Web Vitals are unavailable for the local
preview; the PageSpeed API request was quota-limited. Check the deployed release
and subsequent field data after publication. Local-server caching/compression
warnings are not proof of a GitHub Pages delivery problem. Custom response-header
policies such as CSP require separate hosting-level verification.

Browser verification used Chromium. Native NVDA/VoiceOver and Safari/Firefox
reviews remain separate human/browser checks. The accessibility tree, keyboard
flows and automated passing results are not a substitute for those reviews.
Search Console indexation and real Formspree inbox delivery were not exercised.

## Repeat the checks

```powershell
./scripts/build.ps1
python -m unittest discover -s tests -q
python scripts/audit_accessibility.py http://127.0.0.1:4173 .tools/axe.min.js --full
```

The optional portable tools require the environment described in `README.md`.
GitHub's build workflow runs equivalent build, browser and accessibility checks and
saves the static preview, screenshots and accessibility report. Deployment remains
the separate, manual publication step.
