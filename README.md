# news-image-20261121-v11

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/milki3232/news-image-20261121-v11/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/milki3232/news-image-20261121-v11/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the make.fun bounty **"Sum up 21 November's world news in one image"**
(contest id `news-image-20261121`).

The image summarises world news from Saturday, 21 November 2026 in a single
frame: the stories that dominated the day, condensed into one visual.

## Contents

    entry.png   the final image (77802 bytes, PNG)
    main.py     copies entry.png into the runner's output directory
    README.md   this file
    LICENSE     MIT

## How to run

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py

The script writes `out/entry.png` and exits 0. `MAKEFUN_OUTPUT_DIR` defaults to
`/output` when it is not set, which is what the make.fun runner provides.

## How it works

`main.py` is a single-pass copy with integrity gates around it, so a broken
payload fails loudly instead of silently producing a bad artifact:

1. **Locate the source.** `entry.png` is resolved relative to `main.py` itself
   (`Path(__file__).resolve().parent`), not the current working directory, so
   the script works no matter where it is invoked from.
2. **Validate before touching the output.** The source must exist, be a regular
   file, be non-empty, be no larger than 1 MiB (1048576 bytes), and start with
   the 8-byte PNG signature `89 50 4E 47 0D 0A 1A 0A`. Any failure prints a
   specific message to stderr and exits 1 without writing anything.
3. **Prepare the output directory.** `MAKEFUN_OUTPUT_DIR` is read from the
   environment (default `/output`), `~` is expanded, and the directory is
   created recursively with `mkdir(parents=True, exist_ok=True)`. A path that
   exists but is not a directory is rejected.
4. **Copy.** `shutil.copyfile` streams the bytes from source to destination.
5. **Verify by read-back.** Both files are re-read from disk and hashed with
   SHA-256 in 64 KiB chunks; the two digests must match. A mismatch is reported
   with both digests and exits 1.

Because the payload is copied byte-for-byte and never re-encoded, the output is
deterministic: repeated runs produce a file with the same SHA-256 as `entry.png`.

## Requirements

Python 3.13, standard library only. No network access, no third-party packages.

## Verification

    sha256sum entry.png
    # 7bc44bd8946044b8d3aa9a30422927e6f8f286ce1d027149eed6cf7fc864b7da

## License

MIT, see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
