/**
 * News Filter, Pagination AJAX Handling & Card Click Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  const newsContainer = document.getElementById('news-ajax-container');

  function getHeaderOffset() {
    const headerHeightVar = getComputedStyle(document.documentElement).getPropertyValue('--header-height');
    return parseInt(headerHeightVar, 10) || 88;
  }

  function smoothScrollTo(targetY, duration = 600) {
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
    const filterNav = document.getElementById('news-filter-nav');
    if (!filterNav) return;

    const headerOffset = getHeaderOffset();
    const rect = filterNav.getBoundingClientRect();
    const targetY = Math.max(0, rect.top + window.pageYOffset - headerOffset + 60);

    smoothScrollTo(targetY, 420);
  }

  async function loadNews(url, pushState = true) {
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
      const newFilterNav = doc.getElementById('news-filter-nav');
      const currentFilterNav = document.getElementById('news-filter-nav');
      if (newFilterNav && currentFilterNav) {
        currentFilterNav.innerHTML = newFilterNav.innerHTML;
      }

      // 3. Direct in-place replacement of news list
      const newNewsList = doc.querySelector('.news-listing__articles');
      const currentNewsList = document.querySelector('.news-listing__articles');
      if (newNewsList && currentNewsList) {
        currentNewsList.classList.remove('is-animating');
        currentNewsList.innerHTML = newNewsList.innerHTML;
        void currentNewsList.offsetWidth; // force reflow
        currentNewsList.classList.add('is-animating');
      }

      // 4. Direct in-place replacement of pagination
      const newPagination = doc.querySelector('.news-pagination-wrap');
      const currentPagination = document.querySelector('.news-pagination-wrap');
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
      console.error('Failed to load news via AJAX:', error);
      // Fallback to normal navigation on failure
      window.location.href = url;
    }
  }

  // Intercept Filter and Pagination clicks on news listing
  if (newsContainer) {
    newsContainer.addEventListener('click', (event) => {
      const filterBtn = event.target.closest('.projects-filter-btn');
      if (filterBtn) {
        event.preventDefault();
        const targetUrl = filterBtn.getAttribute('href');
        if (targetUrl) {
          loadNews(targetUrl, true);
        }
        return;
      }

      const paginationLink = event.target.closest('.news-pagination-wrap a');
      if (paginationLink) {
        event.preventDefault();
        const targetUrl = paginationLink.getAttribute('href');
        if (targetUrl) {
          loadNews(targetUrl, true);
        }
        return;
      }
    });

    // Handle Browser Back/Forward buttons
    window.addEventListener('popstate', (event) => {
      const targetUrl = event.state?.url || window.location.href;
      loadNews(targetUrl, false);
    });
  }

  // Global card click handling for .news-row and .news-related-card
  document.addEventListener('click', (event) => {
    // If clicking directly on a link or button, allow native navigation
    if (event.target.closest('a, button')) {
      return;
    }

    const card = event.target.closest('.news-row, .news-related-card');
    if (card) {
      const targetUrl = card.getAttribute('data-url');
      if (targetUrl) {
        window.location.href = targetUrl;
      }
    }
  });
});
