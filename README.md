# news-image-20261121-v11

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/milki3232/news-image-20261121-v11/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/milki3232/news-image-20261121-v11/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An entry for make.fun's bounty *"Sum up 21 November's world news in one image"*.
`entry.png` is the summary: Saturday 21 November 2026, 37 stories across 9
regions, condensed into a single 1024x1024 frame.

## What the program does

`main.py` puts that image where the grader looks for it: `/output/entry.png`.

The copy is not blind. Before writing anything it checks that `entry.png` exists
beside `main.py`, is non-empty, is at most 1 MiB, starts with the PNG signature
and is exactly 1024x1024 — the four things the gate itself checks, so a bad
payload fails here instead of being rejected after upload. After copying it
re-reads both files and compares their SHA-256 digests, so a truncated or
partial write cannot pass silently.

Everything is resolved relative to `main.py` (`Path(__file__).resolve().parent`),
never the current working directory, and nothing is re-encoded: the output is
byte-for-byte the input, so repeated runs are identical.

## Run it

Python 3.13, standard library only, no network:

```sh
MAKEFUN_OUTPUT_DIR=out python main.py
```

`MAKEFUN_OUTPUT_DIR` defaults to `/output`, which is what the grader provides.

## Verify

```sh
sha256sum entry.png
# 7bc44bd8946044b8d3aa9a30422927e6f8f286ce1d027149eed6cf7fc864b7da
```

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
