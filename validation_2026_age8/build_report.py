"""Build this age-specific report from the reviewed 2026 corpus."""
from pathlib import Path
import sys
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from validation_2026_utils import build_report

if __name__ == '__main__':
    build_report(BASE)
