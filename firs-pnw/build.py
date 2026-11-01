#!/usr/bin/env python3
"""
Build FIRS PNW without make: the Makefile's grf chain (lang, nml, graphics, nmlc), skipping the HTML docs.

    python build.py              # generated/firs-pnw.grf
    python build.py --install    # ... and copy it into OpenTTD's newgrf folder
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRF = ROOT / "generated" / "firs-pnw.grf"
NEWGRF = Path(r"G:\Google Drive\Documents\OpenTTD\newgrf")


def run(*args):
    print(">", " ".join(str(a) for a in args))
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    for script in ("render_lang.py", "render_nml.py", "render_graphics.py"):
        run(f"src/{script}", "", "")  # empty TEST_INDUSTRY and NO_MP, as the Makefile passes them
    run("-c", "import sys; from nml.main import run; sys.argv[0] = 'nmlc'; run()",
        "-c", "-l", "generated/lang", "--verbosity=4", "--no-optimisation-warning", f"--grf={GRF}", "generated/firs.nml")
    if "--install" in sys.argv:
        shutil.copy2(GRF, NEWGRF / GRF.name)
        print(f"installed {NEWGRF / GRF.name}")


if __name__ == "__main__":
    main()
