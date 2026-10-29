"""Browser regression check for compact validation panels.

Run Dashboard_2_0.py on port 8503, install Playwright, then run this script.
PLAYWRIGHT_CHROMIUM_EXECUTABLE can select a locally installed Chromium browser.
"""
import os
from pathlib import Path
import re

from playwright.sync_api import sync_playwright


def check_pages(page, edge_id):
    graph = next(frame for frame in page.frames if frame.url == 'about:srcdoc')
    graph.evaluate('(id) => network.emit("selectEdge", {edges:[id]})', edge_id)
    iframe = page.locator('iframe[title*="dashboard_validation_popup"]')
    iframe.wait_for(timeout=30000)
    popup = iframe.element_handle().content_frame()
    page.wait_for_timeout(1000)
    counter = popup.locator('#counter')
    match = re.fullmatch(r'Page 1 of (\d+)', counter.inner_text())
    assert match, f'Pagination failed to initialize: {counter.inner_text()!r}'
    total = int(match[1])
    assert total > 1
    for number in range(1, total):
        before = popup.locator('#content').inner_text()
        popup.locator('#next').click()
        popup.wait_for_function('(expected) => document.querySelector("#counter").textContent === expected', arg=f'Page {number + 1} of {total}')
        # Wait through the component-triggered Streamlit rerun. An immediate
        # counter change alone did not catch the original regression.
        page.wait_for_timeout(650)
        assert counter.inner_text() == f'Page {number + 1} of {total}'
        assert popup.locator('#content').inner_text() != before
        assert popup.locator('#content').inner_text().strip()
    assert popup.locator('#next').is_disabled()
    popup.locator('#previous').click()
    page.wait_for_timeout(650)
    assert counter.inner_text() == f'Page {total - 1} of {total}'
    assert page.locator('.v2-header').bounding_box()['y'] >= 0
    popup.locator('#close').click()
    page.wait_for_timeout(900)
    assert page.get_by_role('tab', name='Info', exact=True).get_attribute('aria-selected') == 'true'
    return total


def main():
    default_edge = Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')) / 'Microsoft/Edge/Application/msedge.exe'
    executable = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
    if not executable and default_edge.is_file():
        executable = str(default_edge)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({'executable_path': executable} if executable else {}))
        page = browser.new_page(viewport={'width':900, 'height':650})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(os.environ.get('DASHBOARD_V2_URL', 'http://localhost:8503'), wait_until='networkidle')
        page.get_by_role('tab', name='Info', exact=True).wait_for(timeout=60000)
        page.wait_for_timeout(1200)
        print('1970 compact panel:', check_pages(page, 'validation-edge-40'), 'pages', flush=True)
        page.get_by_role('slider').nth(0).press('End')
        page.wait_for_timeout(1500)
        print('2026 compact panel:', check_pages(page, 'validation-edge-1'), 'pages', flush=True)
        page.set_viewport_size({'width':800, 'height':600})
        page.wait_for_timeout(1500)
        graph = next(frame for frame in page.frames if frame.url == 'about:srcdoc')
        longest = graph.evaluate('''() => Object.values(network.body.edges).sort((a,b)=>(b.fromId.length+b.toId.length)-(a.fromId.length+a.toId.length))[0].id''')
        print('Long title in smaller panel:', check_pages(page, longest), 'pages', flush=True)
        assert not errors, errors
        browser.close()
        print('Next, Previous, references, reruns and Back to info passed without JavaScript errors.', flush=True)


if __name__ == '__main__':
    main()
