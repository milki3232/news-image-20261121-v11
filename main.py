import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
DST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output") / "entry.png"

DST.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, DST)
print(f"Wrote {DST} ({DST.stat().st_size} bytes)")
