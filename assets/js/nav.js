(function () {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const burger = nav.querySelector('.nav-burger');
  const links = nav.querySelector('.nav-links');
  if (!burger || !links) return;

  burger.setAttribute('role', 'button');
  burger.setAttribute('tabindex', '0');
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
  burger.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggle();
    }
  });

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
