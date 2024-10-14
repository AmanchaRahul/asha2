// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    if (targetId.startsWith('#')) {
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      } else {
        console.error(`Element with selector ${targetId} not found.`);
      }
    } else {
      console.error(`Invalid selector: ${targetId}`);
    }
  });
});

// Add hover effect to images
const images = document.querySelectorAll('.image-row img');
images.forEach(img => {
  img.addEventListener('mouseover', () => {
    img.style.filter = 'brightness(0.8)';
  });
  img.addEventListener('mouseout', () => {
    img.style.filter = 'brightness(1)';
  });
});
