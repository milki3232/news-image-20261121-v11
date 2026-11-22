#!/usr/bin/env python3
"""make.fun entry: news-image-20261121

Copies the packaged entry.png into the output directory requested by the
runner. The output directory is taken from the MAKEFUN_OUTPUT_DIR environment
variable and defaults to /output.

Integrity checks performed before any copy happens:
  * entry.png exists and is a regular file
  * the file starts with the 8-byte PNG signature
  * the file is not larger than 1 MiB (1048576 bytes)

Standard library only, no network access.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"

# 8-byte PNG signature: \x89 P N G \r \n \x1a \n
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_SIZE_BYTES = 1024 * 1024  # 1 MiB
CHUNK_SIZE = 64 * 1024


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a file, read back from disk."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


class EntryError(Exception):
    """Raised when the entry payload fails validation."""


def validate_source(source: Path) -> int:
    """Validate the source image and return its size in bytes."""
    if not source.exists():
        raise EntryError(f"source image not found: {source}")
    if not source.is_file():
        raise EntryError(f"source image is not a regular file: {source}")

    size = source.stat().st_size
    if size == 0:
        raise EntryError(f"source image is empty: {source}")

    if size > MAX_SIZE_BYTES:
        raise EntryError(
            f"source image is too large: {size} bytes "
            f"(limit {MAX_SIZE_BYTES} bytes / 1 MiB)"
        )

    with source.open("rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise EntryError(
            f"source image is not a PNG file: bad header {header!r} "
            f"(expected {PNG_SIGNATURE!r})"
        )

    return size


def resolve_output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    if not raw or not raw.strip():
        raw = DEFAULT_OUTPUT_DIR
    return Path(raw).expanduser()


def main() -> int:
    source = Path(__file__).resolve().parent / OUTPUT_NAME

    try:
        size = validate_source(source)
    except EntryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_dir = resolve_output_dir()
    destination = out_dir / OUTPUT_NAME

    if out_dir.exists() and not out_dir.is_dir():
        print(
            f"error: output path exists but is not a directory: {out_dir}",
            file=sys.stderr,
        )
        return 1

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {out_dir}: {exc}", file=sys.stderr)
        return 1

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        print(f"error: cannot write {destination}: {exc}", file=sys.stderr)
        return 1

    # Read the written file back from disk and compare digests with the source.
    try:
        source_digest = sha256_file(source)
        written_digest = sha256_file(destination)
    except OSError as exc:
        print(f"error: cannot verify {destination}: {exc}", file=sys.stderr)
        return 1

    if source_digest != written_digest:
        print(
            "error: integrity check failed, written file differs from source\n"
            f"  source {source}: {source_digest}\n"
            f"  written {destination}: {written_digest}",
            file=sys.stderr,
        )
        return 1

    print(f"validated {source} ({size} bytes, PNG signature ok)")
    print(f"copied {source} -> {destination}")
    print(f"sha256 verified: {source_digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
