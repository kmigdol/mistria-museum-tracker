# Fields of Mistria — Museum Tracker

### ▶ [Open the tracker](https://kmigdol.github.io/mistria-museum-tracker/)

A single-page tracker for the [Fields of Mistria](https://fieldsofmistria.com/) museum: all **82 sets / 409 donations** across the Fish, Insects, Flora and Archaeology wings, with the season, weather, time, location and method for every item.

## What it does

- **Tick items off** — click anywhere on a row. Progress is saved in your browser (`localStorage`) and survives reloads.
- **Set today's season and weather** — invalid combinations grey out (no rain in Winter, no snow anywhere else). Items you can get right now are highlighted, and the stat tile counts the *time-limited* ones you can only get in these conditions.
- **Filter by location** — 17 places: overworld areas, water types, the five mine layers, apiary/terrarium. Items that spawn anywhere are tagged into every area, so filtering to The Beach still shows the wandering bugs and any-area dig spots.
- **Only time-limited** — the 172 items that are season-restricted or weather-locked. Tick this together with *Only what I can get today* to see exactly what today is your one chance at.
- **Search** by item, location or method — `ocean`, `fish trap`, `giant`, `pheromone`.
- **Export / Import** — progress as a code you can paste between browsers.

Everything is in one self-contained `index.html`, including all 409 item sprites as inline data URIs. No build step, no dependencies, works offline.

## Hosting

**GitHub Pages:** Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`. The `.nojekyll` file keeps Pages from touching anything.

**Vercel:** import the repo at [vercel.com/new](https://vercel.com/new). No framework, no build command, output directory `.` — `vercel.json` is already here.

## Analytics

Page views go to [GoatCounter](https://www.goatcounter.com) — cookieless, no personal data,
no tracking across sites, so there's no consent banner to click. Dashboard:
[kayleigh.goatcounter.com](https://kayleigh.goatcounter.com). The snippet lives in
`build/template.html`, so change it there and rebuild, not in `index.html`.

It ignores localhost, so local testing never shows up. To skip your own visits on the live
site, run `localStorage.setItem('skipgc', 't')` in the browser console once.

## Rebuilding the data

`index.html` is generated. The source data lives in `data/*.json` (one file per wing, item-level season/weather/time/location/method/notes), and `build/` holds the page template, the sprite icons, and the scripts:

```bash
cd build && python3 build.py   # writes ../index.html
```

- `template.html` — the page, with `__DATA__` and `__ICONS__` placeholders
- `tag.py` — maps each item's free-text location to the filter tags
- `build.py` — merges data + icons + fish sizes, applies the in-game set order, writes `index.html`

Data was pulled per-item from the [Fields of Mistria Wiki](https://fieldsofmistria.wiki.gg/wiki/Museum) infoboxes (not the summary tables, which are incomplete) via the MediaWiki API. Item sprites are from the same wiki.

## Notes on the data

- The wiki records **no time-of-day for fish**, so every fish shows "Any" — that's missing data, not a claim they bite at 3am. Insects have real time windows.
- Mine floor ranges come from the wiki's biome-to-floor mapping; individual pages name only the biome.
- Insects wing set order follows the in-game museum. The other three wings follow the wiki's order.

Not affiliated with NPC Studio. Game data © its respective owners; wiki content under the [wiki.gg](https://fieldsofmistria.wiki.gg) licence.
