"""Optional local axe audit: requires axe.min.js downloaded from Deque's axe-core.

Usage: python scripts/audit_accessibility.py http://127.0.0.1:4173 .tools/axe.min.js [--full]
This does not send form data or use a third-party auditing service.
"""
import json
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

base, axe_path = sys.argv[1:3]
routes = ['/', '/pl/', '/projects/', '/pl/projects/energy-techno-economics/', '/404.html']
if '--full' in sys.argv:
    site = Path(__file__).resolve().parents[1] / '_site'
    routes = sorted('/' + p.relative_to(site).as_posix().removesuffix('index.html')
                    for p in site.rglob('index.html')) + ['/404.html', '/pl/404.html']
results = []
def audit_state(page, theme, route, width, state='page'):
    audit = page.evaluate("async () => await axe.run(document, {runOnly: {type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}, rules: {'label-content-name-mismatch': {enabled: true}}})")
    violations = [{'id': v['id'], 'impact': v['impact'], 'nodes': [n['target'] for n in v['nodes']]} for v in audit['violations']]
    results.append({'theme': theme, 'route': route, 'width': width, 'state': state, 'violations': violations})

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(reduced_motion="reduce")
    for theme in ['dark', 'light']:
        for width in [390, 1440]:
            page.set_viewport_size({'width': width, 'height': 1000})
            for route in routes:
                page.goto(base.rstrip('/') + route)
                page.evaluate("localStorage.removeItem('portfolio-theme')")
                page.reload()
                if theme == 'light':
                    page.locator('[data-theme-toggle]').click()
                if route in ['/', '/pl/']:
                    page.wait_for_function("!document.documentElement.hasAttribute('data-hero-entrance')", timeout=6000)
                page.add_script_tag(path=axe_path)
                audit_state(page, theme, route, width)
                if width == 390 and route in ['/', '/pl/']:
                    page.locator('[data-menu-toggle]').click()
                    audit_state(page, theme, route, width, 'open-menu')
                    page.keyboard.press('Escape')
                if route in ['/projects/energy-techno-economics/', '/pl/projects/energy-techno-economics/']:
                    page.locator('[data-image-preview]').first.click()
                    page.wait_for_function("document.querySelector('dialog img').complete")
                    audit_state(page, theme, route, width, 'open-dialog')
                    page.keyboard.press('Escape')
    browser.close()
out = Path('artifacts/accessibility.json')
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps({'scans': len(results), 'failures': [r for r in results if r['violations']]}, indent=2))
sys.exit(any(r['violations'] for r in results))
