# The Sunday Ledger — news-image-20261122

Entry for the make.fun bounty: https://make.fun/bounty/news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122-v1/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122-v1/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One page that sums up the world's news of **Sunday 22 November 2026**:
24 stories, 5 regions, every one dated Sunday 22 November 2026 — a COP31
deal package awaiting its Sunday approval session in Antalya, a drone
strike on a Russia-bound ship in the Gulf of Finland, and 23,000 German
metalworkers called out on strike, plus briefs, a numbered world map and
an itemised DATE CHECK box listing the tempting stories that were *not*
Sunday's news.

## How it works

- `draw.py` renders `entry.png` (1024×1024) with Pillow. It is fully
  deterministic — no randomness, no clock, no network — so two runs
  produce byte-identical output.
- `main.py` validates `entry.png` (PNG signature, dimensions ≤1024×1024,
  size ≤1 MiB) and copies it byte-identically to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Run

```sh
python3 draw.py   # regenerate entry.png
python3 main.py   # validate + copy to the output dir
```

Sources for every story are listed in `SOURCES.md`.
