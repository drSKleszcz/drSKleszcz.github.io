"""Exercise rendered pages and real browser behavior; mock only remote form delivery."""
import functools
import http.server
import os
from pathlib import Path
import threading
import unittest
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect, TimeoutError as PlaywrightTimeoutError

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'

class RenderedTests(unittest.TestCase):
    def test_translations_metadata_and_internal_assets(self):
        pages = list(SITE.rglob('*.html'))
        self.assertGreaterEqual(len(pages), 42, 'Build the site first')
        for path in pages:
            soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            self.assertEqual(len(soup.select('h1')), 1, str(path))
            self.assertIn(soup.html['lang'], ['en', 'pl'])
            self.assertTrue(soup.select_one('link[rel=canonical]')['href'].startswith('https://www.drskleszcz.pl/'))
            self.assertTrue(soup.select_one('meta[name=description]')['content'])
            self.assertTrue(soup.select_one('meta[property="og:image"]')['content'].startswith('https://www.drskleszcz.pl/'))
            for alt in soup.select('link[rel=alternate][hreflang]'):
                target = SITE / urlparse(alt['href']).path.lstrip('/')
                self.assertTrue(target.is_file() or (target / 'index.html').is_file(), str(target))
            for el in soup.select('[src], a[href], link[rel=stylesheet]'):
                url = el.get('src') or el.get('href')
                parsed = urlparse(url)
                if parsed.scheme or parsed.netloc:
                    continue
                target = (SITE / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
                if not parsed.path:
                    target = path
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.is_file(), f'{path}: {url}')
                if parsed.fragment and target.suffix == '.html':
                    target_soup = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                    self.assertIsNotNone(target_soup.find(id=unquote(parsed.fragment)), f'{path}: {url}')
            for img in soup.select('img[src]'):
                self.assertTrue(img.has_attr('alt'))
                if not img.find_parent('article', class_=['project-card', 'atlas-row']):
                    self.assertTrue(img['alt'])
                self.assertGreater(int(img['width']), 0)
                self.assertGreater(int(img['height']), 0)

    def test_sitemap_contains_every_project_and_no_archive(self):
        tree = ET.parse(SITE / 'sitemap.xml')
        urls = [e.text for e in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(len(urls), 40)
        self.assertEqual(len(set(urls)), 40)
        self.assertEqual(sum('/projects/' in u and u.rstrip('/').split('/')[-1] != 'projects' for u in urls), 36)
        self.assertFalse(any('2014' in u or '404' in u for u in urls))

    def test_project_dates_are_not_displayed(self):
        for prefix, expected in [('', 'July 2023'), ('pl/', 'lipiec 2023')]:
            soup = BeautifulSoup((SITE / prefix / 'projects/energy-techno-economics/index.html').read_text(encoding='utf-8'), 'html.parser')
            self.assertNotIn(expected, soup.select_one('.project-facts').get_text(' ', strip=True))

    def test_github_fallback_offers_polish_recovery(self):
        soup = BeautifulSoup((SITE / '404.html').read_text(encoding='utf-8'), 'html.parser')
        polish = soup.select_one('section[lang=pl]')
        self.assertIsNotNone(polish)
        self.assertIsNotNone(polish.select_one('a[href="/pl/"]'))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # Navigating away deliberately cancels in-flight browser requests.
            # Other server errors must still fail visibly.
            pass

class BrowserTests(unittest.TestCase):
    def test_rounded_buttons_preserve_targets_and_form_fields(self):
        for prefix in ['', '/pl']:
            for width in [390, 768, 1440]:
                self.page.set_viewport_size({'width': width, 'height': 960})
                self.page.goto(self.base + prefix + '/')
                expect(self.page.locator('.theme-toggle')).to_be_visible()
                for selector in ['.theme-toggle'] + (['.menu-toggle'] if width <= 900 else []):
                    control = self.page.locator(selector)
                    self.assertEqual(control.evaluate('el => getComputedStyle(el).borderRadius'), '50%')
                    box = control.bounding_box()
                    self.assertEqual((box['width'], box['height']), (44, 44))
                    control.focus()
                    self.assertEqual(control.evaluate('el => getComputedStyle(el).outlineStyle'), 'solid')
                self.assertEqual(self.page.locator('.theme-toggle').evaluate('el => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
                for selector in ['.hero-actions .button', 'form .button', '.back-top', '.skip-link']:
                    self.assertEqual(self.page.locator(selector).evaluate('el => getComputedStyle(el).borderRadius'), '999px')
                for field in self.page.locator('form input:not([type=hidden]), form textarea').all():
                    self.assertEqual(field.evaluate('el => getComputedStyle(el).borderRadius'), '0px')
                self.page.goto(self.base + prefix + '/projects/')
                expect(self.page.locator('[data-filter="all"]')).to_be_visible()
                for control in self.page.locator('.filters button').all():
                    self.assertEqual(control.evaluate('el => getComputedStyle(el).borderRadius'), '999px')
                    self.assertGreaterEqual(control.bounding_box()['height'], 44)
                    self.assertTrue(control.evaluate('el => el.scrollWidth <= el.clientWidth'))
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width)

    def test_circular_dialog_and_carousel_controls_remain_operable(self):
        self.page.goto(self.base + '/projects/microclimate-control/')
        self.page.locator('[data-image-preview]').first.click()
        close = self.page.locator('[data-close-image]')
        expect(close).to_be_focused()
        self.page.wait_for_function('document.querySelector(".image-viewer").getAnimations().every(a => a.playState === "finished")')
        self.assertEqual(close.evaluate('el => getComputedStyle(el).borderRadius'), '50%')
        box = close.bounding_box()
        self.assertEqual((box['width'], box['height']), (44, 44))
        close.click()
        expect(self.page.locator('.image-viewer')).not_to_be_visible()
        for control in self.page.locator('.carousel-controls button').all():
            self.assertEqual(control.evaluate('el => getComputedStyle(el).borderRadius'), '50%')
            box = control.bounding_box()
            self.assertEqual((box['width'], box['height']), (44, 44))
        self.page.goto(self.base + '/404.html')
        for control in self.page.locator('.not-found .button, .fallback-polish .button').all():
            self.assertEqual(control.evaluate('el => getComputedStyle(el).borderRadius'), '999px')

    @classmethod
    def setUpClass(cls):
        if not (SITE / 'index.html').exists():
            raise AssertionError('Production Jekyll build required before browser tests')
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(SITE)))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [])

    def test_header_layout_is_reserved_before_deferred_script(self):
        # Slow the actual handler script: the first painted header must already
        # have its final geometry, in both languages and saved themes.
        self.page.add_init_script('''window.loadingShifts=[];
          new PerformanceObserver(list => list.getEntries().forEach(entry => {
            if (!entry.hadRecentInput) loadingShifts.push(entry.value);
          })).observe({type:'layout-shift', buffered:true});''')
        for prefix in ['', '/pl']:
            for width, theme in [(320, 'dark'), (390, 'light'), (768, 'dark'), (900, 'light'), (901, 'dark'), (1440, 'light')]:
                self.page.set_viewport_size({'width': width, 'height': 844})
                before = []
                def delay_script(route):
                    self.page.wait_for_timeout(250)
                    before.append(self.page.locator('.site-header').bounding_box())
                    route.continue_()
                self.page.route('**/assets/site.js*', delay_script)
                self.context.add_init_script(f"localStorage.setItem('portfolio-theme', '{theme}')")
                self.page.goto(self.base + prefix + '/projects/')
                self.page.wait_for_timeout(100)
                after = self.page.locator('.site-header').bounding_box()
                self.assertEqual(len(before), 1)
                self.assertAlmostEqual(before[0]['height'], after['height'], delta=1)
                self.assertLess(self.page.evaluate('loadingShifts.reduce((a,b)=>a+b,0)'), .01)
                self.page.unroute('**/assets/site.js*', delay_script)

    def test_menu_closes_when_crossing_its_desktop_breakpoint(self):
        self.page.set_viewport_size({'width': 768, 'height': 844})
        self.page.goto(self.base + '/pl/')
        toggle = self.page.locator('[data-menu-toggle]')
        toggle.click()
        expect(toggle).to_have_attribute('aria-expanded', 'true')
        self.page.set_viewport_size({'width': 901, 'height': 844})
        expect(toggle).to_have_attribute('aria-expanded', 'false')
        self.page.set_viewport_size({'width': 768, 'height': 844})
        expect(self.page.locator('#site-nav')).not_to_be_visible()

    def test_mobile_dropdown_overlays_without_changing_header_or_scroll(self):
        for prefix in ['', '/pl']:
            for width in [320, 390, 900]:
                self.page.set_viewport_size({'width': width, 'height': 844})
                self.page.goto(self.base + prefix + '/#projects')
                # Repeated fragment arrivals after resizing can still be scrolling;
                # fresh arrivals also align in a load-time animation frame.
                # Take the menu baseline only once the target reaches the header.
                self.page.wait_for_function("Math.abs(document.querySelector('#projects').getBoundingClientRect().top-document.querySelector('.site-header').getBoundingClientRect().bottom)<=1")
                header = self.page.locator('.site-header')
                before = header.bounding_box()
                scroll = self.page.evaluate('scrollY')
                toggle = self.page.locator('[data-menu-toggle]')
                toggle.click()
                expect(self.page.locator('#site-nav')).to_be_visible()
                self.assertAlmostEqual(header.bounding_box()['height'], before['height'], delta=.5)
                self.page.wait_for_function("!document.querySelector('#site-nav').getAnimations().some(a=>a.playState==='running')")
                self.assertAlmostEqual(self.page.evaluate('scrollY'), scroll, delta=1)
                box = self.page.locator('#site-nav').bounding_box()
                self.assertAlmostEqual(box['y'], before['height'], delta=1)
                links = self.page.locator('#site-nav a').all()
                self.assertTrue(all(a.bounding_box()['y'] < b.bounding_box()['y'] for a, b in zip(links, links[1:])))
                self.page.mouse.click(10, 700)
                expect(toggle).to_have_attribute('aria-expanded', 'false')
                expect(self.page.locator('#site-nav')).not_to_be_visible()
                toggle.click()
                links[0].focus()
                self.page.locator('.brand').focus()
                expect(toggle).to_have_attribute('aria-expanded', 'false')

    def test_phone_arrows_reserve_space_between_image_and_copy(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for path in ['/#projects', '/pl/#projects']:
            self.page.goto(self.base + path)
            carousel = self.page.locator('[data-carousel]')
            photo = carousel.locator('.project-card:visible .card-image').first.bounding_box()
            controls = carousel.locator('.carousel-controls').bounding_box()
            copy = carousel.locator('.project-card:visible .card-body').first.bounding_box()
            self.assertAlmostEqual(controls['y'] - photo['y'] - photo['height'], 12, delta=1)
            self.assertGreaterEqual(copy['y'] - controls['y'] - controls['height'], 11)
            self.assertTrue(carousel.locator('.carousel-controls button').evaluate_all('buttons => buttons.every(b => !b.closest("a") && b.getBoundingClientRect().height >= 44)'))
            first_url = carousel.locator('.project-card:visible a').first.get_attribute('href')
            carousel.locator('[data-next]').click()
            self.assertNotEqual(carousel.locator('.project-card:visible a').first.get_attribute('href'), first_url)
            carousel.locator('[data-prev]').click()
            self.assertEqual(carousel.locator('.project-card:visible a').first.get_attribute('href'), first_url)

    def test_phone_arrow_space_is_reserved_before_enhancement(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.route('**/assets/site.js*', lambda route: route.abort())
        for path in ['/#projects']:
            self.page.goto(self.base + path)
            slot = self.page.locator('[data-carousel] .carousel-image-slot').first
            self.assertEqual(slot.evaluate('el => el.getBoundingClientRect().height'), 68)

    def test_related_phone_pagination_replaces_arrows_below_card(self):
        self.page.emulate_media(reduced_motion='reduce')
        for prefix, hint in [('', 'Swipe to explore'), ('/pl', 'Przesuń, aby zobaczyć projekty')]:
            for width in [320, 390, 600]:
                self.page.set_viewport_size({'width': width, 'height': 844})
                self.page.goto(self.base + prefix + '/projects/microclimate-control/')
                carousel = self.page.locator('[data-carousel]')
                pagination = carousel.locator('[data-carousel-pagination]')
                self.assertEqual(pagination.count(), 1)
                expect(pagination).to_be_visible()
                expect(carousel.locator('.carousel-controls')).to_be_hidden()
                expect(pagination.locator('.swipe-hint')).to_have_text(hint)
                dots = pagination.locator('button')
                expect(dots).to_have_count(5)
                self.assertTrue(dots.evaluate_all('els => els.every(el => !el.closest("a") && el.getBoundingClientRect().width >= 44 && el.getBoundingClientRect().height >= 44)'))
                expect(pagination.locator('[aria-current=true]')).to_have_attribute('data-slide-index', '0')
                grid = carousel.locator('.project-grid')
                height = grid.bounding_box()['height']
                self.assertAlmostEqual(pagination.bounding_box()['y'] - grid.bounding_box()['y'] - height, 12, delta=1)
                self.assertEqual(carousel.locator('.project-card:visible .carousel-image-slot').evaluate('el => el.getBoundingClientRect().height'), 0)
                first_url = carousel.locator('.project-card:visible a').get_attribute('href')
                dots.nth(1).click()
                self.assertNotEqual(carousel.locator('.project-card:visible a').get_attribute('href'), first_url)
                expect(pagination.locator('[aria-current=true]')).to_have_attribute('data-slide-index', '1')
                expect(carousel.locator('[data-position]')).to_contain_text('2 / 17')
                self.assertFalse(carousel.locator('[data-position]').evaluate('el => !!el.closest("[hidden]")'))
                self.assertAlmostEqual(grid.bounding_box()['height'], height, delta=1)
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width)
            for width in [601, 1440]:
                self.page.set_viewport_size({'width': width, 'height': 1000})
                expect(pagination).to_be_hidden()
                expect(carousel.locator('.carousel-controls')).to_be_visible()

    def test_related_pagination_tracks_swipes_and_wraps(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/projects/microclimate-control/?category=engineering')
            carousel = self.page.locator('[data-carousel]')
            total = carousel.locator('.project-card[data-category=engineering]').count()
            active = carousel.locator('[data-carousel-pagination] [aria-current=true]')
            self.assertEqual(active.count(), 1)
            first_url = carousel.locator('.project-card:visible a').get_attribute('href')
            self.touch_drag(-80)
            expect(active).to_have_attribute('data-slide-index', '1')
            self.touch_drag(30)
            expect(active).to_have_attribute('data-slide-index', '1')
            self.touch_drag(80)
            expect(active).to_have_attribute('data-slide-index', '0')
            self.touch_drag(80)
            expect(active).to_have_attribute('data-slide-index', str(total - 1))
            self.touch_drag(-80)
            expect(active).to_have_attribute('data-slide-index', '0')
            self.assertEqual(carousel.locator('.project-card:visible a').get_attribute('href'), first_url)
            self.assertEqual(carousel.locator('.project-card:visible').get_attribute('data-category'), 'engineering')

    def test_related_pagination_preserves_keyboard_focus_and_single_project_state(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/projects/microclimate-control/')
        pagination = self.page.locator('[data-carousel-pagination]')
        self.assertEqual(pagination.count(), 1)
        pagination.locator('button').last.focus()
        self.page.keyboard.press('Enter')
        active = pagination.locator('[aria-current=true]')
        expect(active).to_have_attribute('data-slide-index', '4')
        expect(active).to_be_focused()
        self.assertEqual(self.page.locator('.project-card:visible').evaluate('el => el.getAnimations().length'), 0)
        self.page.set_viewport_size({'width': 601, 'height': 844})
        expect(self.page.locator('[data-next]')).to_be_focused()
        self.page.set_viewport_size({'width': 390, 'height': 844})
        expect(active).to_be_focused()
        # Exercise the one-recommendation edge case without changing project data.
        def single_card(route):
            response = route.fetch()
            soup = BeautifulSoup(response.text(), 'html.parser')
            for card in soup.select('[data-carousel] .project-card')[1:]:
                card.decompose()
            route.fulfill(response=response, body=str(soup))
        self.page.route('**/projects/microclimate-control/', single_card)
        self.page.goto(self.base + '/projects/microclimate-control/')
        expect(self.page.locator('[data-carousel] .project-card:visible')).to_have_count(1)
        expect(self.page.locator('[data-carousel-pagination]')).to_be_hidden()
        expect(self.page.locator('.carousel-controls')).to_be_hidden()

    def test_stacked_portrait_is_centered_without_resizing(self):
        for prefix in ['', '/pl']:
            for width in [320, 390, 760]:
                self.page.set_viewport_size({'width': width, 'height': 844})
                self.page.goto(self.base + prefix + '/#about')
                portrait = self.page.locator('.portrait-panel').bounding_box()
                self.assertAlmostEqual(portrait['x'] + portrait['width'] / 2, width / 2, delta=1)
                self.assertAlmostEqual(portrait['width'], 248, delta=1)

    def touch_drag(self, dx, dy=0, end=True):
        grid = self.page.locator('[data-carousel] .project-grid')
        grid.scroll_into_view_if_needed()
        box = grid.bounding_box()
        x, y = box['x'] + box['width'] / 2, max(120, box['y'] + 90)
        session = self.context.new_cdp_session(self.page)
        session.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
        for step in range(1, 5):
            session.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x + dx * step / 4, 'y': y + dy * step / 4}]})
            self.page.wait_for_timeout(25)
        if end:
            session.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            session.detach()
        return session

    def test_phone_swipes_wrap_and_keep_taps_and_vertical_scroll_native(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.emulate_media(reduced_motion='reduce')
        for path in ['/#projects', '/pl/#projects', '/projects/microclimate-control/?category=engineering', '/pl/projects/microclimate-control/?category=engineering']:
            self.page.goto(self.base + path)
            carousel = self.page.locator('[data-carousel]')
            links = carousel.locator('.project-card a').evaluate_all('links => links.map(a => a.getAttribute("href"))')
            if 'category=engineering' in path:
                links = carousel.locator('.project-card[data-category=engineering] a').evaluate_all('links => links.map(a => a.getAttribute("href"))')
            current = lambda: carousel.locator('.project-card:visible a').first.get_attribute('href')
            original_url = self.page.url
            self.assertEqual(current(), links[0])
            self.touch_drag(-90)
            self.assertEqual(current(), links[1])
            self.assertEqual(self.page.url, original_url)
            self.touch_drag(90)
            self.assertEqual(current(), links[0])
            self.touch_drag(90)
            self.assertEqual(current(), links[-1])
            self.touch_drag(-90)
            self.assertEqual(current(), links[0])
            self.touch_drag(-30)
            self.assertEqual(current(), links[0])
            self.touch_drag(0, -90)
            self.assertEqual(current(), links[0])
            self.assertEqual(self.page.url, original_url)
        # An ordinary touch tap is still a native project link.
        with self.browser.new_context(has_touch=True, viewport={'width':390, 'height':844}) as context:
            page = context.new_page()
            page.goto(self.base + '/#projects')
            page.locator('.project-card:visible a').first.tap()
            expect(page).to_have_url(self.base + '/projects/microclimate-control/')

    def test_swipe_tracks_finger_and_cleans_up_on_interruptions(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for interrupt in ['cancel', 'keyboard', 'resize', 'hidden']:
            self.page.goto(self.base + '/#projects')
            grid = self.page.locator('[data-carousel] .project-grid')
            grid.scroll_into_view_if_needed()
            first = self.page.locator('.project-card:visible').first
            initial = first.bounding_box()['x']
            original = first.locator('a').get_attribute('href')
            session = self.touch_drag(-80, end=False)
            self.assertLess(first.bounding_box()['x'], initial - 30)
            self.assertEqual(first.locator('.project-card-link').evaluate('el => getComputedStyle(el).transform'), 'none')
            self.assertEqual(grid.evaluate('el => getComputedStyle(el).overflowClipMargin'), '8px')
            if interrupt == 'keyboard':
                self.page.keyboard.press('Tab')
            elif interrupt == 'resize':
                self.page.set_viewport_size({'width': 601, 'height': 844})
            elif interrupt == 'hidden':
                self.page.evaluate("Object.defineProperty(document, 'hidden', {configurable:true, value:true}); document.dispatchEvent(new Event('visibilitychange'))")
            session.send('Input.dispatchTouchEvent', {'type':'touchCancel', 'touchPoints':[]})
            session.detach()
            self.assertEqual(self.page.locator('.project-card:visible a').first.get_attribute('href'), original)
            self.assertTrue(self.page.locator('.project-card').evaluate_all('cards=>cards.every(c=>!c.inert && !c.hasAttribute("aria-hidden") && !c.style.transform)'))
            ink_space = '32px' if interrupt == 'resize' else '20px'
            self.assertEqual(grid.evaluate('el => getComputedStyle(el).overflowClipMargin'), ink_space)
            self.page.set_viewport_size({'width': 390, 'height': 844})

    def test_animated_swipe_settles_without_retaining_finished_effects(self):
        self.page.set_viewport_size({'width':390, 'height':844})
        self.page.goto(self.base + '/#projects')
        for _ in range(2):
            session = self.touch_drag(-80, end=False)
            self.assertTrue(self.page.locator('.project-grid').evaluate("g=>g.classList.contains('is-swiping')"))
            session.send('Input.dispatchTouchEvent', {'type':'touchEnd', 'touchPoints':[]})
            session.detach()
            self.page.wait_for_function("!document.querySelector('.project-grid').classList.contains('is-swiping')")
            self.assertTrue(self.page.locator('.project-card').evaluate_all('cards=>cards.every(c=>!c.getAnimations().length && !c.style.transform && !c.inert)'))

    def test_mobile_carousel_does_not_download_hidden_opening_cards(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        requested = []
        self.page.on('request', lambda request: requested.append(request.url))
        def delay_script(route):
            self.page.wait_for_timeout(500)
            expect(self.page.locator('.featured-grid .project-card:visible')).to_have_count(1)
            route.continue_()
        self.page.route('**/assets/site.js*', delay_script)
        self.page.goto(self.base + '/')
        self.page.wait_for_timeout(200)
        for stem in ['mtt-', 'tea-', 'orficle_2-']:
            self.assertFalse(any('/assets/images/' + stem in url for url in requested), requested)
        self.page.unroute('**/assets/site.js*', delay_script)
        self.page.locator('[data-home-carousel] [data-next]').click()
        expect(self.page.locator('.featured-grid .project-card:visible').first.locator('img')).to_have_js_property('complete', True)

    def test_portrait_requests_a_variant_matching_its_display_size(self):
        for prefix in ['', '/pl']:
            for width, expected in [(412, '-480.webp'), (1440, '-640.webp')]:
                with self.browser.new_context(viewport={'width': width, 'height': 1000}, device_scale_factor=1.75) as context:
                    page = context.new_page()
                    page.goto(self.base + prefix + '/#about')
                    portrait = page.locator('.portrait-panel img')
                    portrait.scroll_into_view_if_needed()
                    page.wait_for_function("document.querySelector('.portrait-panel img').complete")
                    self.assertTrue(portrait.evaluate('image => image.currentSrc').endswith(expected))

    def test_navigation_accessible_names_include_visible_text(self):
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/projects/')
            brand = self.page.locator('.brand')
            self.assertIn(brand.locator('.brand-name > span').inner_text(), brand.get_attribute('aria-label'))
            language = self.page.locator('[data-language-switch]')
            self.assertIn(language.inner_text(), language.get_attribute('aria-label'))

    def test_modified_image_click_opens_original_in_new_tab(self):
        self.page.goto(self.base + '/projects/energy-techno-economics/')
        thumb = self.page.locator('[data-image-preview]').first
        with self.context.expect_page() as opened:
            thumb.click(modifiers=['Control'])
        original = opened.value
        original.wait_for_load_state()
        self.assertEqual(original.url, self.base + thumb.get_attribute('href'))
        expect(self.page.locator('dialog[open]')).to_have_count(0)
        original.close()

    def test_image_dialog_reserves_its_size_during_slow_original_loading(self):
        for width in [390, 1440]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            self.page.goto(self.base + '/pl/projects/energy-techno-economics/')
            before = []
            def delayed_image(route):
                self.page.wait_for_timeout(300)
                before.append(self.page.locator('dialog').bounding_box())
                route.continue_()
            self.page.route('**/img/portfolio/tea.png', delayed_image)
            self.page.locator('[data-image-preview]').first.click()
            expect(self.page.locator('dialog img')).to_have_js_property('complete', True)
            after = self.page.locator('dialog').bounding_box()
            self.assertEqual(len(before), 1)
            for key in ['width', 'height', 'x', 'y']:
                self.assertAlmostEqual(before[0][key], after[key], delta=1)
            self.page.unroute('**/img/portfolio/tea.png', delayed_image)

    def test_homepage_project_carousel(self):
        for prefix in ['', '/pl']:
            self.page.set_viewport_size({'width': 1440, 'height': 1000})
            self.page.goto(self.base + prefix + '/#projects')
            carousel = self.page.locator('#projects [data-carousel]')
            expect(carousel).to_have_count(1)
            cards = carousel.locator('.project-card:visible')
            expect(cards).to_have_count(4)
            first = cards.first.locator('a').get_attribute('href')
            self.assertIn('microclimate-control', first)
            seen = set()
            for _ in range(18):
                seen.add(cards.first.locator('a').get_attribute('href'))
                carousel.locator('[data-next]').click()
            self.assertEqual(len(seen), 18)
            self.assertEqual(cards.first.locator('a').get_attribute('href'), first)
            carousel.locator('[data-prev]').click()
            self.assertIn('automated-price-list', cards.first.locator('a').get_attribute('href'))
            self.page.set_viewport_size({'width': 768, 'height': 1000})
            expect(cards).to_have_count(2)
            self.page.set_viewport_size({'width': 390, 'height': 844})
            expect(cards).to_have_count(1)

    def test_carousel_height_stays_stable_when_browsing(self):
        self.page.emulate_media(reduced_motion='reduce')
        for width in [1440, 390]:
            self.page.set_viewport_size({'width': width, 'height': 1000})
            self.page.goto(self.base + '/pl/#projects')
            grid = self.page.locator('.featured-grid')
            heights = []
            for _ in range(18):
                heights.append(grid.bounding_box()['height'])
                self.page.locator('[data-home-carousel] [data-next]').click()
            self.assertLessEqual(max(heights) - min(heights), 1, str(heights))

    def test_enlarged_polish_text_does_not_overflow(self):
        self.page.set_viewport_size({'width': 320, 'height': 844})
        for fallback_font in [False, True]:
            self.page.goto(self.base + '/pl/')
            self.page.locator('html').evaluate("el => el.style.fontSize = '200%'")
            if fallback_font:
                # Linux falls back from Consolas to a wider monospace font.
                self.page.add_style_tag(content='.language-links {font-family: "Courier New", monospace}')
            for section in self.page.locator('main > section').all():
                section.scroll_into_view_if_needed()
                self.assertLessEqual(section.evaluate('el => el.getBoundingClientRect().right'), 320)
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 320)
            # All header controls must fit inside its gutters, even at 200% text.
            self.assertTrue(self.page.locator('.header-inner').evaluate('''header =>
                [...header.children].filter(el => getComputedStyle(el).display !== 'none' && el.id !== 'site-nav')
                  .every(el => el.getBoundingClientRect().right <= header.getBoundingClientRect().right + .1)'''))

    def test_filtered_project_return_and_language_switch(self):
        self.page.goto(self.base + '/projects/#engineering')
        self.page.locator('[data-language-switch]').click()
        expect(self.page.locator('[data-filter="engineering"]')).to_have_attribute('aria-pressed', 'true')
        self.page.locator('[data-project]:visible a').first.click()
        self.page.locator('.back-link').click()
        expect(self.page.locator('[data-filter="engineering"]')).to_have_attribute('aria-pressed', 'true')

    def test_wheel_scroll_can_reverse_immediately(self):
        self.page.set_viewport_size({'width': 1440, 'height': 900})
        self.page.goto(self.base + '/')
        self.page.mouse.wheel(0, 100)
        self.page.wait_for_timeout(100)
        self.page.mouse.wheel(0, -100)
        self.page.wait_for_timeout(1000)
        self.assertLessEqual(self.page.evaluate('window.scrollY'), 2)

    def test_reduced_motion_wheel_steps_instantly_and_reverses(self):
        self.page.set_viewport_size({'width': 1440, 'height': 900})
        self.page.emulate_media(reduced_motion='reduce')
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/')
            self.page.mouse.wheel(0, 100)
            self.page.wait_for_timeout(80)
            gap = self.page.evaluate("document.querySelector('#expertise').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
            self.assertLessEqual(abs(gap), 3, f'{prefix or "en"} first step: {gap}')
            self.page.mouse.wheel(0, -100)
            self.page.wait_for_timeout(80)
            self.assertLessEqual(self.page.evaluate('window.scrollY'), 2, f'{prefix or "en"} reversal')
            self.page.wait_for_timeout(900)
            self.page.mouse.wheel(0, 100)
            self.page.wait_for_timeout(80)
            gap = self.page.evaluate("document.querySelector('#expertise').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
            self.assertLessEqual(abs(gap), 3, f'{prefix or "en"} repeat: {gap}')

    def test_wheel_steps_from_selected_work_to_about_on_short_desktop(self):
        self.page.set_viewport_size({'width': 1280, 'height': 720})
        self.page.emulate_media(reduced_motion='reduce')
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/#projects')
            self.page.mouse.move(500, 450)
            self.page.mouse.wheel(0, 100)
            self.page.wait_for_timeout(80)
            gap = self.page.evaluate("document.querySelector('#about').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
            self.assertLessEqual(abs(gap), 3, f'{prefix or "en"} selected work step: {gap}')

    def test_wheel_up_from_contact_footer_returns_to_about_in_one_step(self):
        self.page.set_viewport_size({'width': 1280, 'height': 720})
        self.page.emulate_media(reduced_motion='reduce')
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/#contact')
            self.page.wait_for_timeout(150)
            self.page.evaluate('scrollTo({top: document.documentElement.scrollHeight, behavior: "instant"})')
            self.page.mouse.move(500, 450)
            self.page.mouse.wheel(0, -100)
            self.page.wait_for_timeout(80)
            gap = self.page.evaluate("document.querySelector('#about').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
            self.assertLessEqual(abs(gap), 3, f'{prefix or "en"} About return: {gap}')

    def test_pointer_carousel_motion_is_interruptible_and_keyboard_is_immediate(self):
        self.page.goto(self.base + '/#projects')
        next_button = self.page.locator('[data-home-carousel] [data-next]')
        next_button.click()
        self.assertTrue(self.page.locator('.featured-grid').evaluate('el => el.getAnimations({subtree:true}).some(a => a.playState === "running")'))
        next_button.click()
        self.assertIn('energy-techno-economics', self.page.locator('.featured-grid .project-card:visible a').first.get_attribute('href'))
        next_button.focus()
        self.page.keyboard.press('Enter')
        self.assertFalse(self.page.locator('.featured-grid').evaluate('el => el.getAnimations({subtree:true}).some(a => a.playState === "running")'))
        self.assertIn('orifice-calculation-software', self.page.locator('.featured-grid .project-card:visible a').first.get_attribute('href'))

    def test_reduced_motion_cancels_running_effects_and_keeps_content_visible(self):
        self.page.goto(self.base + '/#projects')
        self.page.locator('[data-home-carousel] [data-next]').click()
        self.page.emulate_media(reduced_motion='reduce')
        moving = 'el => el.getAnimations({subtree:true}).some(a => a.playState === "running" && a.effect.getKeyframes().some(frame => "transform" in frame || "clipPath" in frame || "opacity" in frame))'
        self.assertFalse(self.page.locator('main').evaluate(moving))
        self.page.locator('[data-home-carousel] [data-next]').click()
        self.assertFalse(self.page.locator('.featured-grid').evaluate(moving))
        self.page.goto(self.base + '/pl/')
        expect(self.page.locator('h1')).to_be_visible()
        self.assertTrue(self.page.locator('h1').evaluate('el => el.getAnimations({subtree:true}).some(a => a.animationName === "portfolio-sentence-fade")'))
        self.assertEqual(self.page.locator('.workflow-signal').evaluate_all('els => els.filter(el => el.getAnimations().length).length'), 0)

    def test_hover_resumes_after_keyboard_use_and_real_mouse_movement(self):
        self.page.goto(self.base + '/#projects')
        card = self.page.locator('.featured-grid .project-card-link').first
        card.hover()
        self.page.keyboard.press('Shift')
        self.assertEqual(card.evaluate('el => getComputedStyle(el).transform'), 'none')
        box = card.bounding_box()
        self.page.mouse.move(box['x'] + box['width'] / 2 + 5, box['y'] + box['height'] / 2)
        expect(self.page.locator('html')).to_have_attribute('data-input', 'pointer')
        self.page.wait_for_timeout(200)
        self.assertNotEqual(card.evaluate('el => getComputedStyle(el).transform'), 'none')

    def test_closing_mobile_menu_cancels_its_entrance(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/')
        toggle = self.page.locator('[data-menu-toggle]')
        nav = self.page.locator('#site-nav')
        toggle.click()
        nav.evaluate('el => el.getAnimations().forEach(a => a.pause())')
        toggle.click()
        expect(nav).not_to_be_visible()
        self.assertEqual(nav.evaluate('el => el.getAnimations().length'), 0)

    def test_resizing_during_carousel_movement_clears_old_positions(self):
        self.page.goto(self.base + '/#projects')
        self.page.locator('[data-home-carousel] [data-next]').click()
        grid = self.page.locator('.featured-grid')
        grid.evaluate('el => el.getAnimations({subtree:true}).forEach(a => a.pause())')
        self.page.set_viewport_size({'width': 768, 'height': 1000})
        expect(grid.locator('.project-card:visible')).to_have_count(2)
        self.assertEqual(grid.evaluate('el => el.getAnimations({subtree:true}).filter(a => a.effect.getKeyframes().some(f => "transform" in f)).length'), 0)
        self.assertEqual(grid.locator('.project-card:visible').evaluate_all('els => els.map(el => getComputedStyle(el).transform)'), ['none', 'none'])

    def test_rapid_carousel_steps_preserve_arriving_card_opacity(self):
        self.page.goto(self.base + '/#projects')
        next_button = self.page.locator('[data-home-carousel] [data-next]')
        next_button.click()
        grid = self.page.locator('.featured-grid')
        grid.evaluate('el => el.getAnimations({subtree:true}).forEach(a => {a.pause(); a.currentTime = 30})')
        arriving = grid.locator('.project-card:visible').last.element_handle()
        before = float(arriving.evaluate('el => getComputedStyle(el).opacity'))
        self.assertLess(before, 1)
        next_button.click()
        first_frame = arriving.evaluate('el => el.getAnimations()[0].effect.getKeyframes()[0]')
        self.assertAlmostEqual(float(first_frame['opacity']), before, places=3)

    def test_carousel_cards_keep_their_gap_through_a_step(self):
        for width in [1440, 768]:
            self.page.set_viewport_size({'width': width, 'height': 1000})
            self.page.goto(self.base + '/#projects')
            self.page.locator('[data-home-carousel] [data-next]').click()
            grid = self.page.locator('.featured-grid')
            for time in [0, 55, 110, 210]:
                gaps = grid.evaluate('''(el, time) => {
                    el.getAnimations({subtree:true}).forEach(a => {a.pause(); a.currentTime = time});
                    const bounds = [...el.querySelectorAll('.project-card:not([hidden])')].map(card => card.getBoundingClientRect());
                    return bounds.slice(1).map((box, i) => box.left - bounds[i].right);
                }''', time)
                self.assertTrue(all(gap >= 19 for gap in gaps), f'width={width}, time={time}, gaps={gaps}')

    def test_image_preview_exit_starts_at_interrupted_visual_state(self):
        self.page.goto(self.base + '/projects/hydrogen-hub/')
        self.page.locator('[data-image-preview]').first.click()
        viewer = self.page.locator('dialog')
        before = viewer.evaluate('''el => {
            const animation = el.getAnimations()[0];
            animation.pause(); animation.currentTime = 30;
            const style = getComputedStyle(el);
            return {opacity: Number(style.opacity), transform: style.transform};
        }''')
        self.page.locator('[data-close-image]').click()
        first_frame = viewer.evaluate('el => el.getAnimations()[0].effect.getKeyframes()[0]')
        self.assertAlmostEqual(float(first_frame['opacity']), before['opacity'], places=3)
        self.assertEqual(first_frame.get('transform'), before['transform'])
        expect(viewer).not_to_be_visible()

    def test_theme_switch_keeps_reading_colours_instant(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.page.goto(self.base + '/')
        self.page.locator('[data-theme-toggle]').click()
        colours = self.page.locator('.hero .button').evaluate('el => ({text:getComputedStyle(el).color, background:getComputedStyle(el).backgroundColor})')
        self.assertEqual(colours, {'text':'rgb(255, 255, 255)', 'background':'rgb(9, 108, 97)'})
        self.assertEqual(self.page.locator('.featured-grid h3').first.evaluate('el => getComputedStyle(el).color'), 'rgb(32, 45, 48)')
        self.page.locator('[data-theme-toggle]').click()
        colours = self.page.locator('.hero .button').evaluate('el => ({text:getComputedStyle(el).color, background:getComputedStyle(el).backgroundColor})')
        self.assertEqual(colours, {'text':'rgb(16, 32, 30)', 'background':'rgb(139, 232, 213)'})
        self.assertEqual(self.page.locator('.featured-grid h3').first.evaluate('el => getComputedStyle(el).color'), 'rgb(242, 244, 239)')

    def test_hero_content_and_centered_workflow(self):
        for prefix, removed in [('', 'Informing business decisions.'), ('/pl', 'Wspierać decyzje biznesowe.')]:
            self.page.goto(self.base + prefix + '/')
            expect(self.page.locator('[data-hero-line]')).to_have_count(2)
            self.assertNotIn(removed, self.page.locator('h1').inner_text())
            expect(self.page.locator('.hero-description')).to_have_count(0)
            expect(self.page.locator('.hero-actions a')).to_have_count(2)
            expect(self.page.locator('.workflow-stage')).to_have_count(5)
            self.assertTrue(self.page.locator('.hero-workflow').evaluate(
                'el => !!(el.compareDocumentPosition(document.querySelector(".hero-actions")) & Node.DOCUMENT_POSITION_FOLLOWING)'
            ))
            hero = self.page.locator('.hero').bounding_box()
            workflow = self.page.locator('.hero-workflow').bounding_box()
            self.assertAlmostEqual(workflow['x'] + workflow['width']/2, hero['x'] + hero['width']/2, delta=2)

    def test_expertise_rules_trace_once_without_moving_content(self):
        self.page.set_viewport_size({'width': 768, 'height': 900})
        self.page.goto(self.base + '/')
        self.page.wait_for_timeout(450)
        self.assertFalse(self.page.locator('.expertise').evaluate('el => el.hasAttribute("data-expertise-seen")'))
        self.page.set_viewport_size({'width': 1440, 'height': 1000})
        for route in ['/', '/pl/']:
            self.page.goto(self.base + route)
            section = self.page.locator('.expertise')
            section.scroll_into_view_if_needed()
            expect(section).to_have_attribute('data-expertise-animated', '')
            articles = section.locator('article')
            self.assertEqual(articles.count(), 3)
            self.assertEqual(articles.evaluate_all('els => els.map(el => getComputedStyle(el, "::before").animationName)'), ['expertise-rule-vertical'] * 3)
            self.assertEqual(articles.evaluate_all('els => els.map(el => getComputedStyle(el, "::before").animationDelay)'), ['0s', '0.14s', '0.28s'])
            self.assertEqual(articles.evaluate_all('els => els.map(el => getComputedStyle(el, "::before").animationDuration)'), ['0.28s'] * 3)
            self.assertEqual(articles.locator('h3').evaluate_all('els => els.map(el => getComputedStyle(el).opacity)'), ['1'] * 3)
            self.page.wait_for_timeout(650)
            expect(section).to_have_attribute('data-expertise-seen', '')
            self.assertFalse(section.evaluate('el => el.hasAttribute("data-expertise-animated")'))
            first = articles.first
            resting = float(first.evaluate('el => getComputedStyle(el, "::before").opacity'))
            first.hover()
            self.page.wait_for_timeout(220)
            self.assertGreater(float(first.evaluate('el => getComputedStyle(el, "::before").opacity')), resting)
            self.page.mouse.move(0, 0)
            self.page.locator('.hero').scroll_into_view_if_needed()
            section.scroll_into_view_if_needed()
            self.assertFalse(section.evaluate('el => el.hasAttribute("data-expertise-animated")'))
            self.page.emulate_media(reduced_motion='reduce')
            self.page.emulate_media(reduced_motion='no-preference')
            self.assertEqual(first.evaluate('el => getComputedStyle(el, "::before").animationName'), 'none')

    def test_expertise_mobile_reduced_motion_and_no_script(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/pl/')
        section = self.page.locator('.expertise')
        section.evaluate('el => scrollTo({top: scrollY + el.getBoundingClientRect().top - 80, behavior: "instant"})')
        expect(section).to_have_attribute('data-expertise-animated', '')
        article = section.locator('article').first
        self.assertEqual(article.evaluate('el => getComputedStyle(el, "::before").animationName'), 'expertise-rule-horizontal')
        self.assertEqual(article.evaluate('el => getComputedStyle(el, "::before").height'), '2px')
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))
        self.page.emulate_media(reduced_motion='reduce')
        self.page.reload()
        section.evaluate('el => scrollTo({top: scrollY + el.getBoundingClientRect().top - 80, behavior: "instant"})')
        expect(section).to_have_attribute('data-expertise-seen', '')
        self.assertFalse(section.evaluate('el => el.hasAttribute("data-expertise-animated")'))
        self.assertEqual(article.evaluate('el => getComputedStyle(el, "::before").animationName'), 'none')
        self.page.emulate_media(reduced_motion='no-preference')
        self.page.goto(self.base + '/pl/')
        self.page.keyboard.press('Tab')
        section.evaluate('el => scrollTo({top: scrollY + el.getBoundingClientRect().top - 80, behavior: "instant"})')
        expect(section).to_have_attribute('data-expertise-seen', '')
        self.assertFalse(section.evaluate('el => el.hasAttribute("data-expertise-animated")'))
        with self.browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844}) as context:
            page = context.new_page()
            page.goto(self.base + '/pl/')
            articles = page.locator('.expertise-grid article')
            self.assertEqual(articles.count(), 3)
            self.assertEqual(articles.locator('h3').evaluate_all('els => els.map(el => getComputedStyle(el).opacity)'), ['1'] * 3)
            self.assertEqual(articles.first.evaluate('el => getComputedStyle(el, "::before").opacity'), '0.28')

    def test_compact_hero_replays_complete_stages_on_every_homepage_load(self):
        self.page.goto(self.base + '/')
        stages = self.page.locator('.workflow-stage')
        delays = [1100, 1360, 1620, 1880, 2140]
        self.assertEqual(stages.evaluate_all('els => els.map(el => Math.round(el.getAnimations().find(a => a.animationName === "portfolio-stage-fade")?.effect.getTiming().delay))'), delays)
        self.page.reload()
        self.assertEqual(stages.evaluate_all('els => els.map(el => Math.round(el.getAnimations().find(a => a.animationName === "portfolio-stage-fade")?.effect.getTiming().delay))'), delays)
        self.page.goto(self.base + '/projects/hydrogen-hub/')
        self.page.locator('.brand').click()
        expect(self.page).to_have_url(self.base + '/')
        self.assertEqual(stages.evaluate_all('els => els.map(el => Math.round(el.getAnimations().find(a => a.animationName === "portfolio-stage-fade")?.effect.getTiming().delay))'), delays)

    def test_headline_and_complete_stages_fade_in_order(self):
        for route in ['/', '/pl/']:
            with self.browser.new_context(viewport={'width':1440, 'height':900}) as context:
                page = context.new_page()
                page.goto(self.base + route)
                lines = page.locator('[data-hero-line]')
                stages = page.locator('.workflow-stage')
                expect(lines).to_have_count(2)
                expect(stages).to_have_count(5)
                initial_height = page.locator('h1').bounding_box()['height']
                page.evaluate('''() => {
                    window.headlineSamples=[...document.querySelectorAll('[data-hero-line]')].map(el => el.getAnimations()[0]);
                    window.stageSamples=[...document.querySelectorAll('.workflow-stage')].map(el => el.getAnimations()[0]);
                    [...headlineSamples,...stageSamples].forEach(a => a.pause());
                }''')
                self.assertEqual([a['duration'] for a in lines.evaluate_all('els => els.map(el => el.getAnimations()[0].effect.getTiming())')], [480,480])
                self.assertEqual([a['delay'] for a in lines.evaluate_all('els => els.map(el => el.getAnimations()[0].effect.getTiming())')], [0,540])
                self.assertEqual(stages.evaluate_all('els => els.map(el => el.getAnimations()[0].effect.getTiming().duration)'), [240]*5)
                self.assertEqual(page.locator('.workflow-connection').evaluate('el => {const t=el.getAnimations()[0].effect.getTiming();return [t.delay,t.duration]}'), [1100,1280])
                for time, opacity in [(0,[0,0]), (480,[1,0]), (540,[1,0]), (1020,[1,1])]:
                    page.evaluate('time => headlineSamples.forEach(a => a.currentTime=time)', time)
                    self.assertEqual(lines.evaluate_all('els => els.map(el => parseFloat(getComputedStyle(el).opacity))'), opacity)
                    self.assertEqual(page.locator('h1').bounding_box()['height'], initial_height)
                for time, index in [(240,0),(780,1)]:
                    page.evaluate('time => headlineSamples.forEach(a => a.currentTime=time)', time)
                    faded = float(lines.nth(index).evaluate('el => getComputedStyle(el).opacity'))
                    self.assertGreater(faded, .25)
                    self.assertLess(faded, .75)
                    self.assertEqual(lines.nth(index).evaluate('el => getComputedStyle(el).clipPath'), 'none')
                for time, visible in [(0,0), (1340,1), (1600,2), (1860,3), (2120,4), (2380,5)]:
                    page.evaluate('time => stageSamples.forEach(a => a.currentTime=time)', time)
                    self.assertEqual(stages.evaluate_all('els => els.filter(el => parseFloat(getComputedStyle(el).opacity) === 1).length'), visible)
                page.evaluate('[...headlineSamples,...stageSamples].forEach(a => a.finish())')

    def test_wrapped_polish_sentence_fades_as_one_block(self):
        self.page.set_viewport_size({'width':390, 'height':844})
        self.page.goto(self.base + '/pl/')
        self.page.locator('h1').evaluate('el => { window.inkSamples=el.getAnimations({subtree:true}); inkSamples.forEach(a => a.pause()); }')
        for index,time in enumerate([240,780]):
            self.page.evaluate('time => inkSamples.forEach(a => a.currentTime=time)', time)
            faded = float(self.page.locator('[data-hero-line]').nth(index).evaluate('el => getComputedStyle(el).opacity'))
            self.assertGreater(faded, .25)
            self.assertLess(faded, .75)
        self.assertGreaterEqual(self.page.locator('[data-hero-line]').nth(1).evaluate('el => {const range=document.createRange();range.selectNodeContents(el);return range.getClientRects().length}'), 2)

    def test_signal_runs_across_five_stages_after_the_opening(self):
        self.page.goto(self.base + '/')
        signals = self.page.locator('.workflow-signal')
        expect(signals).to_have_count(5)
        self.assertEqual(signals.first.evaluate('el => el.getAnimations().length'), 0)
        self.page.wait_for_function('document.querySelector("[data-hero-workflow]").hasAttribute("data-idle-pulse")', timeout=5000)
        timings = signals.evaluate_all('els => els.map(el => el.getAnimations()[0].effect.getTiming())')
        self.assertEqual([timing['delay'] for timing in timings], [600,820,1040,1260,1480])
        self.assertEqual([timing['duration'] for timing in timings], [7000]*5)
        self.assertEqual(signals.first.bounding_box()['width'], 36)
        for index,signal in enumerate(signals.all()):
            signal.evaluate('(el,time) => { const a=el.getAnimations()[0]; a.pause(); a.currentTime=time; }', timings[index]['delay']+325)
            self.assertGreater(float(signal.evaluate('el => getComputedStyle(el).opacity')), .25)
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)

    def test_hover_keeps_caption_static_and_does_not_replay_entrance(self):
        self.page.goto(self.base + '/#projects')
        workflow = self.page.locator('.hero-workflow')
        workflow.scroll_into_view_if_needed()
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length > 0')
        caption = workflow.locator('figcaption').inner_text()
        self.page.locator('h1').hover()
        self.assertFalse(self.page.locator('html').evaluate('el => el.hasAttribute("data-hero-entrance")'))
        self.page.locator('.workflow-analysis .workflow-label').hover()
        self.assertEqual(workflow.locator('figcaption').inner_text(), caption)
        self.assertEqual(workflow.locator('.workflow-signal').first.evaluate('el => el.getAnimations().length'), 0)
        self.page.mouse.move(0,0)
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length > 0')

    def test_css_and_no_javascript_fallbacks_show_complete_hero(self):
        for prefix in ['', '/pl']:
            with self.browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844}) as context:
                page = context.new_page()
                page.goto(self.base + prefix + '/')
                expect(page.locator('[data-hero-line]')).to_have_count(2)
                expect(page.locator('.workflow-stage')).to_have_count(5)
                self.assertEqual(page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)
                self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'))
        self.page.route('**/assets/motion.js*', lambda route: route.abort())
        self.page.goto(self.base + '/')
        self.page.wait_for_timeout(3700)
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).opacity)'), ['1']*5)
        expect(self.page.locator('.hero-actions .button')).to_be_visible()

    def test_anchor_arrivals_are_static_but_reduced_motion_keeps_entrance(self):
        self.page.goto(self.base + '/#projects')
        self.assertFalse(self.page.locator('html').evaluate('el => el.hasAttribute("data-hero-entrance")'))
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)
        self.page.emulate_media(reduced_motion='reduce')
        self.page.goto(self.base + '/pl/')
        self.assertTrue(self.page.locator('html').evaluate('el => el.hasAttribute("data-hero-entrance")'))
        self.assertEqual(self.page.locator('[data-hero-line]').evaluate_all('els => els.map(el => el.getAnimations()[0]?.animationName)'), ['portfolio-sentence-fade']*2)
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => el.getAnimations()[0]?.animationName)'), ['portfolio-stage-fade']*5)
        first = self.page.locator('[data-hero-line]').first
        first.evaluate('el => {window.entranceSample=el.getAnimations()[0]; entranceSample.pause(); entranceSample.currentTime=240}')
        faded = float(first.evaluate('el => getComputedStyle(el).opacity'))
        self.assertGreater(faded, .25)
        self.assertLess(faded, .75)
        self.assertEqual(first.evaluate('el => getComputedStyle(el).clipPath'), 'none')
        first.evaluate('el => entranceSample.finish()')
        self.page.wait_for_function('!document.documentElement.hasAttribute("data-hero-entrance")')
        self.assertEqual(self.page.locator('.workflow-signal').evaluate_all('els => els.filter(el => el.getAnimations().length).length'), 0)

    def test_interruptions_settle_the_entire_hero(self):
        for trigger in ['keyboard','reduced','resize','pointer','offscreen']:
            with self.browser.new_context(viewport={'width':1440,'height':900}) as context:
                page = context.new_page()
                page.goto(self.base + '/')
                if trigger == 'keyboard': page.keyboard.press('Tab')
                elif trigger == 'reduced': page.emulate_media(reduced_motion='reduce')
                elif trigger == 'resize': page.set_viewport_size({'width':1280,'height':900})
                elif trigger == 'pointer': page.locator('.hero-identity').click()
                else: page.evaluate('window.scrollTo({top:document.querySelector("#contact").offsetTop,behavior:"instant"})')
                page.wait_for_function('!document.documentElement.hasAttribute("data-hero-entrance")')
                self.assertEqual(page.locator('[data-hero-line]').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*2)
                self.assertEqual(page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)
                self.assertEqual(page.locator('[data-hero-line]').evaluate_all('els => els.map(el => getComputedStyle(el).opacity)'), ['1']*2)
                self.assertEqual(page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).opacity)'), ['1']*5)

    def test_signal_stops_offscreen_hidden_and_with_reduced_motion(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.goto(self.base + '/pl/#projects')
        self.page.evaluate("document.documentElement.style.scrollBehavior='auto'")
        self.page.locator('.hero-workflow').scroll_into_view_if_needed()
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length > 0', timeout=3000)
        self.assertEqual(self.page.locator('.workflow-signal').first.bounding_box()['width'], 30)
        self.page.locator('#contact').scroll_into_view_if_needed()
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length === 0', timeout=3000)
        self.page.locator('.hero-workflow').scroll_into_view_if_needed()
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length > 0', timeout=3000)
        self.page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true}); document.dispatchEvent(new Event('visibilitychange'))")
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length === 0', timeout=3000)
        self.page.evaluate("delete document.hidden; document.dispatchEvent(new Event('visibilitychange'))")
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length > 0', timeout=3000)
        self.page.emulate_media(reduced_motion='reduce')
        self.page.wait_for_function('document.querySelector(".workflow-signal").getAnimations().length === 0', timeout=3000)

    def test_touch_workflow_opens_the_project_on_the_first_tap(self):
        with self.browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True) as context:
            page = context.new_page()
            page.goto(self.base + '/pl/')
            page.locator('.workflow-analysis').tap()
            expect(page).to_have_url(self.base + '/pl/projects/energy-techno-economics/')
            page.go_back()
            expect(page.locator('[data-hero-line]')).to_have_count(2)

    def test_storage_failure_and_motion_change_keep_links_usable(self):
        with self.browser.new_context(viewport={'width':1440,'height':900}) as context:
            context.add_init_script("Object.defineProperty(window,'sessionStorage',{get(){throw new DOMException('Unavailable','SecurityError')}})")
            page = context.new_page()
            page.goto(self.base + '/pl/')
            expect(page.locator('[data-hero-line]')).to_have_count(2)
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_function('!document.documentElement.hasAttribute("data-hero-entrance")')
            page.locator('.workflow-analysis').focus()
            page.keyboard.press('Enter')
            expect(page).to_have_url(self.base + '/pl/projects/energy-techno-economics/')

    def test_keyboard_navigation_skips_arrival_motion(self):
        self.page.goto(self.base + '/projects/hydrogen-hub/')
        self.page.locator('.brand').focus()
        self.page.keyboard.press('Enter')
        expect(self.page).to_have_url(self.base + '/')
        self.assertFalse(self.page.locator('html').evaluate('el => el.hasAttribute("data-hero-entrance")'))
        self.assertEqual(self.page.locator('.workflow-stage').evaluate_all('els => els.map(el => getComputedStyle(el).clipPath)'), ['none']*5)

    def test_whole_card_hover_keeps_images_still_and_respects_reduced_motion(self):
        self.page.emulate_media(reduced_motion='no-preference')
        self.page.goto(self.base + '/#projects')
        for media in ['media-photo', 'media-technical']:
            card = self.page.locator(f'.featured-grid .project-card-link:has(.{media})').first
            image = card.locator('img')
            card.hover()
            self.page.wait_for_timeout(330)
            matrix = card.evaluate('el => { const m = new DOMMatrix(getComputedStyle(el).transform); return [m.a, m.d, m.f]; }')
            self.assertAlmostEqual(matrix[0], 1.02, delta=.001)
            self.assertAlmostEqual(matrix[1], 1.02, delta=.001)
            self.assertAlmostEqual(matrix[2], -8, delta=.1)
            self.assertEqual(image.evaluate('el => getComputedStyle(el).transform'), 'none')
            self.page.mouse.move(0, 0)
            self.page.wait_for_timeout(250)
            self.page.emulate_media(reduced_motion='reduce')
            card.hover()
            halfway = card.evaluate('''el => {
                const travel = el.getAnimations().find(a => a.transitionProperty === 'transform');
                if (travel) { travel.pause(); travel.currentTime = travel.effect.getTiming().duration * .4; }
                return new DOMMatrix(getComputedStyle(el).transform).f;
            }''')
            self.assertGreater(halfway, -6)
            self.assertLess(halfway, 0)
            card.evaluate('el => el.getAnimations().forEach(a => a.play())')
            self.page.wait_for_timeout(240)
            reduced = card.evaluate('''el => {
                const style = getComputedStyle(el), matrix = new DOMMatrix(style.transform);
                return {scale: matrix.a, lift: matrix.f, duration: style.transitionDuration,
                        shadow: style.boxShadow, animations: el.getAnimations().length};
            }''')
            self.assertEqual(reduced['scale'], 1)
            self.assertEqual(reduced['lift'], -6)
            self.assertEqual(reduced['duration'].split(',')[0], '0.2s')
            self.assertNotEqual(reduced['shadow'], 'none')
            self.assertEqual(reduced['animations'], 0)
            self.page.emulate_media(reduced_motion='no-preference')

    def test_rounded_carousel_surfaces_do_not_change_layout_or_swipe_layer(self):
        # Hover may scroll an offscreen card into view. Compare document
        # geometry so scrolling cannot be mistaken for a layout change.
        document_box = '''el => {const r = el.getBoundingClientRect();
            return {x:r.left + scrollX, y:r.top + scrollY, width:r.width, height:r.height};}'''
        for route, selector in [('/#projects', '[data-home-carousel]'), ('/projects/microclimate-control/#related-heading', '.related[data-carousel]')]:
            self.page.goto(self.base + route)
            carousel = self.page.locator(selector)
            grid = carousel.locator('.project-grid')
            outer = grid.locator('.project-card:visible').first
            surface = outer.locator('.project-card-link')
            # Exercise the automatic scroll that triggered the CI failure.
            self.page.evaluate('scrollTo({top:0, behavior:"instant"})')
            self.page.mouse.move(0, 0)
            before = outer.evaluate(document_box)
            height = grid.bounding_box()['height']
            surface.hover()
            self.page.wait_for_timeout(200)
            self.assertEqual(surface.evaluate('el => getComputedStyle(el).borderTopLeftRadius'), '24px')
            self.assertNotEqual(surface.evaluate('el => getComputedStyle(el).boxShadow'), 'none')
            self.assertEqual(outer.evaluate('el => getComputedStyle(el).transform'), 'none')
            self.assertEqual(before, outer.evaluate(document_box))
            self.assertAlmostEqual(height, grid.bounding_box()['height'], delta=1)
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 1440)
            self.page.keyboard.press('Tab')
            surface.focus()
            self.assertEqual(surface.evaluate('el => getComputedStyle(el).transform'), 'none')
            self.assertEqual(surface.evaluate('el => getComputedStyle(el).outlineStyle'), 'solid')
            self.page.set_viewport_size({'width': 390, 'height': 844})
            self.assertEqual(surface.evaluate('el => getComputedStyle(el).borderTopLeftRadius'), '20px')
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)
            self.page.set_viewport_size({'width': 1440, 'height': 1000})

    def test_sliding_carousel_ink_stays_inside_tablet_gutters(self):
        for route, selector in [('/#projects', '[data-home-carousel]'), ('/projects/microclimate-control/#related-heading', '.related[data-carousel]')]:
            self.page.set_viewport_size({'width': 768, 'height': 1000})
            self.page.goto(self.base + route)
            carousel = self.page.locator(selector)
            carousel.locator('[data-next]').click()
            carousel.locator('.project-grid').evaluate('''grid => grid.getAnimations({subtree:true}).forEach(a => {
                a.pause(); a.currentTime = a.effect.getTiming().duration * .4;
            })''')
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 768)
            carousel.locator('[data-next]').click()

    def test_image_preview_motion_preserves_escape_and_focus(self):
        self.page.goto(self.base + '/projects/hydrogen-hub/')
        thumb = self.page.locator('[data-image-preview]').first
        thumb.click()
        viewer = self.page.locator('dialog')
        self.assertTrue(viewer.evaluate('el => el.getAnimations().some(a => a.playState === "running")'))
        self.page.keyboard.press('Escape')
        expect(viewer).not_to_be_visible()
        expect(thumb).to_be_focused()
        self.page.keyboard.press('Enter')
        expect(viewer).to_be_visible()
        self.assertFalse(viewer.evaluate('el => el.getAnimations().some(a => a.playState === "running")'))

    def test_mobile_navigation_alignment_and_footer_access(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for section in ['expertise', 'projects', 'about', 'contact']:
            self.page.goto(self.base + '/')
            self.page.locator('[data-menu-toggle]').click()
            self.page.locator('#site-nav a[href$="#' + section + '"]').click()
            expect(self.page.locator('[data-menu-toggle]')).to_have_attribute('aria-expanded', 'false')
            # Native smooth-scroll timing differs by platform and CI load.
            # Wait for the geometry we require, not an assumed animation length.
            try:
                self.page.wait_for_function("id=>Math.abs(document.getElementById(id).getBoundingClientRect().top-document.querySelector('.site-header').getBoundingClientRect().bottom)<=3", arg=section, timeout=5000)
            except PlaywrightTimeoutError:
                geometry = self.page.evaluate("id=>({sectionTop:document.getElementById(id).getBoundingClientRect().top,headerBottom:document.querySelector('.site-header').getBoundingClientRect().bottom,scrollY,maxScroll:document.documentElement.scrollHeight-innerHeight})", section)
                self.fail(f'{section} did not reach header alignment: {geometry}')
            gap = self.page.evaluate("id=>document.getElementById(id).getBoundingClientRect().top-document.querySelector('.site-header').getBoundingClientRect().bottom", section)
            self.assertLessEqual(abs(gap), 3, f'{section}: {gap}')
        self.page.set_viewport_size({'width': 1440, 'height': 900})
        self.page.goto(self.base + '/#contact')
        self.page.wait_for_timeout(1000)
        self.page.mouse.wheel(0, 500)
        self.page.wait_for_timeout(1000)
        self.assertTrue(self.page.locator('.site-footer').evaluate('el=>el.getBoundingClientRect().bottom <= innerHeight+1'))

    def test_home_navigation_is_localized_and_tracks_the_hero(self):
        for prefix, label, expertise_label in [('', 'Home', 'Expertise'), ('/pl', 'Strona główna', 'Kompetencje')]:
            self.page.goto(self.base + prefix + '/#projects')
            home = self.page.locator('#site-nav [data-nav-home]')
            expertise = self.page.locator('#site-nav a[href$="#expertise"]')
            expect(home).to_have_text(label)
            expect(home).to_have_attribute('href', '#page-top')
            expect(expertise).to_have_text(expertise_label)
            expect(expertise).to_have_attribute('href', '#expertise')
            self.assertEqual(self.page.locator('#site-nav > a').all_text_contents()[1], expertise_label)
            expect(self.page.locator('#site-nav a[href="#projects"]')).to_have_attribute('aria-current', 'location')
            self.assertIsNone(home.get_attribute('aria-current'))
            self.page.evaluate('window.homeNavMarker = true')
            home.click()
            self.page.wait_for_function('scrollY < 2')
            expect(self.page).to_have_url(self.base + prefix + '/#page-top')
            self.assertTrue(self.page.evaluate('window.homeNavMarker'))
            expect(home).to_have_attribute('aria-current', 'location')
            expertise.click()
            expect(self.page).to_have_url(self.base + prefix + '/#expertise')
            expect(expertise).to_have_attribute('aria-current', 'location')
            self.assertTrue(self.page.evaluate('window.homeNavMarker'))
            for section in ['about', 'contact']:
                link = self.page.locator(f'#site-nav a[href$="#{section}"]')
                link.click()
                expect(link).to_have_attribute('aria-current', 'location')
                self.assertIsNone(home.get_attribute('aria-current'))
            self.page.goto(self.base + prefix + '/projects/microclimate-control/')
            expect(home).to_have_attribute('href', prefix + '/')
            expect(expertise).to_have_attribute('href', prefix + '/#expertise')
            expertise.focus()
            self.page.keyboard.press('Enter')
            expect(self.page).to_have_url(self.base + prefix + '/#expertise')
            self.page.wait_for_timeout(900)
            gap = self.page.evaluate("document.querySelector('#expertise').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
            self.assertLessEqual(abs(gap), 3, f'{prefix or "en"} expertise arrival: {gap}')
            self.page.goto(self.base + prefix + '/projects/microclimate-control/')
            home.focus()
            self.page.keyboard.press('Enter')
            expect(self.page).to_have_url(self.base + prefix + '/')

    def test_mobile_home_link_closes_menu_and_preserves_layout(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/pl/#projects')
        self.page.locator('[data-menu-toggle]').click()
        home = self.page.locator('#site-nav [data-nav-home]')
        expect(home).to_be_visible()
        home.click()
        self.page.wait_for_function('scrollY < 2')
        expect(self.page.locator('[data-menu-toggle]')).to_have_attribute('aria-expanded', 'false')
        expect(home).to_have_attribute('aria-current', 'location')

    def test_navigation_uses_menu_through_tablet_widths_without_overflow(self):
        for width in [320, 390, 768, 900, 901, 1440]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            self.page.goto(self.base + '/pl/')
            toggle = self.page.locator('[data-menu-toggle]')
            if width <= 900:
                expect(toggle).to_be_visible()
                if width == 320:
                    expect(toggle).to_have_attribute('aria-label', 'Menu')
                    self.assertLess(toggle.bounding_box()['y'], self.page.locator('.brand').bounding_box()['y'] + self.page.locator('.brand').bounding_box()['height'])
                expect(self.page.locator('#site-nav')).not_to_be_visible()
                toggle.click()
            else:
                expect(toggle).not_to_be_visible()
            expect(self.page.locator('#site-nav')).to_be_visible()
            line_counts = self.page.locator('#site-nav a').evaluate_all('''els => els.map(el => {
                const range = document.createRange();
                range.selectNodeContents(el);
                return range.getClientRects().length;
            })''')
            self.assertEqual(line_counts, [1, 1, 1, 1, 1], f'{width}: {line_counts}')
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width)

    def test_wheel_step_and_exact_anchor_alignment(self):
        self.page.set_viewport_size({'width': 1440, 'height': 900})
        self.page.goto(self.base + '/')
        self.page.mouse.wheel(0, 100)
        self.page.wait_for_timeout(1200)
        gap = self.page.evaluate("document.querySelector('.expertise').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom")
        self.assertLessEqual(abs(gap), 3, f'expertise: {gap}')
        for width, height in [(1440, 900), (1100, 620), (390, 844)]:
            with self.browser.new_context(viewport={'width': width, 'height': height}) as context:
                page = context.new_page()
                page.goto(self.base + '/#contact')
                page.wait_for_timeout(900)
                alignment = page.evaluate("""() => ({
                    gap: document.querySelector('#contact').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().bottom,
                    header: document.querySelector('.site-header').getBoundingClientRect().height,
                    padding: getComputedStyle(document.documentElement).scrollPaddingTop,
                    scrollY, maxScroll: document.documentElement.scrollHeight - innerHeight
                })""")
                self.assertLessEqual(abs(alignment['gap']), 3, f'{width}x{height}: {alignment}')

    def test_contact_and_footer_share_the_final_desktop_screen(self):
        self.page.emulate_media(reduced_motion='reduce')
        for prefix in ['', '/pl']:
            for theme in ['dark', 'light']:
                for width, height in [(1280,720), (1280,761), (1280,839), (1280,840), (1536,844), (1920,1200)]:
                    self.page.set_viewport_size({'width':width, 'height':height})
                    self.page.goto(self.base + prefix + '/?footer-fit=' + theme + '-' + str(width) + '-' + str(height) + '#contact')
                    self.page.wait_for_function("Math.abs(document.querySelector('#contact').getBoundingClientRect().top-document.querySelector('.site-header').getBoundingClientRect().bottom)<=2", timeout=3000)
                    if self.page.locator('html').get_attribute('data-theme') != theme:
                        self.page.locator('[data-theme-toggle]').click()
                    self.page.wait_for_function("Math.abs(document.querySelector('#contact').getBoundingClientRect().top-document.querySelector('.site-header').getBoundingClientRect().bottom)<=2", timeout=3000)
                    geometry = self.page.evaluate('''()=>{
                        const contact=document.querySelector('#contact').getBoundingClientRect(),
                            footer=document.querySelector('.site-footer').getBoundingClientRect(),
                            header=document.querySelector('.site-header').getBoundingClientRect();
                        return {top:contact.top-header.bottom,bottom:footer.bottom-innerHeight,
                            gap:footer.top-contact.bottom,remaining:document.documentElement.scrollHeight-innerHeight-scrollY,
                            formBottom:document.querySelector('#contact-form').getBoundingClientRect().bottom,
                            overflow:document.documentElement.scrollWidth>innerWidth};
                    }''')
                    self.assertLessEqual(abs(geometry['top']), 2, geometry)
                    self.assertLessEqual(abs(geometry['bottom']), 2, geometry)
                    self.assertLessEqual(abs(geometry['gap']), 1, geometry)
                    self.assertLessEqual(abs(geometry['remaining']), 2, geometry)
                    self.assertLess(geometry['formBottom'], height, geometry)
                    self.assertFalse(geometry['overflow'], geometry)
                    self.assertEqual(self.page.locator('footer').count(), 1)
                    self.assertEqual(self.page.locator('body > footer').count(), 1)

    def test_homepage_sections_and_reduced_motion(self):
        self.page.goto(self.base + '/')
        self.assertEqual(self.page.locator('main > section').evaluate_all("els=>els.map(el=>el.id || el.getAttribute('aria-labelledby'))"), ['hero-heading', 'expertise', 'projects', 'about', 'contact'])
        self.assertEqual(self.page.locator('html').evaluate('el=>getComputedStyle(el).scrollSnapType'), 'y')
        self.page.emulate_media(reduced_motion='reduce')
        self.assertEqual(self.page.locator('html').evaluate('el=>getComputedStyle(el).scrollSnapType'), 'none')
        self.page.locator('.hero .button').click()
        expect(self.page).to_have_url(self.base + '/#projects')

    def test_about_and_contact_complete_the_alternating_section_surfaces(self):
        for prefix, theme, width in [('', 'dark', 1440), ('/pl', 'light', 1440), ('/pl', 'dark', 390), ('', 'light', 768)]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            self.page.goto(self.base + prefix + '/')
            if theme == 'light': self.page.locator('[data-theme-toggle]').click()
            surfaces = self.page.evaluate('''() => {
                const color = selector => getComputedStyle(document.querySelector(selector)).backgroundColor;
                const about = document.querySelector('#about');
                const content = about.querySelector('.container').getBoundingClientRect();
                const work = document.querySelector('#projects').getBoundingClientRect();
                return {
                    base: color('body'), panel: color('.project-card-link'), about: color('#about'),
                    contact: color('#contact'), field: color('#contact-name'),
                    aboutWidth: about.getBoundingClientRect().width, contentLeft: content.left,
                    workLeft: work.left, viewportWidth: innerWidth,
                    overflow: document.documentElement.scrollWidth > innerWidth
                };
            }''')
            self.assertEqual(surfaces['about'], surfaces['panel'], surfaces)
            self.assertEqual(surfaces['contact'], surfaces['base'], surfaces)
            self.assertEqual(surfaces['field'], surfaces['panel'], surfaces)
            self.assertEqual(surfaces['aboutWidth'], surfaces['viewportWidth'], surfaces)
            self.assertAlmostEqual(surfaces['contentLeft'], surfaces['workLeft'], delta=1, msg=str(surfaces))
            self.assertFalse(surfaces['overflow'], surfaces)

    def test_project_gallery_below_text(self):
        self.page.goto(self.base + '/projects/hydrogen-hub/')
        thumbs = self.page.locator('[data-image-preview]')
        expect(thumbs).to_have_count(3)
        self.assertGreaterEqual(self.page.locator('.project-images').bounding_box()['y'], self.page.locator('.prose').bounding_box()['y'] + self.page.locator('.prose').bounding_box()['height'])
        thumbs.first.click()
        expect(self.page.locator('dialog[open]')).to_have_count(1)
        self.page.keyboard.press('Escape')
        expect(self.page.locator('dialog[open]')).to_have_count(0)
        expect(thumbs.first).to_be_focused()

    def test_cropped_previews_preserve_proportions_and_originals(self):
        previews = [('v6-engine', 1024 / 834, '/img/portfolio/engine.png'),
                    ('fedex-pricing', 361 / 457, '/img/portfolio/fedex_app.png')]
        for prefix in ['', '/pl']:
            for slug, ratio, original in previews:
                self.page.goto(self.base + prefix + '/projects/' + slug + '/')
                thumb = self.page.locator('[data-image-preview]').first
                crop = thumb.locator('.image-crop')
                expect(crop).to_have_count(1)
                for theme in ['dark', 'light']:
                    if self.page.locator('html').get_attribute('data-theme') != theme:
                        self.page.locator('[data-theme-toggle]').click()
                    for width in [320, 390, 768, 1440]:
                        self.page.set_viewport_size({'width': width, 'height': 900})
                        frame, preview = thumb.bounding_box(), crop.bounding_box()
                        self.assertAlmostEqual(preview['width'] / preview['height'], ratio, delta=.01)
                        self.assertGreaterEqual(preview['x'], frame['x'])
                        self.assertLessEqual(preview['x'] + preview['width'], frame['x'] + frame['width'] + 1)
                        self.assertLessEqual(preview['height'], frame['height'])
                        self.assertEqual(thumb.evaluate('el => getComputedStyle(el).backgroundColor'),
                                         self.page.locator('.project-card-link').first.evaluate('el => getComputedStyle(el).backgroundColor'))
                thumb.click()
                expect(self.page.locator('dialog[open] img')).to_have_attribute('src', self.base + original)
                self.page.keyboard.press('Escape')
                expect(thumb).to_be_focused()

    def test_project_atlas_chapters_and_filter_reset(self):
        categories = [('engineering', 6), ('simulation', 4), ('analysis', 3), ('software', 5)]
        for prefix in ['', '/pl']:
            self.page.set_viewport_size({'width': 1440, 'height': 900})
            self.page.goto(self.base + prefix + '/projects/')
            chapters = self.page.locator('[data-category-section]')
            expect(chapters).to_have_count(4)
            self.assertEqual(chapters.evaluate_all('(nodes) => nodes.map(node => node.dataset.categorySection)'), [key for key, _ in categories])
            expect(self.page.locator('.atlas-row')).to_have_count(18)
            for key, count in categories:
                chapter = self.page.locator('[data-category-section="' + key + '"]')
                expect(chapter.locator('.atlas-row')).to_have_count(count)
                self.assertEqual(chapter.locator('.atlas-chapter-heading').evaluate('el => getComputedStyle(el).position'), 'sticky')
            row = self.page.locator('.atlas-row').first
            self.assertEqual(row.locator('a').count(), 1)
            self.assertEqual(row.evaluate('el => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
            plate = row.locator('.atlas-row-image').bounding_box()
            self.assertLessEqual(plate['width'], 161)
            self.assertLessEqual(plate['height'], 113)
            self.page.locator('[data-filter="engineering"]').click()
            expect(self.page.locator('[data-category-section]:visible')).to_have_count(1)
            expect(self.page.locator('.atlas-row:visible')).to_have_count(6)
            self.page.locator('[data-filter="all"]').click()
            expect(self.page.locator('[data-category-section]:visible')).to_have_count(4)
            self.page.set_viewport_size({'width': 390, 'height': 844})
            self.assertEqual(self.page.locator('.atlas-chapter-heading').first.evaluate('el => getComputedStyle(el).position'), 'static')
            self.assertLessEqual(self.page.locator('.atlas-row-image').first.bounding_box()['width'], 97)
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)

    def test_case_study_spine_and_compact_contact_sheet(self):
        for prefix in ['', '/pl']:
            self.page.set_viewport_size({'width': 1440, 'height': 1000})
            self.page.goto(self.base + prefix + '/projects/microclimate-control/')
            intro = self.page.locator('.case-intro')
            header = intro.locator('.case-header').bounding_box()
            facts = intro.locator('.project-facts').bounding_box()
            self.assertGreaterEqual(facts['y'], header['y'] + header['height'] - 1)
            self.assertEqual(self.page.locator('.case-body .prose h2').count(), 4)
            self.assertEqual(self.page.locator('.case-body .prose').evaluate('el => getComputedStyle(el, "::before").content'), '""')
            for figure in self.page.locator('.project-images .image-thumbnail').all():
                box = figure.bounding_box()
                self.assertLessEqual(box['width'], 221)
                self.assertLessEqual(box['height'], 166)
            self.assertGreaterEqual(self.page.locator('.project-images').bounding_box()['y'], self.page.locator('.prose').bounding_box()['y'] + self.page.locator('.prose').bounding_box()['height'])
            if self.page.locator('.references').count():
                self.assertAlmostEqual(self.page.locator('.references').bounding_box()['x'], self.page.locator('.project-images').bounding_box()['x'], delta=1)
            self.page.set_viewport_size({'width': 320, 'height': 700})
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 320)

        for slug, media_type in [('energy-techno-economics', 'technical'), ('orifice-calculation-software', 'screen')]:
            self.page.set_viewport_size({'width': 1440, 'height': 1000})
            self.page.goto(self.base + '/projects/' + slug + '/')
            figure = self.page.locator('.project-images .media-' + media_type + ' .image-thumbnail').first
            self.assertLessEqual(figure.bounding_box()['width'], 221)
            self.assertLessEqual(figure.bounding_box()['height'], 166)
            figure.click()
            expect(self.page.locator('dialog[open]')).to_have_count(1)

    def test_atlas_fragment_focus_and_responsive_themes(self):
        self.page.goto(self.base + '/projects/')
        for prefix in ['', '/pl']:
            for theme in ['dark', 'light']:
                self.page.goto(self.base + prefix + '/projects/#analysis')
                expect(self.page.locator('[data-filter="analysis"]')).to_have_attribute('aria-pressed', 'true')
                expect(self.page.locator('[data-category-section]:visible')).to_have_count(1)
                expect(self.page.locator('.atlas-row:visible')).to_have_count(3)
                self.page.wait_for_timeout(100)
                chapter_top = self.page.locator('#analysis').bounding_box()['y']
                header_bottom = self.page.locator('.site-header').bounding_box()['height']
                self.assertGreaterEqual(chapter_top, header_bottom)
                self.assertLessEqual(chapter_top, header_bottom + 30)
                if self.page.locator('html').get_attribute('data-theme') != theme:
                    self.page.locator('[data-theme-toggle]').click()
                self.assertEqual(self.page.locator('html').get_attribute('data-theme'), theme)
                first = self.page.locator('.atlas-row:visible').first
                first.locator('a').focus()
                self.page.wait_for_timeout(250)
                self.assertEqual(first.evaluate('el => getComputedStyle(el, "::before").transform'), 'matrix(1, 0, 0, 1, 0, 0)')
                for width in [320, 390, 768, 1440]:
                    self.page.set_viewport_size({'width': width, 'height': 900})
                    self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width)
                    plate = first.locator('.atlas-row-image').bounding_box()
                    self.assertLessEqual(plate['width'], 97 if width <= 600 else 161)
                self.page.locator('[data-language-switch]').click()
                self.assertIn('#analysis', self.page.url)

    def test_header_category_and_figure_layout(self):
        for prefix in ['', '/pl']:
            for slug in ['hydrogen-hub', 'heat-exchanger-simulation']:
                self.page.goto(self.base + prefix + '/projects/' + slug + '/')
                expect(self.page.locator('.case-header .eyebrow a')).to_have_count(2)
                expect(self.page.locator('.case-body')).not_to_contain_text('Open original image')
                expect(self.page.locator('.case-body')).not_to_contain_text('Otwórz oryginalny obraz')
                expect(self.page.locator('[data-theme-toggle] svg')).to_have_count(2)
                for width in [390, 1440]:
                    self.page.set_viewport_size({'width': width, 'height': 1000})
                    theme = self.page.locator('[data-theme-toggle]').bounding_box()
                    languages = self.page.locator('.language-links').bounding_box()
                    self.assertGreaterEqual(theme['x'], languages['x'] + languages['width'])
                    for image in self.page.locator('.case-body figure img').all():
                        image.scroll_into_view_if_needed()
                        image.evaluate('img => img.decode()')
                        self.assertTrue(image.evaluate("img => {const f=img.closest('figure').getBoundingClientRect(), i=img.getBoundingClientRect(); return i.bottom <= f.bottom + 1 && i.top >= f.top - 1}"))
                self.page.locator('.case-header .eyebrow a').last.click()
                category = 'engineering' if slug == 'hydrogen-hub' else 'simulation'
                expect(self.page.locator('[data-filter="' + category + '"]')).to_have_attribute('aria-pressed', 'true')

    def test_category_exploration_context(self):
        self.page.goto(self.base + '/projects/#engineering')
        self.page.locator('[data-project]:visible a').first.click()
        self.assertIn('category=engineering', self.page.url)
        for _ in range(6):
            cards = self.page.locator('[data-carousel] .project-card:visible')
            expect(cards).to_have_count(4)
            self.assertEqual(cards.evaluate_all("els=>els.map(el=>el.dataset.category)"), ['engineering'] * 4)
            self.page.locator('[data-next]').click()
        cards.first.locator('a').click()
        self.assertIn('category=engineering', self.page.url)
        self.page.locator('[data-language-switch]').click()
        self.assertIn('category=engineering', self.page.url)
        self.assertEqual(self.page.locator('[data-carousel] .project-card:visible').evaluate_all("els=>els.map(el=>el.dataset.category)"), ['engineering'] * 4)
        self.page.goto(self.base + '/projects/')
        self.page.locator('[data-project]:visible a').first.click()
        self.assertNotIn('category=', self.page.url)
        self.page.goto(self.base + '/projects/microclimate-control/?category=invalid')
        expect(self.page.locator('[data-carousel] .project-card:visible')).to_have_count(4)

    def test_theme_and_carousel(self):
        self.page.goto(self.base + '/projects/microclimate-control/')
        switch = self.page.locator('[data-theme-toggle]')
        expect(switch).to_have_count(1)
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'dark')
        switch.click()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'light')
        self.page.locator('[data-language-switch]').click()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'light')
        cards = self.page.locator('[data-carousel] .project-card:visible')
        expect(cards).to_have_count(4)
        first = cards.first.locator('a').get_attribute('href')
        self.assertIn('gas-turbine-digital-twin', first)
        seen = set()
        for _ in range(17):
            seen.add(self.page.locator('[data-carousel] .project-card[style="order: 0;"] a').get_attribute('href'))
            self.page.locator('[data-next]').click()
        self.assertEqual(len(seen), 17)
        self.assertFalse(any('microclimate-control' in url for url in seen))
        self.assertEqual(cards.first.locator('a').get_attribute('href'), first)
        self.page.locator('[data-prev]').click()
        self.assertTrue(any('automated-price-list' in a.get_attribute('href') for a in cards.locator('a').all()))
        self.page.set_viewport_size({'width': 390, 'height': 844})
        expect(cards).to_have_count(1)

    def test_saved_theme_before_main_script(self):
        self.context.add_init_script("localStorage.setItem('portfolio-theme', 'light')")
        self.page.route('**/assets/site.js*', lambda route: route.abort())
        self.page.goto(self.base + '/pl/')
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'light')

    def test_theme_without_storage(self):
        self.context.add_init_script("Object.defineProperty(window, 'localStorage', {get() {throw new Error('unavailable')}})")
        self.page.goto(self.base + '/')
        switch = self.page.locator('[data-theme-toggle]')
        expect(switch).to_have_count(1)
        switch.click()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'light')

    def test_collection_filters_and_language_pairs(self):
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/projects/')
            expect(self.page.locator('[data-project]:visible')).to_have_count(18)
            for category, count in [('engineering', 6), ('simulation', 4), ('analysis', 3), ('software', 5), ('all', 18)]:
                button = self.page.locator(f'[data-filter="{category}"]')
                button.click()
                expect(button).to_have_attribute('aria-pressed', 'true')
                expect(self.page.locator('[data-project]:visible')).to_have_count(count)
            self.page.locator('[data-project] a').first.click()
            before = urlparse(self.page.url).path
            self.page.locator('[data-language-switch]').click()
            after = urlparse(self.page.url).path
            self.assertEqual(before.removeprefix('/pl'), after.removeprefix('/pl'))
            self.assertNotEqual(before, after)

    def test_legacy_fragment_and_hashchange(self):
        self.page.goto(self.base + '/#portfolioModal-8')
        expect(self.page).to_have_url(self.base + '/projects/microclimate-control/')
        self.page.goto(self.base + '/')
        self.page.evaluate("location.hash = 'portfolioModal-4'")
        expect(self.page).to_have_url(self.base + '/projects/orifice-calculation-software/')
        self.page.goto(self.base + '/#portfolioModal-999')
        expect(self.page).to_have_url(self.base + '/#portfolioModal-999')
        self.page.goto(self.base + '/#constructor')
        expect(self.page).to_have_url(self.base + '/#constructor')

    def test_mobile_menu_escape_keyboard_and_no_overflow(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.goto(self.base + '/pl/')
        toggle = self.page.locator('[data-menu-toggle]')
        toggle.click()
        expect(toggle).to_have_attribute('aria-expanded', 'true')
        self.page.keyboard.press('Escape')
        expect(toggle).to_have_attribute('aria-expanded', 'false')
        expect(toggle).to_be_focused()
        toggle.click()
        self.page.locator('#site-nav a[href="#projects"]').click()
        expect(self.page).to_have_url(self.base + '/pl/#projects')
        for width in [320, 360, 390, 768, 1440]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            for path in ['/', '/pl/', '/pl/projects/', '/pl/projects/energy-techno-economics/']:
                self.page.goto(self.base + path)
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width, path)

    def fill_form(self, prefix=''):
        self.page.goto(self.base + prefix + '/#contact')
        self.page.locator('#contact-name').fill('Preview Test')
        self.page.locator('#contact-email').fill('preview@example.com')
        self.page.locator('#contact-message').fill('A local test; never sent to Formspree.')

    def test_invalid_form_never_sends(self):
        requests = []
        self.page.route('https://formspree.io/**', lambda route: (requests.append(route.request), route.abort()))
        self.page.goto(self.base + '/pl/#contact')
        self.page.locator('#contact-form button[type=submit]').click()
        expect(self.page.locator('#contact-status')).to_contain_text('Uzupełnij')
        self.assertEqual(requests, [])

    def test_form_errors_remain_described_until_corrected(self):
        requests = []
        self.page.route('https://formspree.io/**', lambda route: (requests.append(route.request), route.abort()))
        for prefix in ['', '/pl']:
            self.page.goto(self.base + prefix + '/#contact')
            self.page.locator('#contact-form button[type=submit]').click()
            status = self.page.locator('#contact-status')
            message = status.inner_text()
            self.page.locator('#contact-name').fill('Audit')
            expect(status).to_have_text(message)
            email = self.page.locator('#contact-email')
            email.fill('invalid')
            expect(email).to_have_attribute('aria-invalid', 'true')
            for field in ['#contact-email', '#contact-message']:
                expect(self.page.locator(field)).to_have_attribute('aria-describedby', 'contact-status')
            email.fill('preview@example.com')
            expect(email).not_to_have_attribute('aria-invalid', 'true')
            expect(status).to_have_text(message)
            self.page.locator('#contact-message').fill('Validation only; never sent.')
            expect(status).to_be_empty()
            expect(self.page.locator('#contact-form [aria-invalid=true]')).to_have_count(0)
        self.assertEqual(requests, [])

    def test_form_success_and_duplicate_prevention(self):
        pending = []
        self.page.route('https://formspree.io/**', lambda route: pending.append(route))
        self.fill_form('/pl')
        button = self.page.locator('#contact-form button[type=submit]')
        button.click()
        expect(button).to_be_disabled()
        expect(button).to_have_text('Wysyłanie…')
        expect(self.page.locator('#contact-message')).not_to_be_editable()
        self.page.locator('#contact-form').evaluate("el => el.dispatchEvent(new Event('submit', {bubbles:true, cancelable:true}))")
        self.assertEqual(len(pending), 1)
        pending[0].fulfill(status=200, content_type='application/json', body='{"ok":true}')
        expect(self.page.locator('#contact-status')).to_contain_text('Dziękuję')
        expect(self.page.locator('#contact-message')).to_have_value('')
        expect(button).to_be_enabled()
        expect(self.page.locator('#contact-message')).to_be_editable()

    def test_form_http_and_network_failures_preserve_text(self):
        for mode in ['http', 'network']:
            self.page.unroute_all()
            self.page.route('https://formspree.io/**', lambda route: route.fulfill(status=429, body='{}') if mode == 'http' else route.abort())
            self.fill_form()
            self.page.locator('#contact-form button[type=submit]').click()
            expect(self.page.locator('#contact-status')).to_contain_text('could not be sent')
            expect(self.page.locator('#contact-message')).to_have_value('A local test; never sent to Formspree.')
            expect(self.page.locator('#contact-form button[type=submit]')).to_be_enabled()

    def test_no_javascript_still_shows_content_and_navigation(self):
        with self.browser.new_context(java_script_enabled=False, viewport={'width':390, 'height':844}) as context:
            page = context.new_page()
            page.goto(self.base + '/pl/projects/')
            expect(page.locator('[data-project]')).to_have_count(18)
            expect(page.locator('[data-category-section]:visible')).to_have_count(4)
            expect(page.locator('#site-nav')).to_be_visible()
            expect(page.locator('#site-nav [data-nav-home]')).to_have_text('Strona główna')
            expect(page.locator('#site-nav a[href="/pl/#expertise"]')).to_have_text('Kompetencje')
            expect(page.locator('[data-filter-controls]')).to_be_hidden()
            for width in [768, 900]:
                page.set_viewport_size({'width': width, 'height': 900})
                page.goto(self.base + '/pl/')
                expect(page.locator('#site-nav a[href="#expertise"]')).to_be_visible()
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), width)
            page.goto(self.base + '/pl/projects/microclimate-control/')
            expect(page.locator('[data-carousel] .project-card:visible')).to_have_count(2)
            expect(page.locator('.carousel-controls')).to_be_hidden()

    def test_visual_review_captures(self):
        out = ROOT / 'artifacts/screenshots'
        out.mkdir(parents=True, exist_ok=True)
        for theme in ['dark', 'light']:
            for name, path, width in [('home-en', '/', 1440), ('home-pl-mobile', '/pl/', 390), ('home-tablet', '/', 768), ('projects', '/projects/', 1440), ('projects-mobile', '/pl/projects/', 390), ('project-pl', '/pl/projects/energy-techno-economics/', 1440), ('project-photo', '/projects/microclimate-control/', 1440), ('project-gallery-mobile', '/pl/projects/hydrogen-hub/', 390), ('project-software', '/projects/fedex-pricing/', 1440)]:
                self.page.set_viewport_size({'width':width, 'height':1000})
                self.page.goto(self.base + path)
                self.page.evaluate("localStorage.setItem('portfolio-theme', '" + theme + "')")
                self.page.reload()
                for img in self.page.locator('img:visible').all():
                    img.scroll_into_view_if_needed()
                    expect(img).to_have_js_property('complete', True)
                    self.assertGreater(img.evaluate('el => el.naturalWidth'), 0)
                self.page.evaluate('window.scrollTo(0,0)')
                self.page.screenshot(path=str(out / (theme+'-'+name+'.png')), full_page=True, animations='disabled')
                self.page.screenshot(path=str(out / (theme+'-'+name+'-viewport.png')), animations='disabled')

if __name__ == '__main__':
    unittest.main()
