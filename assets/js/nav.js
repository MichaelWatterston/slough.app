(function () {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const burger = nav.querySelector('.nav-burger');
  const links = nav.querySelector('.nav-links');
  if (!burger || !links) return;

  burger.setAttribute('aria-expanded', 'false');
  burger.setAttribute('aria-controls', 'primary-nav');
  links.id = links.id || 'primary-nav';

  const close = () => {
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
  };
  const toggle = () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  };

  burger.addEventListener('click', toggle);

  links.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') close();
  });

  document.addEventListener('click', (e) => {
    if (!nav.classList.contains('is-open')) return;
    if (!nav.contains(e.target)) close();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 880) close();
  });
})();

// Pause control for looping animations. Only added on pages that have one running,
// so nothing appears when the visitor has Reduce Motion on (the loops are off then).
(function () {
  if (!document.getAnimations) return;
  const loops = document.getAnimations().some((a) => a.effect && a.effect.getTiming().iterations === Infinity);
  if (!loops) return;
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'motion-toggle';
  btn.textContent = 'Pause animations';
  btn.addEventListener('click', () => {
    const paused = document.documentElement.classList.toggle('motion-paused');
    btn.textContent = paused ? 'Play animations' : 'Pause animations';
  });
  const skip = document.querySelector('.skip-link');
  if (skip) skip.after(btn); else document.body.prepend(btn);
})();
