# MoSuBi v2

Clean-slate redesign (Cuong, 2026-11-11). Free for everyone, no charts, no usage logging. Subi the Pocket Coach tells people what to do.

- `src/app.html`: the app source (one file; `/*__DATA__*/null` is filled at build time).
- `build.py`: run `python3 build.py`. It reads the verified data (value-tracker/services.json, app-prototype/*.json), lifts logos, category names, popular list and sourced price news from the v1 app, adds `data/additions.json`, and writes:
  - `mosubi.html`: standalone file that opens in any browser.
  - `mosubi-artifact.html`: the same page without the document shell, published at https://claude.ai/artifact/7AfgjSdkT8BAcvBSP8t4bk
- `data/additions.json`: v2-only data (Crunchyroll, the young-adult Popular order).
- `subi-concept/`: the character and screen concept canvas (https://claude.ai/artifact/SsLZxZTY5Z4HcWskXzK5Nt).

The v1 app (app-prototype/) and the public GitHub Pages site are untouched. Ask Cuong before putting v2 on the public site.
