(() => {
  'use strict';
  const motion = window.portfolioMotion;
  const header = document.querySelector('.site-header');
  const contactFooter = document.querySelector('[data-contact-footer]');
  const updateHeaderHeight = () => {
    if (header) document.documentElement.style.setProperty('--header-height', header.getBoundingClientRect().height + 'px');
    if (contactFooter) document.documentElement.style.setProperty('--home-footer-height', contactFooter.getBoundingClientRect().height + 'px');
  };
  updateHeaderHeight();
  if (window.ResizeObserver) {
    const sizingObserver = new ResizeObserver(updateHeaderHeight);
    if (header) sizingObserver.observe(header);
    if (contactFooter) sizingObserver.observe(contactFooter);
  }
  window.addEventListener('resize', updateHeaderHeight);
  // Native fragment scrolling can use the 95px fallback before the mobile
  // header is measured. Correct a direct homepage arrival after load.
  if (header && document.documentElement.classList.contains('home-page') && location.hash) {
    window.addEventListener('load', () => requestAnimationFrame(() => {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
      const target = document.getElementById(id);
      if (!target || !target.matches('main > section')) return;
      updateHeaderHeight();
      const gap = target.getBoundingClientRect().top - header.getBoundingClientRect().bottom;
      if (Math.abs(gap) > 1) window.scrollBy({top: gap, behavior: 'instant'});
    }), {once: true});
  }
  // Discrete desktop wheel gestures move between sections. Touch and keyboard stay native.
  if (document.documentElement.classList.contains('home-page')) {
    const sections = [...document.querySelectorAll('main > section')];
    const footer = document.querySelector('.site-footer:not([data-contact-footer])');
    const projectsIndex = sections.findIndex(section => section.id === 'projects');
    const stepMode = window.matchMedia('(min-width: 1001px) and (min-height: 650px)');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let lockedUntil = 0;
    let lastWheel = -Infinity;
    let settling = false;
    let pendingSection = null;
    let lastDirection = 0;
    const moveTo = (index, direction, now) => {
      const target = sections[index] || (index === sections.length ? footer : null);
      if (!target) return false;
      pendingSection = index;
      lastDirection = direction;
      settling = true;
      lockedUntil = now + 850;
      const top = index === sections.length
        ? document.documentElement.scrollHeight - innerHeight
        : target.getBoundingClientRect().top + window.scrollY - header.getBoundingClientRect().height;
      window.scrollTo({top: Math.max(0, top), behavior: reducedMotion.matches ? 'instant' : 'smooth'});
      return true;
    };
    window.addEventListener('wheel', event => {
      if (!stepMode.matches || event.ctrlKey || !event.deltaY || Math.abs(event.deltaX) > Math.abs(event.deltaY) || event.target.closest('input, textarea, select, dialog, [contenteditable="true"]')) return;
      const now = performance.now();
      const idle = now - lastWheel;
      lastWheel = now;
      const direction = Math.sign(event.deltaY);
      if (now < lockedUntil || (settling && idle < 160)) {
        if (direction !== lastDirection && pendingSection !== null) moveTo(pendingSection + direction, direction, now);
        event.preventDefault();
        return;
      }
      settling = false;
      const offset = header.getBoundingClientRect().height;
      const position = window.scrollY + offset;
      let current = 0;
      sections.forEach((section, i) => { if (section.getBoundingClientRect().top + window.scrollY <= position + 2) current = i; });
      if (footer && footer.getBoundingClientRect().top < innerHeight - 2) current = sections.length;
      const rect = sections[current]?.getBoundingClientRect();
      const leaveProjects = current === projectsIndex && direction > 0 && Math.abs(rect.top - offset) <= 2;
      if (rect && !leaveProjects && ((direction > 0 && rect.bottom > innerHeight + 2) || (direction < 0 && rect.top < offset - 2))) return;
      if (moveTo(current + direction, direction, now)) event.preventDefault();
    }, {passive: false});

    const sectionLinks = [...document.querySelectorAll('#site-nav a')];
    let scrollFrame = 0;
    const updateCurrentSection = () => {
      scrollFrame = 0;
      const readingLine = header.getBoundingClientRect().bottom + 80;
      const current = sections.find(section => {
        const rect = section.getBoundingClientRect();
        return rect.top <= readingLine && rect.bottom > readingLine;
      });
      sectionLinks.forEach(link => {
        const pointsToCurrent = current && (link.hasAttribute('data-nav-home')
          ? current === sections[0]
          : current.id && new URL(link.href).hash === '#' + current.id);
        if (pointsToCurrent) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    };
    window.addEventListener('scroll', () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(updateCurrentSection); }, {passive: true});
    window.addEventListener('resize', updateCurrentSection);
    requestAnimationFrame(updateCurrentSection);
    const releaseWheel = () => { lockedUntil = 0; settling = false; pendingSection = null; };
    document.addEventListener('keydown', releaseWheel);
    document.addEventListener('click', event => { if (event.target.closest('a[href*="#"]')) releaseWheel(); });
  }

  const themeToggle = document.querySelector('[data-theme-toggle]');
  if (themeToggle) {
    let themeChange = 0;
    const renderTheme = theme => {
      const change = ++themeChange;
      // Switch the reading palette together; interpolating foreground and
      // background independently briefly destroys contrast between themes.
      document.documentElement.dataset.themeChanging = 'true';
      document.documentElement.dataset.theme = theme;
      document.documentElement.style.colorScheme = theme;
      document.querySelector('meta[name="theme-color"]').content = theme === 'light' ? '#f7f6f2' : '#182225';
      const label = theme === 'dark' ? themeToggle.dataset.light : themeToggle.dataset.dark;
      themeToggle.setAttribute('aria-label', label);
      themeToggle.title = label;
      requestAnimationFrame(() => requestAnimationFrame(() => {
        if (change === themeChange) delete document.documentElement.dataset.themeChanging;
      }));
    };
    renderTheme(document.documentElement.dataset.theme || 'dark');
    themeToggle.hidden = false;
    themeToggle.addEventListener('click', event => {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      renderTheme(theme);
      if (motion && motion.canPlay(event)) motion.play(themeToggle.querySelector(theme === 'light' ? '.theme-moon' : '.theme-sun'), [{transform: 'rotate(-20deg)', opacity: .65}, {transform: 'none', opacity: 1}], 'feedback');
      try { localStorage.setItem('portfolio-theme', theme); } catch (_) {}
    });
  }
  const categories = ['engineering', 'simulation', 'analysis', 'software'];
  const requestedCategory = new URLSearchParams(location.search).get('category');
  const browsingCategory = categories.includes(requestedCategory) ? requestedCategory : 'all';
  const setCategoryLink = (link, category) => {
    const url = new URL(link.href);
    if (category === 'all') url.searchParams.delete('category');
    else url.searchParams.set('category', category);
    link.href = url.pathname + url.search + url.hash;
  };
  const languageSwitch = document.querySelector('[data-language-switch]');
  if (languageSwitch && browsingCategory !== 'all') setCategoryLink(languageSwitch, browsingCategory);
  if (browsingCategory !== 'all') document.querySelectorAll('[data-project-index-link]').forEach(link => {
    const url = new URL(link.href);
    url.hash = browsingCategory;
    link.href = url.pathname + url.hash;
  });
  const carousel = document.querySelector('[data-carousel]');
  if (carousel) {
    const allCards = [...carousel.querySelectorAll('.project-card')];
    const category = carousel.hasAttribute('data-home-carousel') ? 'all' : browsingCategory;
    const cards = allCards.filter(card => category === 'all' || card.dataset.category === category);
    allCards.forEach(card => { card.hidden = true; });
    cards.forEach(card => setCategoryLink(card.querySelector('a'), category));
    const heading = carousel.querySelector('h2');
    if (heading) heading.textContent = carousel.getAttribute('data-title-' + category);
    const mobile = window.matchMedia('(max-width: 600px)');
    const tablet = window.matchMedia('(max-width: 1000px)');
    let index = 0;
    const grid = carousel.querySelector('.project-grid');
    let measuredSize = '';
    // Reserve the tallest card in this collection without truncating any copy.
    // All measurements happen synchronously, before the browser paints.
    const measureHeight = () => {
      const size = grid.getBoundingClientRect().width + ':' + getComputedStyle(grid).fontSize;
      if (size === measuredSize) return;
      measuredSize = size;
      // A new viewport invalidates distances captured for the previous layout.
      if (motion) cards.forEach(card => motion.stop(card));
      grid.style.minHeight = '';
      const hidden = cards.map(card => card.hidden);
      cards.forEach(card => { card.hidden = false; });
      const height = Math.max(0, ...cards.map(card => card.getBoundingClientRect().height));
      cards.forEach((card, i) => { card.hidden = hidden[i]; });
      grid.style.minHeight = Math.ceil(height) + 'px';
    };
    const render = () => {
      const count = Math.min(cards.length, mobile.matches ? 1 : tablet.matches ? 2 : 4);
      carousel.querySelector('.carousel-controls').hidden = cards.length <= count;
      cards.forEach((card, i) => {
        const offset = (i - index + cards.length) % cards.length;
        card.hidden = offset >= count;
        card.style.order = offset;
      });
      for (let step = 0; step < cards.length; step++) grid.append(cards[(index + step) % cards.length]);
      measureHeight();
      carousel.querySelector('[data-position]').textContent = `${carousel.dataset.positionLabel}: ${index + 1}${count > 1 ? '–' + ((index + count - 1) % cards.length + 1) : ''} / ${cards.length}`;
    };
    carousel.classList.add('enhanced-carousel');
    carousel.querySelector('.carousel-controls').hidden = false;
    const move = (direction, event) => {
      const before = new Map(cards.filter(card => !card.hidden).map(card => [card, {
        left: card.getBoundingClientRect().left,
        opacity: getComputedStyle(card).opacity
      }]));
      if (motion) cards.forEach(card => motion.stop(card));
      index = (index + direction + cards.length) % cards.length;
      render();
      if (!motion || !motion.canPlay(event)) return;
      cards.filter(card => !card.hidden).forEach(card => {
        const previous = before.get(card);
        const current = card.getBoundingClientRect();
        // Enter beside the moving row, rather than over its last card.
        const stride = mobile.matches ? 12 : current.width + parseFloat(getComputedStyle(grid).columnGap);
        const distance = previous ? previous.left - current.left : direction * stride;
        motion.play(card, [{transform: `translateX(${distance}px)`, opacity: previous ? previous.opacity : .72}, {transform: 'none', opacity: 1}], 'change');
      });
    };
    carousel.querySelector('[data-prev]').addEventListener('click', event => move(-1, event));
    carousel.querySelector('[data-next]').addEventListener('click', event => move(1, event));
    mobile.addEventListener('change', render);
    tablet.addEventListener('change', render);
    render();
    if (window.ResizeObserver) new ResizeObserver(measureHeight).observe(grid);
    document.fonts.ready.then(() => { measuredSize = ''; measureHeight(); });
  }
  const viewer = document.querySelector('.image-viewer');
  if (viewer && typeof viewer.showModal === 'function') {
    let opener;
    document.querySelectorAll('[data-image-preview]').forEach(link => {
      link.addEventListener('click', event => {
        // Keep the native link available for opening originals in another tab.
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        opener = link;
        const image = viewer.querySelector('img');
        const thumbnail = link.querySelector('img');
        // Reserve the original's proportions before its full-resolution file loads.
        const width = Number(thumbnail.getAttribute('width'));
        const height = Number(thumbnail.getAttribute('height'));
        image.width = width;
        image.height = height;
        image.style.setProperty('--image-width', width + 'px');
        image.style.setProperty('--image-ratio', width / height);
        image.src = link.href;
        image.alt = thumbnail.alt;
        viewer.querySelector('p').textContent = image.alt;
        viewer.showModal();
        if (motion && motion.canPlay(event)) motion.play(viewer, [{opacity: .7, transform: 'scale(.985)'}, {opacity: 1, transform: 'none'}], 'overlay');
      });
    });
    let closeSequence = 0;
    const closeViewer = event => {
      const sequence = ++closeSequence;
      // Preserve the current entrance/exit state before cancelling it.
      const style = getComputedStyle(viewer);
      const opacity = style.opacity;
      const transform = style.transform;
      const animation = motion && motion.canPlay(event) ? motion.play(viewer, [{opacity, transform}, {opacity: .5, transform}], 'exit') : null;
      const finish = () => { if (sequence === closeSequence && viewer.open) viewer.close(); };
      if (animation) animation.finished.then(finish, finish);
      else finish();
    };
    viewer.querySelector('[data-close-image]').addEventListener('click', closeViewer);
    viewer.addEventListener('close', () => { closeSequence++; if (motion) motion.stop(viewer); if (opener) opener.focus({preventScroll: true}); });
    viewer.addEventListener('click', event => {
      const box = viewer.getBoundingClientRect();
      if (event.target === viewer && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) closeViewer(event);
    });
  }

  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('#site-nav');
  if (toggle && nav) {
    toggle.hidden = false;
    nav.classList.add('enhanced-nav');
    const close = () => {
      if (motion) motion.stop(nav);
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      updateHeaderHeight();
    };
    toggle.addEventListener('click', event => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      if (!open) { close(); return; }
      toggle.setAttribute('aria-expanded', 'true');
      nav.classList.add('is-open');
      updateHeaderHeight();
      if (motion && motion.canPlay(event)) motion.play(nav, [{opacity: .7, transform: 'translateY(-4px)'}, {opacity: 1, transform: 'none'}], 'change');
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        close();
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', close);
  }

  const controls = document.querySelector('[data-filter-controls]');
  if (controls) {
    controls.hidden = false;
    const buttons = [...controls.querySelectorAll('[data-filter]')];
    const cards = [...document.querySelectorAll('[data-project]')];
    const chapters = [...document.querySelectorAll('[data-category-section]')];
    const count = controls.querySelector('[data-results-count]');
    const apply = category => {
      const valid = buttons.some(button => button.dataset.filter === category);
      const selected = valid ? category : 'all';
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === selected)));
      chapters.forEach(chapter => {
        chapter.hidden = selected !== 'all' && chapter.dataset.categorySection !== selected;
      });
      cards.forEach(card => {
        card.hidden = selected !== 'all' && card.dataset.category !== selected;
        setCategoryLink(card.querySelector('a'), selected);
      });
      count.textContent = String(cards.filter(card => !card.hidden).length);
      if (languageSwitch) {
        const url = new URL(languageSwitch.href);
        url.hash = selected === 'all' ? '' : selected;
        languageSwitch.href = url.pathname + url.hash;
      }
    };
    buttons.forEach(button => button.addEventListener('click', event => {
      const category = button.dataset.filter;
      history.replaceState(null, '', location.pathname + location.search + (category === 'all' ? '' : '#' + category));
      apply(category);
    }));
    const applyFragment = () => {
      const category = location.hash.slice(1);
      apply(category);
      const chapter = chapters.find(item => item.dataset.categorySection === category);
      if (chapter) requestAnimationFrame(() => chapter.scrollIntoView({ block: 'start', behavior: 'instant' }));
    };
    applyFragment();
    window.addEventListener('hashchange', applyFragment);
  }

  const form = document.querySelector('#contact-form');
  if (form && window.fetch && window.FormData && window.AbortController) {
    form.noValidate = true;
    const button = form.querySelector('button[type="submit"]');
    const status = document.querySelector('#contact-status');
    const idleLabel = button.textContent;
    const fields = [...form.querySelectorAll('[required]')];
    let sending = false;
    const report = (message, state) => { status.textContent = message; status.dataset.state = state; };
    fields.forEach(field => field.addEventListener('input', () => {
      if (field.value.trim() && field.checkValidity()) {
        field.removeAttribute('aria-invalid');
        field.removeAttribute('aria-describedby');
      }
      // The shared explanation still belongs to every uncorrected field.
      if (!sending && !fields.some(input => input.getAttribute('aria-invalid') === 'true')) report('', '');
    }));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (sending) return;
      const invalid = fields.filter(field => !field.value.trim() || !field.checkValidity());
      fields.forEach(field => {
        if (invalid.includes(field)) {
          field.setAttribute('aria-invalid', 'true');
          field.setAttribute('aria-describedby', 'contact-status');
        } else {
          field.removeAttribute('aria-invalid');
          field.removeAttribute('aria-describedby');
        }
      });
      if (invalid.length) {
        report(form.dataset.invalid, 'error');
        invalid[0].focus();
        return;
      }
      if (form.elements._gotcha.value) return;
      sending = true;
      fields.forEach(field => { field.readOnly = true; });
      button.disabled = true;
      button.textContent = form.dataset.sending;
      form.setAttribute('aria-busy', 'true');
      report(form.dataset.sending, 'sending');
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(form.action, {
          method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' }, signal: controller.signal
        });
        if (!response.ok) throw new Error('Delivery failed');
        form.reset();
        report(form.dataset.success, 'success');
      } catch {
        report(form.dataset.failure, 'error');
      } finally {
        clearTimeout(timeout);
        sending = false;
        fields.forEach(field => { field.readOnly = false; });
        button.disabled = false;
        button.textContent = idleLabel;
        form.removeAttribute('aria-busy');
      }
    });
  }
})();
