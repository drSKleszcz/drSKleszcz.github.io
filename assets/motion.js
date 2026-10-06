/* Small, interruptible enhancements. Content and navigation never wait for motion. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const coarse = matchMedia('(hover: none), (pointer: coarse)');
  const tokens = getComputedStyle(root);
  const duration = role => parseFloat(tokens.getPropertyValue('--motion-' + role));
  const easing = tokens.getPropertyValue('--ease-ui').trim();
  const active = new Map();
  let settleHero = () => { delete root.dataset.heroEntrance; };
  let settleExpertise = () => {};
  let updateHeroIdle = () => {};
  let keyboard = false;
  try {
    keyboard = sessionStorage.getItem('portfolio-navigation-input') === 'keyboard';
    sessionStorage.removeItem('portfolio-navigation-input');
  } catch (_) {}
  root.dataset.input = keyboard ? 'keyboard' : 'pointer';
  const canPlay = event => !reduced.matches && !keyboard && !document.hidden && (!event || event.detail > 0);
  const stop = element => { const animation = active.get(element); if (animation) animation.cancel(); active.delete(element); };
  const stopAll = () => { settleHero(); settleExpertise(); active.forEach(animation => animation.cancel()); active.clear(); updateHeroIdle(); };
  const play = (element, frames, role = 'change', options = {}) => {
    stop(element);
    if (!canPlay() || !element.animate) return null;
    const animation = element.animate(frames, {duration: duration(role), easing, ...options});
    active.set(element, animation);
    const clear = () => { if (active.get(element) === animation) active.delete(element); };
    animation.finished.then(clear, clear);
    return animation;
  };
  const setInput = value => {
    if (keyboard === value) return;
    keyboard = value;
    root.dataset.input = value ? 'keyboard' : 'pointer';
    updateHeroIdle();
  };
  document.addEventListener('keydown', () => { setInput(true); stopAll(); }, {capture: true});
  document.addEventListener('pointerdown', () => setInput(false), {capture: true, passive: true});
  document.addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse' && (event.movementX || event.movementY)) setInput(false);
  }, {capture: true, passive: true});
  document.addEventListener('wheel', () => setInput(false), {capture: true, passive: true});
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || link.target === '_blank' || link.hasAttribute('download')) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || (url.pathname === location.pathname && url.search === location.search) || !(url.pathname.endsWith('/') || url.pathname.endsWith('.html'))) return;
    try { sessionStorage.setItem('portfolio-navigation-input', keyboard || event.detail === 0 ? 'keyboard' : 'pointer'); } catch (_) {}
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      stopAll();
      // Settle an existing pickup immediately; later pointer hovers use the
      // shorter CSS profile without inheriting the old zoom transition.
      document.querySelectorAll('.project-card-link').forEach(card => {
        card.getAnimations().forEach(animation => animation.finish());
      });
    } else updateHeroIdle();
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopAll(); else updateHeroIdle(); });
  window.addEventListener('pageswap', event => {
    if (event.viewTransition && (keyboard || reduced.matches || coarse.matches)) event.viewTransition.skipTransition();
    stopAll();
  });
  window.portfolioMotion = {canPlay, play, stop};

  // CSS owns the complete pre-paint headline and stage sequence. Without its
  // early flag, every word and diagram stays visible and every link still works.
  const workflow = document.querySelector('[data-hero-workflow]');
  if (workflow) {
    const hero = workflow.closest('.hero');
    const heading = hero.querySelector('h1');
    const stages = [...workflow.querySelectorAll('.workflow-stage')];
    const connector = workflow.querySelector('.workflow-connection');
    const entrance = [
      ...heading.getAnimations({subtree: true}),
      ...stages.flatMap(stage => stage.getAnimations()),
      ...connector.getAnimations()
    ].filter(animation => ['portfolio-sentence-fade', 'portfolio-stage-fade', 'portfolio-connection-fade'].includes(animation.animationName) && animation.playState !== 'finished');
    const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
    let hovered = null;
    let focused = null;
    let openingComplete = !entrance.length;
    let workflowVisible = false;
    let heroVisible = true;
    updateHeroIdle = () => {
      const idle = openingComplete && workflowVisible && heroVisible && !hovered && !focused && !keyboard && !reduced.matches && !document.hidden;
      if (workflow.hasAttribute('data-idle-pulse') !== idle) workflow.toggleAttribute('data-idle-pulse', idle);
    };
    const finishEntrance = () => {
      openingComplete = true;
      delete root.dataset.heroEntrance;
      updateHeroIdle();
    };
    settleHero = finishEntrance;
    hero.addEventListener('pointerdown', finishEntrance, {passive: true});
    Promise.all(entrance.map(animation => animation.finished.catch(() => {}))).then(finishEntrance);
    stages.forEach(stage => {
      stage.addEventListener('pointerenter', event => {
        if (!finePointer.matches || event.pointerType === 'touch') return;
        hovered = stage;
        updateHeroIdle();
      });
      stage.addEventListener('pointerleave', () => {
        if (hovered === stage) hovered = null;
        updateHeroIdle();
      });
      stage.addEventListener('focus', () => {
        focused = stage;
        finishEntrance();
      });
      stage.addEventListener('blur', event => {
        focused = stages.find(candidate => candidate === event.relatedTarget) || null;
        updateHeroIdle();
      });
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        workflowVisible = entries[0].isIntersecting && entries[0].intersectionRatio >= .15;
        updateHeroIdle();
      }, {threshold: .15}).observe(workflow);
      new IntersectionObserver(entries => {
        heroVisible = entries[0].isIntersecting;
        if (!heroVisible) finishEntrance();
        else updateHeroIdle();
      }).observe(hero);
    } else { workflowVisible = true; updateHeroIdle(); }
    window.addEventListener('resize', finishEntrance, {passive: true});
  }

  // The expertise sequence traces only decorative rules and numerals. Reading
  // content remains visible before, during, and without this enhancement.
  const expertise = document.querySelector('.expertise');
  if (expertise && 'IntersectionObserver' in window) {
    let observer;
    settleExpertise = () => { expertise.removeAttribute('data-expertise-animated'); };
    const finalNumber = expertise.querySelector('article:last-child .expertise-number');
    expertise.addEventListener('animationend', event => {
      if (event.target === finalNumber && event.animationName === 'expertise-number') settleExpertise();
    });
    const enterExpertise = () => {
      if (expertise.hasAttribute('data-expertise-seen') || document.hidden) return;
      expertise.setAttribute('data-expertise-seen', '');
      if (canPlay()) expertise.setAttribute('data-expertise-animated', '');
      observer.disconnect();
    };
    observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) enterExpertise();
    }, {threshold: 0, rootMargin: '0px 0px -28% 0px'});
    observer.observe(expertise);
    window.addEventListener('resize', settleExpertise, {passive: true});
    document.addEventListener('visibilitychange', () => {
      if (document.hidden || expertise.hasAttribute('data-expertise-seen')) return;
      const bounds = expertise.getBoundingClientRect();
      if (bounds.top < innerHeight * .72 && bounds.bottom > 0) enterExpertise();
    });
  }
})();
