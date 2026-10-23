# Subscription Keeper (prototype)

A clickable prototype that helps people track their subscriptions, see what they actually use, and find cheaper options.

Open it at https://cquach1004.github.io/Subscription-keeper/

- Everything runs in the browser. Each visitor's list is saved only in their own browser.
- `index.html` is a single self-contained file built from the prototype source, with the service catalog inlined.
- Prices are US list prices checked in October 2026; "not confirmed" marks prices taken from news or review sites.

## Repository layout

| Path | What it is |
| --- | --- |
| `index.html` | The live public site (GitHub Pages). A generated file: don't edit it by hand. |
| `app-prototype/index.html` | The app source (HTML, CSS and JavaScript in one file). Make app changes here. |
| `app-prototype/alternatives.json`, `explore-extra.json`, `location-prices.json` | Alternatives, Explore categories and location-specific prices. |
| `app-prototype/regional.json` | Regional providers shown only in the states they serve. Generated from `app-prototype/regional/`. |
| `app-prototype/regional/` | One JSON file and research report per US region, `approved.txt` (regions approved for the app), `queue.txt` (regions still to research) and `merge_regional.py`. |
| `app-prototype/standalone/build_standalone.py` | Builds the self-contained copy that becomes the public site. |
| `app-prototype/site/index.html` | An older copy of the public site, kept for reference. |
| `value-tracker/` | The price catalog: `services.json` (source of truth for prices), `build_services.py` (generates it), `value-tracker.html`, and weekly price-check reports in `price-checks/`. See `value-tracker/README.md`. |

## Rebuilding

Python 3, no extra packages. Run from the repository root:

```sh
# 1. Only if the catalog changed (edit build_services.py, then regenerate):
python3 value-tracker/build_services.py value-tracker/services.json

# 2. Only if a region file or approved.txt changed:
python3 app-prototype/regional/merge_regional.py

# 3. Build the standalone copy and make it the public site:
python3 app-prototype/standalone/build_standalone.py
cp app-prototype/standalone/subscription-keeper.html index.html
```

The app source fetches its JSON files, so open the built `index.html` to try it locally rather than `app-prototype/index.html`.

## Working together

- Work on your own branch and open a pull request; the other person reviews before merging.
- Merging into `main` updates the public site within a few minutes, so only merge a rebuilt `index.html` once Cuong has approved it going live.
- Price changes need Cuong's approval before they go into `services.json`.
