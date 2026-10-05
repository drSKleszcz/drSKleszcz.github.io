
# Sławosz Kleszcz - bilingual engineering portfolio

Static Jekyll portfolio at **https://www.drskleszcz.pl**, with English at `/`
and Polish at `/pl/`. It uses shared Liquid layouts, plain CSS and small
progressively enhanced JavaScript modules. No CMS or application server is needed.

## Run locally

Install Ruby 3.3 (RubyInstaller **with Devkit** on Windows) and Bundler, then:

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open http://127.0.0.1:4000. For a production build:

```sh
JEKYLL_ENV=production bundle exec jekyll build
```

On PowerShell use `$env:JEKYLL_ENV = 'production'` before the build command.
The supplied checkout also has ignored portable tools: dot-source
`./scripts/local-env.ps1` to use them without changing your machine's PATH.
For this Windows checkout, run `./scripts/build.ps1` to avoid Bundler's
`bundle exec` quoting issue when the installation path contains spaces.
The helper is optional; ordinary Ruby/Python installations work without it.

## Edit or add a project

1. Edit the paired Markdown files in `_projects/en/` and `_projects/pl/`.
   Each has four sections: challenge, contribution, approach and results.
2. Shared facts live in `_data/projects.yml`, keyed by a stable project slug.
   This includes organization, source date, category, image, gallery and references.
3. To add a project, add its metadata and both language files. Set the same
   `project_id` and `translation_key`, `layout: project`, the appropriate `lang`,
   and explicit permalinks `/projects/<slug>/` and `/pl/projects/<slug>/`.
   `order` controls listing order; `featured: 1` through `4` selects homepage cards;
   use `featured: 0` otherwise. Keep these editorial values consistent in both files.
4. The categories are `engineering`, `simulation`, `analysis` and `software`.
   Set `legacy_id` only when migrating an old modal. IDs 1–8 and 10–19 are already
   assigned; do not reuse them. Update the migration count tests and translated
   collection counts when intentionally growing the portfolio beyond 18 projects.
5. Store original images in `img/portfolio/` with unique filenames. Add their paths
   to project metadata, then run `python scripts/optimize_images.py` after installing
   the development requirements. Commit both generated WebP files and `_data/images.yml`.
6. Add translated gallery alternative text under `alt.en` and `alt.pl`. Retain
   technical labels inside original source figures; the gallery explains this.

Image presentation uses `media_type: photo`, `technical` or `screen`. All project
images appear automatically below the Markdown description: the main `image` first,
then `gallery` entries in metadata order. Compact previews keep technical figures in
their original colours on white panels. Clicking opens an accessible image dialog;
without JavaScript, the link opens the original file. No inline figure includes are needed.
The project index groups rows into category chapters in the order listed above. A
category filter shows only its chapter; without JavaScript, all chapters remain visible.
The four `featured` projects retain their emphasis on the homepage only.
Diagram and screenshot frames follow the selected theme while retaining original
image colours. Optional `crop: engine` or `crop: fedex` metadata trims only the
preview through CSS; the image dialog continues to open the original source file.
The header theme switch defaults to dark and remembers light/dark across both languages.
The dependency-free [motion system](docs/motion-system.md) defines hero, navigation,
carousel and media feedback, with keyboard and reduced-motion alternatives.
Project dates remain source metadata but are not displayed. The homepage uses desktop
CSS proximity snapping plus one-section wheel gestures on desktop. Wheel gestures remain native inside tall sections and form fields; mobile and reduced-motion settings use normal scrolling. Header offsets follow the measured sticky-header height.

Headings, navigation, biography, form messages and other interface copy live in
`_data/i18n.yml`. Preserve matching keys in both languages. No automatic language
redirect is used; the language switch always points to the equivalent page.

Original `_posts` remain as excluded editorial source archives. They do not build
into the site. The translated Markdown files are the authoritative editorial content.
The excluded legacy theme files are retained for provenance and are not loaded by
the new layouts. There is no public blog or generated legacy feed.

## Verification

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
bundle exec jekyll build
python -m unittest discover -s tests -v
```

The tests check bilingual completeness, all rendered links and images, metadata,
the sitemap, legacy fragment redirects, filters, mobile navigation and overflow,
no-JavaScript access, and contact validation/success/error/duplicate prevention.
Formspree requests are intercepted by the browser tests: **no email is sent**.
Review screenshots are saved in `artifacts/screenshots/` (ignored by Git).

The build workflow also runs axe (pinned and integrity checked) against every
rendered page in both themes at mobile and desktop widths. Local equivalent:
`python scripts/audit_accessibility.py http://127.0.0.1:4173 .tools/axe.min.js --full`.
Its report is saved in `artifacts/accessibility.json`. This includes WCAG 2.2,
best-practice rules, and the explicit Label in Name check; automated passing
results do not replace a screen-reader review.

The existing Formspree endpoint is configured in `_config.yml`. It remains an
external service; browser tests verify our behavior rather than inbox delivery.
Without JavaScript, the form uses normal POST submission and browser validation.
Without JavaScript, navigation, all project cards and language links remain visible.
Legacy `#portfolioModal-N` links redirect through JavaScript; homepage section
anchors for portfolio, software, analysis, projects, about, contact and CFD remain.
GitHub Pages uses the root `404.html` for unknown addresses in either language;
that fallback therefore provides recovery text and links in both English and Polish.
The dedicated `/pl/404.html` is also available entirely in Polish.

## Preview and publication

`build.yml` builds and tests every push/PR and uploads a static preview and screenshots.
It does not deploy. `deploy.yml` is a **manual** workflow for the reviewed version.

After the preview is approved:

1. In repository Settings → Pages, use **GitHub Actions** as the source before
   merging if branch-based publishing is still enabled. Otherwise GitHub may deploy
   a merge through its old branch-based pipeline independently of these workflows.
2. Merge the reviewed branch into the intended publishing branch.
3. Confirm the custom domain remains `www.drskleszcz.pl` and HTTPS is enforced.
4. Run **Publish approved portfolio** for the approved branch/commit.
5. Verify HTTPS, English and Polish homepages, a case study in each language,
   language switching, images, canonical URLs and a legacy modal link. A real
   form-delivery check requires an explicitly authorized test message.

To roll back, run the manual workflow for a reviewed rollback commit. No DNS or
hosting migration is part of this redesign. Never upload `.tools`, `vendor`,
test artifacts, or the whole checkout; deploy only the generated `_site` directory.

Category browsing uses `?category=engineering` (or simulation, analysis, software) on project URLs. Filtered index links and related cards preserve this context, including language switches; direct project URLs default to all projects. Canonical URLs remain query-free.
