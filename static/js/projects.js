/**
 * Projects Filter & Pagination AJAX Handling
 * Smooth filter transitions with scroll-to-view
 */

document.addEventListener('DOMContentLoaded', () => {
  const projectsContainer = document.getElementById('projects-ajax-container');
  if (!projectsContainer) return;

  function getHeaderOffset() {
    const headerHeightVar = getComputedStyle(document.documentElement).getPropertyValue('--header-height');
    return parseInt(headerHeightVar, 10) || 88;
  }

  function smoothScrollTo(targetY, duration = 600) {
    const startY = window.pageYOffset;
    const distance = targetY - startY;
    if (Math.abs(distance) < 4) return;

    let startTime = null;

    // Gentle easeInOutCubic curve
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
    const filterNav = document.getElementById('projects-filter-nav');
    if (!filterNav) return;

    const headerOffset = getHeaderOffset();
    const rect = filterNav.getBoundingClientRect();
    const targetY = Math.max(0, rect.top + window.pageYOffset - headerOffset + 60);

    smoothScrollTo(targetY, 420);
  }

  async function loadProjects(url, pushState = true) {
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
      const newFilterNav = doc.getElementById('projects-filter-nav');
      const currentFilterNav = document.getElementById('projects-filter-nav');
      if (newFilterNav && currentFilterNav) {
        currentFilterNav.innerHTML = newFilterNav.innerHTML;
      }

      // 3. Direct in-place replacement of projects list with subtle staggered slide-in
      const newProjectsList = doc.querySelector('.projects-list');
      const currentProjectsList = document.querySelector('.projects-list');
      if (newProjectsList && currentProjectsList) {
        currentProjectsList.classList.remove('is-animating');
        currentProjectsList.innerHTML = newProjectsList.innerHTML;
        void currentProjectsList.offsetWidth; // force reflow
        currentProjectsList.classList.add('is-animating');
      }

      // 4. Direct in-place replacement of pagination
      const newPagination = doc.querySelector('.projects-pagination-wrap');
      const currentPagination = document.querySelector('.projects-pagination-wrap');
      if (newPagination && currentPagination) {
        currentPagination.innerHTML = newPagination.innerHTML;
      }

      // 5. Update title
      if (doc.title) {
        document.title = doc.title;
      }

      if (pushState) {
        history.pushState({ url }, '', url);
      }
    } catch (error) {
      console.error('Failed to load projects via AJAX:', error);
      // Fallback to normal navigation on failure
      window.location.href = url;
    }
  }

  // Intercept Filter, Pagination, and Project Card clicks
  projectsContainer.addEventListener('click', (event) => {
    const filterBtn = event.target.closest('.projects-filter-btn');
    if (filterBtn) {
      event.preventDefault();
      const targetUrl = filterBtn.getAttribute('href');
      if (targetUrl) {
        loadProjects(targetUrl, true);
      }
      return;
    }

    const paginationLink = event.target.closest('.projects-pagination-wrap a');
    if (paginationLink) {
      event.preventDefault();
      const targetUrl = paginationLink.getAttribute('href');
      if (targetUrl) {
        loadProjects(targetUrl, true);
      }
      return;
    }

    // Allow clicking anywhere on the project band to navigate
    const projectCard = event.target.closest('.project-band');
    if (projectCard) {
      // If the click is on an interactive element (link or button), let default behavior work
      if (event.target.closest('a, button')) {
        return;
      }
      const link = projectCard.querySelector('.project-band__link, .project-band__title-link');
      if (link && link.getAttribute('href')) {
        window.location.href = link.getAttribute('href');
      }
    }
  });

  // Handle Browser Back/Forward buttons
  window.addEventListener('popstate', (event) => {
    const targetUrl = event.state?.url || window.location.href;
    loadProjects(targetUrl, false);
  });
});
