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
    const controls = carousel.querySelector('.carousel-controls');
    const pagination = carousel.querySelector('[data-carousel-pagination]');
    let refreshImages = () => {};
    if (carousel.hasAttribute('data-home-carousel')) {
      const prepared = new WeakSet();
      const connection = navigator.connection;
      let ready = false;
      let busy = false;
      let scheduled = false;
      let queue = [];
      const canPrepare = () => ready && !document.hidden &&
        !connection?.saveData && !['slow-2g', '2g'].includes(connection?.effectiveType);
      const schedule = () => {
        if (busy || scheduled || !queue.length || !canPrepare()) return;
        scheduled = true;
        const prepare = () => {
          scheduled = false;
          if (!canPrepare() || busy) return;
          const image = queue.shift();
          if (!image) return;
          busy = true;
          prepared.add(image);
          image.fetchPriority = 'low';
          image.loading = 'eager';
          const decoded = typeof image.decode === 'function' ? image.decode() :
            image.complete ? Promise.resolve() : new Promise(resolve => {
              image.addEventListener('load', resolve, {once: true});
              image.addEventListener('error', resolve, {once: true});
            });
          // A failed image must not stall the queue or reject into the page.
          decoded.catch(() => {}).finally(() => { busy = false; schedule(); });
        };
        if (window.requestIdleCallback) window.requestIdleCallback(prepare, {timeout: 1500});
        else window.setTimeout(prepare, 0);
      };
      refreshImages = (urgent = false) => {
        if (urgent && !document.hidden) cards.filter(card => !card.hidden).forEach(card => {
          const image = card.querySelector('img');
          prepared.add(image);
          image.fetchPriority = 'auto';
          image.loading = 'eager';
        });
        const count = Math.min(cards.length, mobile.matches ? 1 : tablet.matches ? 2 : 4);
        const offsets = [...Array(count).keys(), count, -1];
        queue = [...new Set(offsets.map(offset => cards[(index + offset + cards.length) % cards.length].querySelector('img')))]
          .filter(image => !prepared.has(image));
        schedule();
      };
      const afterLoad = () => window.setTimeout(() => { ready = true; refreshImages(); }, 500);
      if (document.readyState === 'complete') afterLoad();
      else window.addEventListener('load', afterLoad, {once: true});
      document.addEventListener('visibilitychange', () => {
        const bounds = carousel.getBoundingClientRect();
        refreshImages(!document.hidden && bounds.top < window.innerHeight && bounds.bottom > 0);
      });
      connection?.addEventListener('change', () => refreshImages());
      if (window.IntersectionObserver) new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !document.hidden) refreshImages(true);
      }).observe(carousel);
    }
    let focusedControl = null;
    if (pagination) {
      // CSS may hide a focused control before the breakpoint callback runs.
      // Remember it so focus can move to the newly visible control set.
      document.addEventListener('focusin', event => {
        focusedControl = pagination.contains(event.target) || controls.contains(event.target) ? event.target : null;
      });
      document.addEventListener('pointerdown', event => {
        if (!pagination.contains(event.target) && !controls.contains(event.target)) focusedControl = null;
      }, {passive: true});
      window.addEventListener('blur', () => { focusedControl = null; });
    }
    const dotButtons = pagination ? Array.from({length: Math.min(5, cards.length)}, () => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'carousel-dot';
      pagination.querySelector('[data-carousel-dots]').append(button);
      return button;
    }) : [];
    const updatePagination = () => {
      const start = Math.max(0, Math.min(index - 2, cards.length - dotButtons.length));
      dotButtons.forEach((button, offset) => {
        const slide = start + offset;
        button.dataset.slideIndex = slide;
        button.setAttribute('aria-label', `${carousel.dataset.selectProject}: ${cards[slide].querySelector('h3').textContent}`);
        if (slide === index) button.setAttribute('aria-current', 'true');
        else button.removeAttribute('aria-current');
        button.toggleAttribute('data-more', (offset === 0 && start > 0) || (offset === dotButtons.length - 1 && start + dotButtons.length < cards.length));
      });
    };
    let gesture = null;
    let suppressTouchClickUntil = 0;
    let measuredSize = '';
    const positionControls = () => {
      if (!mobile.matches || controls.hidden) return;
      const image = cards[index].querySelector('.card-image').getBoundingClientRect();
      const wrapper = controls.parentElement.getBoundingClientRect();
      controls.style.setProperty('--carousel-controls-top', image.bottom - wrapper.top + 12 + 'px');
    };
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
      positionControls();
    };
    const render = (prepareVisible = false) => {
      const count = Math.min(cards.length, mobile.matches ? 1 : tablet.matches ? 2 : 4);
      const focusTarget = focusedControl || document.activeElement;
      const focusWasInDots = pagination && pagination.contains(focusTarget);
      const focusWasInArrows = controls.contains(focusTarget);
      const showPagination = pagination && mobile.matches && cards.length > 1;
      controls.hidden = cards.length <= count || showPagination;
      if (pagination) pagination.hidden = !showPagination;
      carousel.classList.toggle('has-carousel-controls', !controls.hidden);
      cards.forEach((card, i) => {
        const offset = (i - index + cards.length) % cards.length;
        card.hidden = offset >= count;
        card.style.order = offset;
      });
      for (let step = 0; step < cards.length; step++) grid.append(cards[(index + step) % cards.length]);
      measureHeight();
      positionControls();
      updatePagination();
      refreshImages(prepareVisible);
      if (showPagination && focusWasInArrows) dotButtons.find(button => Number(button.dataset.slideIndex) === index).focus({preventScroll: true});
      else if (!showPagination && focusWasInDots && !controls.hidden) controls.querySelector('[data-next]').focus({preventScroll: true});
      carousel.querySelector('[data-position]').textContent = `${carousel.dataset.positionLabel}: ${index + 1}${count > 1 ? '–' + ((index + count - 1) % cards.length + 1) : ''} / ${cards.length}`;
    };
    carousel.classList.add('enhanced-carousel');
    carousel.querySelector('.carousel-controls').hidden = false;
    const move = (direction, event) => {
      cancelSwipe();
      const before = new Map(cards.filter(card => !card.hidden).map(card => [card, {
        left: card.getBoundingClientRect().left,
        opacity: getComputedStyle(card).opacity
      }]));
      if (motion) cards.forEach(card => motion.stop(card));
      index = (index + direction + cards.length) % cards.length;
      render(true);
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
    dotButtons.forEach(button => button.addEventListener('click', event => {
      const target = Number(button.dataset.slideIndex);
      if (target !== index) move(target - index, event);
      dotButtons.find(dot => Number(dot.dataset.slideIndex) === index).focus({preventScroll: true});
    }));
    const clearSwipeCard = card => {
      if (motion) motion.stop(card);
      card.classList.remove('swipe-adjacent');
      card.style.removeProperty('transform');
      card.inert = false;
      card.removeAttribute('aria-hidden');
    };
    const cancelSwipe = () => {
      if (!gesture) return;
      const previous = gesture;
      gesture = null;
      if (previous.horizontal) suppressTouchClickUntil = performance.now() + 600;
      if (grid.hasPointerCapture(previous.pointerId)) grid.releasePointerCapture(previous.pointerId);
      cards.forEach(clearSwipeCard);
      grid.classList.remove('is-swiping');
      render();
    };
    const settleSwipe = commit => {
      const current = gesture;
      if (!current) return;
      if (!current.horizontal) { gesture = null; return; }
      current.settling = true;
      suppressTouchClickUntil = performance.now() + 600;
      if (grid.hasPointerCapture(current.pointerId)) grid.releasePointerCapture(current.pointerId);
      if (commit) index = (index + current.direction + cards.length) % cards.length;
      const finish = () => {
        if (gesture !== current) return;
        gesture = null;
        cards.forEach(clearSwipeCard);
        grid.classList.remove('is-swiping');
        render(true);
      };
      if (!motion || !motion.canPlay()) { finish(); return; }
      const outgoing = motion.play(current.card, [
        {transform: `translateX(${current.dx}px)`},
        {transform: `translateX(${commit ? -current.direction * current.width : 0}px)`}
      ], 'change');
      const incoming = motion.play(current.adjacent, [
        {transform: `translateX(${current.dx + current.direction * current.width}px)`},
        {transform: `translateX(${commit ? 0 : current.direction * current.width}px)`}
      ], 'change');
      Promise.all([outgoing, incoming].filter(Boolean).map(animation => animation.finished.catch(() => {}))).then(finish);
    };
    grid.addEventListener('pointerdown', event => {
      if (!mobile.matches || cards.length < 2 || event.pointerType !== 'touch' || !event.isPrimary) return;
      cancelSwipe();
      suppressTouchClickUntil = 0;
      if (motion) cards.forEach(card => motion.stop(card));
      gesture = {pointerId: event.pointerId, x: event.clientX, y: event.clientY, card: cards[index], width: grid.getBoundingClientRect().width, dx: 0, horizontal: false};
    });
    grid.addEventListener('pointermove', event => {
      const current = gesture;
      if (!current || current.settling || current.pointerId !== event.pointerId) return;
      const dx = event.clientX - current.x;
      const dy = event.clientY - current.y;
      if (!current.horizontal) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) < 10) return;
        if (Math.abs(dx) <= Math.abs(dy) * 1.2) { gesture = null; return; }
        current.horizontal = true;
        grid.setPointerCapture(event.pointerId);
        grid.classList.add('is-swiping');
        current.card.inert = true;
        current.card.setAttribute('aria-hidden', 'true');
      }
      event.preventDefault();
      current.dx = Math.max(-current.width, Math.min(current.width, dx));
      const direction = dx < 0 ? 1 : -1;
      if (current.direction !== direction) {
        if (current.adjacent) { clearSwipeCard(current.adjacent); current.adjacent.hidden = true; }
        current.direction = direction;
        current.adjacent = cards[(index + direction + cards.length) % cards.length];
        current.adjacent.hidden = false;
        current.adjacent.inert = true;
        current.adjacent.setAttribute('aria-hidden', 'true');
        current.adjacent.classList.add('swipe-adjacent');
        refreshImages(true);
      }
      current.card.style.transform = `translateX(${current.dx}px)`;
      current.adjacent.style.transform = `translateX(${current.dx + direction * current.width}px)`;
    });
    grid.addEventListener('pointerup', event => {
      if (gesture && gesture.pointerId === event.pointerId) settleSwipe(Math.abs(gesture.dx) >= 48);
    });
    grid.addEventListener('pointercancel', cancelSwipe);
    grid.addEventListener('lostpointercapture', event => {
      // Touch starts with implicit capture on the image/link. Its transfer
      // to this grid bubbles a separate loss event from that original target.
      if (event.target === grid && gesture && !gesture.settling) cancelSwipe();
    });
    grid.addEventListener('click', event => {
      if (event.detail > 0 && performance.now() < suppressTouchClickUntil) {
        event.preventDefault();
        event.stopPropagation();
      }
    }, {capture: true});
    const resizeCarousel = () => { cancelSwipe(); render(true); };
    mobile.addEventListener('change', resizeCarousel);
    tablet.addEventListener('change', resizeCarousel);
    window.addEventListener('resize', resizeCarousel);
    document.addEventListener('keydown', cancelSwipe);
    document.addEventListener('visibilitychange', () => { if (document.hidden) cancelSwipe(); });
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', cancelSwipe);
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
    const compact = window.matchMedia('(max-width: 900px)');
    let menuSequence = 0;
    const close = (event, immediate = false) => {
      const sequence = ++menuSequence;
      const visible = nav.classList.contains('is-open');
      const style = visible ? getComputedStyle(nav) : null;
      const clipPath = style ? style.clipPath : 'none';
      const transform = style ? style.transform : 'none';
      if (motion) motion.stop(nav);
      toggle.setAttribute('aria-expanded', 'false');
      nav.inert = compact.matches;
      const finish = () => {
        if (sequence !== menuSequence) return;
        if (motion) motion.stop(nav);
        nav.classList.remove('is-open');
      };
      const animation = visible && compact.matches && !immediate && motion && motion.canPlay(event)
        ? motion.play(nav, [{clipPath, transform}, {clipPath: 'inset(0 0 100% 0)', transform: 'translateY(-6px)'}], 'exit')
        : null;
      if (animation) animation.finished.then(finish, finish);
      else finish();
    };
    nav.inert = compact.matches;
    toggle.addEventListener('click', event => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      if (!open) { close(event); return; }
      const visible = nav.classList.contains('is-open');
      const style = visible ? getComputedStyle(nav) : null;
      const clipPath = style ? style.clipPath : 'inset(0 0 100% 0)';
      const transform = style ? style.transform : 'translateY(-6px)';
      ++menuSequence;
      if (motion) motion.stop(nav);
      toggle.setAttribute('aria-expanded', 'true');
      nav.inert = false;
      nav.classList.add('is-open');
      if (motion && motion.canPlay(event)) motion.play(nav, [{clipPath, transform}, {clipPath: 'inset(0)', transform: 'none'}], 'change');
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(undefined, true); });
    document.addEventListener('pointerdown', event => {
      if (toggle.getAttribute('aria-expanded') === 'true' && !nav.contains(event.target) && !toggle.contains(event.target)) close();
    });
    nav.addEventListener('focusout', event => {
      if (!nav.contains(event.relatedTarget) && !toggle.contains(event.relatedTarget)) close(undefined, true);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        close(undefined, true);
        toggle.focus({preventScroll: true});
      }
    });
    compact.addEventListener('change', () => close(undefined, true));
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
