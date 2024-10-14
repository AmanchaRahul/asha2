// Navbar animation function
function updateNavAnimation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const isMobile = window.innerWidth < 768; // Adjust this value based on your mobile breakpoint
  
    navLinks.forEach((link, index) => {
      if (isMobile) {
        link.style.animation = 'none';
      } else {
        const duration = 1 + (index * 0.1); // Varies from 2s to 2.8s
        link.style.animation = `moveRight ${duration}s infinite ease-in-out`;
      }
    });
  }
  
  // Initialize navbar animation
  function initNavAnimation() {
    updateNavAnimation();
    window.addEventListener('resize', updateNavAnimation);
  }
  
  // Toggle functionality for mobile menu
  function initMobileMenu() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
  
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('hidden');
    });
  }
  
  // Initialize all functionality when the DOM is loaded
  document.addEventListener('DOMContentLoaded', () => {
    initNavAnimation();
    initMobileMenu();
  });
  
  
  
  // Add fade-in animation for elements as they come into view
  function initFadeInAnimation() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const fadeInObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });
  
    fadeElements.forEach(element => {
      fadeInObserver.observe(element);
    });
  }
  
  // Initialize fade-in animation
  initFadeInAnimation();