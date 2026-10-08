# Updating project content

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
   assigned; do not reuse them. Update project-count tests and collection metadata when adding projects;
   keep the original migration IDs intact. The visible result count is generated automatically.
5. Store original images in `img/portfolio/` with unique filenames. Add their paths
   to project metadata, then run `python scripts/optimize_images.py` after installing
   the development requirements. To process only new images, pass their paths:
   `python scripts/optimize_images.py img/portfolio/new-image.png`.
   Commit both generated WebP files and `_data/images.yml`.
6. Add translated gallery alternative text under `alt.en` and `alt.pl`. Retain
   technical labels inside original source figures; the gallery explains this.

Interface labels and biography text are translated in `_data/i18n.yml`. Keep English and Polish keys consistent.
