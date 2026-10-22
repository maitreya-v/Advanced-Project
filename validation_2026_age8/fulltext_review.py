"""Load the explicit, hash-bound 2026 age-8 judgments."""
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validation_2026_utils import load_review

_LEDGER, _REVIEW = load_review(8)
STATUS_DEFINITIONS = _LEDGER['status_definitions']
E = _LEDGER['excerpts']

def build_review(edges):
    if [list(edge) for edge in edges] != _REVIEW['original_edges']:
        raise ValueError('Graph edges changed; reassess before rebuilding.')
    return json.loads(json.dumps(_REVIEW['edges']))
