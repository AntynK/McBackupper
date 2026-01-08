"""
Small script for compilation.
Make sure to install gettext (visit https://www.gnu.org/software/gettext/).
"""

import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent
po_files = ROOT_DIR.rglob("*.po")
for input_file in po_files:
    output_file = input_file.with_suffix(".mo")
    subprocess.run(
        ["msgfmt", "-o", str(output_file.resolve()), str(input_file.resolve())]
    )
