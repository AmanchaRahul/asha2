document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');

  function toggleNav() {
    navMenu.classList.toggle('show'); // Add/remove 'show' to display menu
    navToggle.setAttribute('aria-expanded', navMenu.classList.contains('show') ? 'true' : 'false');
  }

  navToggle.addEventListener('click', toggleNav);

  // Close navigation when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInside = navToggle.contains(event.target) || navMenu.contains(event.target);
    if (!isClickInside && navMenu.classList.contains('show')) {
      toggleNav();
    }
  });

  // Close navigation when pressing Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && navMenu.classList.contains('show')) {
      toggleNav();
    }
  });
});
