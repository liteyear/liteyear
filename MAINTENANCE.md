# Profile maintenance

This repository renders the public Liteyear GitHub profile.

- `README.md`: profile copy and links. Keep release markers intact.
- `assets/`: self-contained SVG artwork. No external fonts, scripts, or image services.
- `scripts/update_releases.py`: standard-library Python 3.10+ release updater. Reads only the two explicitly listed public projects. Validates every response before replacing the release section.
- `.github/workflows/profile.yml`: refreshes daily at 10:23 UTC, on updater changes, or manually through Actions. GitHub may delay scheduled runs. GitHub can disable scheduled workflows after 60 days without repository activity; re-enable in Actions if necessary.

No personal access token or external stats account is required. The workflow uses the repository's built-in token with contents-write permission to commit a successful refresh. A request, validation, or push failure does not replace the public page with an error graphic. Check Actions if the visible snapshot date stops advancing.

Links use `releases/latest` so downloads follow the maintained release. Keep private repository details out of public copy. The older NEXP repository is intentionally not featured.

To update manually: `python3 scripts/update_releases.py`. Inspect the diff before committing. To change the artwork, edit the SVGs and inspect at desktop and mobile widths; keep equivalent alt text in the README.
