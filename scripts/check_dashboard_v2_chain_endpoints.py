"""Browser regression for independent A/B endpoints and refreshed chain frames.

Run Dashboard_2_0.py on port 8503, install Playwright, then run this script.
PLAYWRIGHT_CHROMIUM_EXECUTABLE and DASHBOARD_V2_URL override browser and server.
"""
import os
from pathlib import Path
import tempfile
import time

from playwright.sync_api import Error as PlaywrightError, expect, sync_playwright


def choose_endpoint(page, label, value):
    control = page.get_by_role("combobox", name=label, exact=True)
    if not control.is_visible():
        page.get_by_role("button", name="Choose routes", exact=True).click()
    control.fill(value)
    page.get_by_role("option", name=value, exact=True).click()


def wait_chain(page, side, start, end):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        for frame in page.frames:
            if "horizontal_chain" not in frame.url:
                continue
            try:
                label = frame.locator(".heading strong").text_content(timeout=500)
                if label != "Scenario " + side:
                    continue
                chain = frame.evaluate("chain")
                if (chain and chain["query"]["start"] == start and chain["query"]["end"] == end
                        and frame.locator(".node-name").all_text_contents() == chain["node_ids"]):
                    return frame, chain
            except PlaywrightError:
                # Streamlit replaces the iframe when a route query changes.
                continue
        page.wait_for_timeout(100)
    frames = []
    for frame in page.frames:
        if "horizontal_chain" in frame.url:
            frames.append(frame.evaluate("({label:document.querySelector('.heading strong').textContent, query:chain?.query, nodes:chain?.node_ids})"))
    page.screenshot(path=str(Path(tempfile.gettempdir()) / "dashboard-chain-endpoint-failure.png"))
    raise AssertionError(f"Scenario {side} never displayed {start} → {end}. Rendered: {frames}. Exceptions: {page.locator('[data-testid=stException]').all_text_contents()}")


def details_mode(page, mode):
    page.get_by_role("radiogroup", name="Step details", exact=True).get_by_text(mode, exact=True).click()


def main():
    executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not executable and chrome.is_file():
        executable = str(chrome)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({"executable_path": executable} if executable else {}))
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(os.environ.get("DASHBOARD_V2_URL", "http://localhost:8503"))
        page.get_by_role("button", name="Choose routes", exact=True).wait_for(timeout=30000)
        _, original_b = wait_chain(page, "B", "Diagnosis Status", "Quality of Life")
        b, _ = wait_chain(page, "B", "Diagnosis Status", "Quality of Life")
        b.locator(".edge").nth(2).click()
        details_mode(page, "Validation")
        popup = page.frame_locator('iframe[title*="dashboard_validation_popup"]')
        expect(popup.locator("#context")).to_have_text("2026 · Age 32")

        choose_endpoint(page, "Start A", "Genetic Risk")
        wait_chain(page, "A", "Genetic Risk", "Quality of Life")
        choose_endpoint(page, "End A", "Symptom Severity")
        a, chain_a = wait_chain(page, "A", "Genetic Risk", "Symptom Severity")
        assert chain_a["node_ids"] == ["Genetic Risk", "ADHD", "Symptom Severity"]
        b, chain_b = wait_chain(page, "B", "Diagnosis Status", "Quality of Life")
        assert chain_b == original_b
        expect(b.locator(".edge").nth(2)).to_have_attribute("aria-pressed", "true")
        page.keyboard.press("Escape")
        expect(popup.locator("#context")).to_have_text("1970 · Age 8")
        expect(popup.locator("#edge-title")).to_have_text("Genetic Risk → ADHD")
        a.locator(".edge").nth(1).click()

        choose_endpoint(page, "Start B", "Treatment Access")
        wait_chain(page, "B", "Treatment Access", "Quality of Life")
        choose_endpoint(page, "End B", "Functional Impairment")
        _, chain_b = wait_chain(page, "B", "Treatment Access", "Functional Impairment")
        a, unchanged_a = wait_chain(page, "A", "Genetic Risk", "Symptom Severity")
        assert unchanged_a == chain_a
        expect(a.locator(".edge").nth(1)).to_have_attribute("aria-pressed", "true")
        page.keyboard.press("Escape")
        expect(popup.locator("#context")).to_have_text("2026 · Age 32")
        first = chain_b["steps"][0]
        expect(popup.locator("#edge-title")).to_have_text(f"{first['source']} → {first['target']}")
        print("All four endpoint controls refresh their own chain; the other side's route and step are preserved.", flush=True)

        choose_endpoint(page, "Start B", "Quality of Life")
        choose_endpoint(page, "End B", "Genetic Risk")
        page.keyboard.press("Escape")
        expect(page.get_by_text("Scenario B: No directed route from Quality of Life → Genetic Risk", exact=False)).to_be_visible()
        wait_chain(page, "A", "Genetic Risk", "Symptom Severity")
        choose_endpoint(page, "Start B", "Genetic Risk")
        choose_endpoint(page, "End B", "ADHD")
        b, chain_b = wait_chain(page, "B", "Genetic Risk", "ADHD")
        assert chain_b["node_ids"] == ["Genetic Risk", "ADHD"]
        page.keyboard.press("Escape")
        expect(popup.locator("#context")).to_have_text("2026 · Age 32")
        expect(popup.locator("#edge-title")).to_have_text("Genetic Risk → ADHD")
        print("Disconnected endpoints show a scoped message; valid endpoints restore the chain and correct evidence.", flush=True)

        page.set_viewport_size({"width": 900, "height": 650})
        details_mode(page, "Story")
        expect(page.get_by_role("tab", name="Story", exact=True)).to_have_attribute("aria-selected", "true")
        assert not page.locator('[data-testid="stException"]').count()
        assert not errors, errors
        browser.close()
        print("Story/Validation switching and compact layout passed without browser errors.", flush=True)


if __name__ == "__main__":
    main()
