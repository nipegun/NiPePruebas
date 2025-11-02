(function () {
  const root = document.documentElement;
  const body = document.body;
  const toggle = document.getElementById('colorScheme');
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  const storageKey = 'luci-theme-modern-scheme';

  function applyScheme(scheme) {
    if (scheme === 'light') {
      root.classList.add('light');
      body.dataset.colorScheme = 'light';
    } else {
      root.classList.remove('light');
      body.dataset.colorScheme = 'dark';
    }
    localStorage.setItem(storageKey, scheme);
  }

  function toggleScheme() {
    const current = body.dataset.colorScheme === 'light' ? 'dark' : 'light';
    applyScheme(current);
  }

  function loadScheme() {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      applyScheme(stored);
    } else {
      applyScheme(prefersDark.matches ? 'dark' : 'light');
    }
  }

  function handlePrefersChange(event) {
    if (!localStorage.getItem(storageKey)) {
      applyScheme(event.matches ? 'dark' : 'light');
    }
  }

  function trapFocus(element) {
    const focusableSelectors = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])'
    ];
    const focusables = element.querySelectorAll(focusableSelectors.join(','));
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    function loopFocus(event) {
      if (event.key !== 'Tab') return;
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    element.addEventListener('keydown', loopFocus);
  }

  function toggleSidebar() {
    const isOpen = sidebar.classList.toggle('is-open');
    sidebar.setAttribute('aria-hidden', String(!isOpen));
    if (isOpen) {
      trapFocus(sidebar);
      sidebar.querySelector('a, button')?.focus();
    }
  }

  loadScheme();
  prefersDark.addEventListener('change', handlePrefersChange);

  if (toggle) {
    toggle.addEventListener('click', toggleScheme);
  }

  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener('click', toggleSidebar);
    sidebar.setAttribute('aria-hidden', 'true');
  }
})();
