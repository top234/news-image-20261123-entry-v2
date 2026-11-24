# The World in One Day — v2 — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/top234/news-image-20261123-entry-v2/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/top234/news-image-20261123-entry-v2/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A make.fun entry for [news-image-20261123](https://make.fun/bounty/news-image-20261123): one 1024×1024 image summing up Monday 23 November 2026's world news.

**The World in One Day v2** is a newspaper front page rebuilt from scratch: 35 verified stories across 6 regions — 3 hero cards with rich, layered code-drawn scene illustrations leading with the day's biggest stories (COP31 collapses in Antalya, Sparta II towed from Finnish waters, Wall Street in correction), 10 smaller cards with clear mini-illustrations, a dotted world map with 13 numbered pins, a two-column list of 22 more stories, and a DATE CHECK box explaining the verification method, exclusions, and what is still to come. Every story happened, or was first reported, on its tagged day, with its source named beside it.

## Files

- `generate.py` — draws `entry.png` (1024×1024, PIL, deterministic; no network, no external assets). Written from scratch for this entry. Run `python3 generate.py` to re-render.
- `entry.png` — the rendered image (also the bundled fallback for `main.ts`).
- `main.ts` — entrypoint (Node 22 stdlib only): renders via `generate.py` when Python/PIL are available, otherwise copies the bundled `entry.png`, with PNG signature verification, IHDR 1024×1024 check, and size check.

## Verification

Every story was checked against a reputable source (Reuters, AP, AFP, GFZ, UKMTO, Yle) before use; anything unverifiable or misdated was dropped. Day tags: MON = Monday 23 Nov, SUN = Sunday 22 Nov, FRI = Friday 20 Nov, WEEK = earlier in the week. The image was rendered and inspected visually (full frame plus enlarged crops of the hero row, small cards, and map): all text legible, no clipping, overlap, or gibberish. `main.ts` was run to a temporary output directory and verified byte-identical to the bundled image.
