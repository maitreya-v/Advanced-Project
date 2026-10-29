"""Reusable horizontal-chain component and a dependency-free HTML preview."""
import json

import streamlit.components.v1 as components

from .data import ROOT

COMPONENT_DIR = ROOT / "storytelling" / "chain_component"
chain_component = components.declare_component("horizontal_chain", path=str(COMPONENT_DIR))


def chain_preview_html(chain: dict) -> str:
    payload = json.dumps(chain, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (COMPONENT_DIR / "index.html").read_text(encoding="utf-8")
    return template.replace("/* INITIAL_CHAIN */null", payload)
