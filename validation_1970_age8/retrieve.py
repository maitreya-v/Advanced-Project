"""Offline 1970 validation: only the four supplied PDFs are in scope."""
from pathlib import Path
import runpy, sys
sys.dont_write_bytecode = True
if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "build_report.py"), run_name="__main__")
