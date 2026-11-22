# news-image-20261121

Entry for make.fun's bounty [Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121):
one image that sums up Saturday, 21 November 2026's world news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py
```

The program is Python 3.13 standard library only, runs with no network, and is
deterministic: it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`), creating the output directory if needed. Both
runs write byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
