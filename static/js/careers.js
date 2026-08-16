/**
 * Careers Department Filter AJAX Handling
 * Matches projects filter characteristics 100%
 */

document.addEventListener('DOMContentLoaded', () => {
  const careersContainer = document.getElementById('careers-ajax-container');
  if (!careersContainer) return;

  function getHeaderOffset() {
    const headerHeightVar = getComputedStyle(document.documentElement).getPropertyValue('--header-height');
    return parseInt(headerHeightVar, 10) || 88;
  }

  function smoothScrollTo(targetY, duration = 420) {
    const startY = window.pageYOffset;
    const distance = targetY - startY;
    if (Math.abs(distance) < 4) return;

    let startTime = null;

    function easeInOutCubic(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function animationStep(currentTime) {
      if (!startTime) startTime = currentTime;
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = easeInOutCubic(progress);

      window.scrollTo(0, startY + distance * ease);

      if (progress < 1) {
        requestAnimationFrame(animationStep);
      }
    }

    requestAnimationFrame(animationStep);
  }

  function scrollToFilterTop() {
    const sectionHeader = document.querySelector('.careers-openings__header') || careersContainer;
    if (!sectionHeader) return;

    const headerOffset = getHeaderOffset();
    const rect = sectionHeader.getBoundingClientRect();
    const targetY = Math.max(0, rect.top + window.pageYOffset - headerOffset + 60);

    smoothScrollTo(targetY, 420);
  }

  async function loadCareers(url, pushState = true) {
    // 1. Smooth scroll to anchor position
    scrollToFilterTop();

    try {
      const response = await fetch(url, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const htmlText = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(htmlText, 'text/html');

      // 2. Direct in-place replacement of filter navigation
      const newFilterNav = doc.getElementById('careers-filter-nav');
      const currentFilterNav = document.getElementById('careers-filter-nav');
      if (newFilterNav && currentFilterNav) {
        currentFilterNav.innerHTML = newFilterNav.innerHTML;
      }

      // 3. Direct in-place replacement of careers list with staggered slide-in
      const newCareersList = doc.querySelector('.careers-list');
      const currentCareersList = document.querySelector('.careers-list');
      if (newCareersList && currentCareersList) {
        currentCareersList.classList.remove('is-animating');
        currentCareersList.innerHTML = newCareersList.innerHTML;
        void currentCareersList.offsetWidth; // force reflow
        currentCareersList.classList.add('is-animating');
      }

      // 4. Update title
      if (doc.title) {
        document.title = doc.title;
      }

      if (pushState) {
        history.pushState({ url }, '', url);
      }
    } catch (error) {
      console.error('Failed to load careers via AJAX:', error);
      window.location.href = url;
    }
  }

  // Intercept Filter clicks
  careersContainer.addEventListener('click', (event) => {
    const filterBtn = event.target.closest('.projects-filter-btn');
    if (filterBtn) {
      event.preventDefault();
      const targetUrl = filterBtn.getAttribute('href');
      if (targetUrl) {
        loadCareers(targetUrl, true);
      }
    }
  });

  // Handle Browser Back/Forward buttons
  window.addEventListener('popstate', (event) => {
    const targetUrl = event.state?.url || window.location.href;
    loadCareers(targetUrl, false);
  });
});
