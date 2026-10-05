# Bilingual portfolio implementation

Approved specification: the user's implementation request of 28 September 2026.

## Tasks
- [x] Bilingual collection and source-grounded case studies.
- [x] Shared layouts, visual design, localization and metadata.
- [x] Accessible navigation, filters, legacy links and contact form.
- [x] Locked build, CI, documentation and verification.

## Decisions
- Work on the dedicated local `redesign/bilingual-portfolio` branch in the supplied checkout. Publication is separate.
- Keep original posts as excluded source archives to preserve provenance; the new project collection is the published content.
- Use Jekyll 4 with Sass Embedded. The portable Ruby environment required a local MSYS2 compiler for Jekyll's transitive native dependencies; both remain ignored under `.tools`.
- No production form submission during testing; mock only the external Formspree requests.

## Verification record
- Content tests failed before migration and passed after all 36 translated entries were generated.
- Initial production build succeeded using Ruby with Bundler setup directly: `bundle exec` fails on the supplied Windows path containing spaces. The sandbox also blocks Ruby's absolute glob traversal; the build required an approved escalation.
- First browser pass: filters, paired languages, legacy navigation, responsive overflow, mobile navigation, no-JS navigation and mocked form states passed.
- Rendered checks found missing filter-fragment targets; fixed by adding explicit anchors.
- Screenshot review found missing month translations. Added a failing date regression test, then fixed the nested Liquid lookup.
- Independent read-only review: no critical issues. Restored omitted original-summary validation figures in both languages, with content regression tests.
- Prevented edits during form submission to avoid clearing unsent changes on success; browser regression failed before the fix.
- Removed unused duplicated ordering/featured metadata; translated Markdown remains authoritative. Removed the one-time migration generator after completing migration to avoid reintroducing stale copy.
- Added an own-property guard to legacy redirects after reproducing unwanted navigation for `#constructor`.
- Added bilingual recovery content to the root GitHub Pages 404 fallback; no automatic language redirect.
- Axe 4.10.3 found zero WCAG 2 A/AA and 2.1 AA violations across five representative routes at 390px and 1440px (10 page/viewport combinations).
- Final production build: `scripts/build.ps1`, exit 0, Jekyll 4.4.1; lockfile includes Windows and Linux platforms.
- Final verification: `python -m unittest discover -s tests -v`, **15 tests passed**. Browser checks include 360px, 390px, 768px and 1440px widths. Post-review axe audit also passed all 10 combinations.
- Visually reviewed final desktop, tablet and Polish mobile homepage screenshots, mobile collection, and Polish case-study layout. All screenshot images loaded successfully.
- `git diff --check` passed. Local preview returns HTTP 200 for English and Polish homepages at http://127.0.0.1:4173/.
- Kept the local redesign branch and working changes for preview review. No commit, merge, push, DNS change, production form submission or publication was performed. CI workflow definitions are prepared but have not run on GitHub.


## Visual refinement - 28 September 2026
Approved light/dark themes, original figure colours, centred case studies, no visible dates, clearer hero, original portrait and 17-project carousel. Regression tests first failed for missing theme controls and visible dates. Implementation complete; build and visual verification pending. Ruling: retain all screenshot content (including FedEx source slide), removing the prior crop to meet complete-image requirement.

Verification: production Jekyll build passed; 18 tests passed, including theme persistence, unavailable storage, pre-main-script theme, carousel wrap and no-JS fallback, bilingual content and mocked forms. Axe: 20 page/theme/viewport audits, zero violations. Screenshots inspected in both themes, including Polish mobile and white diagram panels. Independent refinement review: no blocking defects. Local preview is current; no publication performed.

## Header and figure corrections
Sun/moon action icon now follows EN/PL, visible outside mobile menu. Removed portrait CSS backing (source PNG already transparent). Removed original-image controls and linked project breadcrumb/category to index/filter. Figures now reserve natural height and use width calculated from source aspect ratio with 620px cover / 720px supporting height targets; no crop or stretching. Asset URLs carry build version to avoid stale preview CSS/JS. Regression covers both reported projects in EN/PL and mobile/desktop, category filtering and header placement.

## Category browsing and header polish
Grouped desktop nav beside language divider; unboxed sun/moon action; subtle theme-aware portrait card. Carousel counts visually hidden, accessible announcement retained. Category filter writes validated category query to project links and preserves it through related cards/language switches; All/direct links use full portfolio. Regression first failed for missing category context, then passed. Production build and 20 tests passed; 20 axe audits zero violations; desktop/mobile screenshots checked. Nothing published.

Card simplification: portrait frame increased to 338px (300px source image plus padding); removed photo corner arrows and repeated card CTA; visible collection counts removed in both languages and homepage all-project link. Filter result announcement remains screen-reader-only. Production build and 20 tests passed; collection screenshot checked.

Homepage reordered as requested: hero, About, Expertise, Selected works, Contact. EN/PL section numbering updated; production build and rendered order verified in both languages.

About layout refined: shared heading above portrait/biography, centred 960px section, 48px desktop gap, top-aligned text, thin oval portrait frame replacing square card. Mobile stacks portrait and biography. Production build passed; desktop dark and Polish mobile light screenshots visually checked.

## 29 September - text-first projects and one-page rhythm
Confirmed user preference: left-aligned descriptions, square clickable pictures below, About retained before Contact. All project images now metadata-driven thumbnail galleries; dialog supports Escape, close button, focus return and native non-JS image links. Compact category-labelled related cards show 4/2/1 across desktop/tablet/mobile. Contact arrows removed; light header distinct; copyright moved under identity and Back to top emphasized. Homepage order Hero/Expertise/Selected/About/Contact, desktop proximity snap with natural tall sections; mobile and reduced-motion scrolling unaffected. Homepage Projects and hero CTA scroll to selected section. Production build passed; 22 tests passed; 20 axe page audits plus open-dialog audit zero violations. Desktop scroll progression and image dialog visually inspected, EN/PL mobile/desktop captures refreshed. Independent review found no blocking issue. Preview current, nothing published.

Exact anchor alignment and wheel stepping: live header-height CSS variable replaces fixed offsets; desktop wheel gestures move one section with an animation/inertia guard, preserving native scrolling for tall content/forms, mobile and reduced-motion. Removed All projects arrows. Production build passed. Initial full-suite filter click timed out during abnormally long run; clean rerun passed all 23 tests in 32.5s. Separate down/up wheel checks across Expertise/Selected/About/Contact measured zero-pixel section/header gap.

Follow-up scrolling audit found and fixed two edge cases: mobile menu close now synchronously refreshes header offset before anchor navigation (previously ~71px gap); footer participates in homepage snap positions so wheel scrolling can reach it. Added regression for mobile Projects/About/Contact and desktop footer reachability; targeted test passed. Seven-event rapid wheel burst stayed on the next section.

Homepage carousel added: starts with four featured projects, then remaining projects in editorial order; left/right arrows wrap through all 18, one card per click. Shared carousel supports 4/2/1 desktop/tablet/mobile; homepage ignores category context, case-study carousels retain it. No-JS fallback keeps four selected projects. Added EN/PL full-cycle/previous/responsive regression; 25 tests passed, production build passed, desktop arrows visually inspected.
