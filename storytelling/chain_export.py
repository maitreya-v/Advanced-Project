"""Export saved chains with all navigation and story text available offline."""
from html import escape

from .chain_store import validate_saved_chains
from .chain_view import chain_preview_html


def saved_chains_html(record: dict, *, snapshots: dict | None = None) -> str:
    validate_saved_chains(record, snapshots)
    title = escape(record["name"])
    frames = []
    for index, chain in enumerate(record["chains"]):
        scope = chain["scenario"]
        label = f"{scope['year']} · Age {scope['age']}"
        if len(record["chains"]) == 2:
            label = ("A" if index == 0 else "B") + " · " + label
        frames.append(f'<section><h2>{escape(label)}</h2><iframe title="{escape(label, quote=True)}" '
                      f'srcdoc="{escape(chain_preview_html(chain), quote=True)}"></iframe></section>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>
* {{ box-sizing:border-box; }} body {{ margin:0; background:#edf2f5; color:#173248; font-family:system-ui,sans-serif; }}
main {{ max-width:1380px; margin:auto; padding:24px; }} h1 {{ font-size:26px; margin:0 0 8px; }}
header p {{ font-size:13px; color:#637b8c; margin:6px 0; }} h2 {{ font-size:14px; margin:20px 0 6px; }}
iframe {{ display:block; border:0; width:100%; min-height:550px; background:white; border-radius:12px; }}
</style></head><body><main><header><h1>{title}</h1>
<p>Saved story chains · select arrows or use Previous / Next. This file works offline.</p>
<p>Each chain preserves its own scenario. Strengths are authored model values.</p></header>
{''.join(frames)}</main><script>
const frames = Array.from(document.querySelectorAll('iframe'));
window.addEventListener('message', event => {{
  const frame = frames.find(item => item.contentWindow === event.source);
  if (!frame || event.data?.type !== 'streamlit:setFrameHeight' || !event.data.isStreamlitMessage) return;
  const height = event.data.height;
  if (Number.isFinite(height) && height > 0 && height < 20000) frame.style.height = height + 'px';
}});
</script></body></html>"""
