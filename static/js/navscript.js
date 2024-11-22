document.addEventListener('DOMContentLoaded', function () {
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');

  function toggleNav() {
    navMenu.classList.toggle('hidden');
    navToggle.setAttribute('aria-expanded', navMenu.classList.contains('hidden') ? 'false' : 'true');
  }

  navToggle.addEventListener('click', toggleNav);

  // Close navigation when clicking outside
  document.addEventListener('click', function (event) {
    const isClickInside = navToggle.contains(event.target) || navMenu.contains(event.target);
    if (!isClickInside && !navMenu.classList.contains('hidden')) {
      navMenu.classList.add('hidden');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Close navigation when pressing Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !navMenu.classList.contains('hidden')) {
      navMenu.classList.add('hidden');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
});
