/**
 * AL BAHAA CONTRACTING - INTRO PRELOADER & SEAMLESS REVEAL CONTROLLER
 * Production-grade lifecycle management with accessibility, performance, and concurrency guards.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'albahaa_intro_seen_timestamp';
  const SESSION_TTL_MS = 60 * 60 * 1000; // 1 hour cooldown (راحة ساعة)
  const TRANSITION_TRIGGER_TIME = 3.8; // Exactly aligned with Keyframe at 3.753s
  const MAX_STALL_LIMIT_MS = 1500;
  const LOW_POWER_FALLBACK_MS = 1800;

  // Safe Storage Wrapper (Incognito & Sandbox Resilient)
  function isSessionValid() {
    try {
      const params = new URLSearchParams(window.location.search);

      // Force preview whenever ?intro=1 or ?preview_intro=1 is in URL
      if (params.get('intro') === '1' || params.get('preview_intro') === '1') {
        return false;
      }

      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;

      const timestamp = parseInt(raw, 10);
      if (isNaN(timestamp)) return false;

      // Check if last seen was within 1 hour
      return (Date.now() - timestamp) < SESSION_TTL_MS;
    } catch (e) {
      return Boolean(window.__introSeenMemoryFallback);
    }
  }

  function markSessionSeen() {
    try {
      localStorage.setItem(STORAGE_KEY, Date.now().toString());
    } catch (e) {
      window.__introSeenMemoryFallback = true;
    }
  }

  // Instant bypass verification (Deep-links, non-home pages, reduced motion)
  function shouldBypassImmediately() {
    const params = new URLSearchParams(window.location.search);

    // If explicit intro preview requested via URL, play regardless
    if (params.get('intro') === '1' || params.get('preview_intro') === '1') {
      return false;
    }

    // 1. Only run on Home Page (الصفحة الرئيسية فقط)
    const isHomePage = window.location.pathname === '/' || document.body.classList.contains('home-page');
    if (!isHomePage) {
      return true;
    }

    // 2. Cooldown check: 1 hour rest between displays (راحة ساعة بين مرات الظهور)
    if (isSessionValid()) {
      return true;
    }

    // 3. Direct Anchor Deep-links (e.g. #contact, #specialization)
    if (window.location.hash && window.location.hash.length > 1) {
      return true;
    }

    // 4. Accessibility: reduced motion preference
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return true;
    }

    return false;
  }

  function initIntro() {
    console.log('[Intro] initIntro() started on', window.location.href);
    const preloader = document.getElementById('site-preloader');
    if (!preloader) {
      console.warn('[Intro] No #site-preloader element found in DOM!');
      return;
    }

    const video = preloader.querySelector('.intro-video-player');
    const skipBtn = preloader.querySelector('.intro-skip-btn');
    const header = document.getElementById('main-header');
    const main = document.getElementById('main-content');

    // If already seen or bypass requested, purge immediately
    if (shouldBypassImmediately()) {
      console.log('[Intro] shouldBypassImmediately returned true -> removing preloader');
      preloader.remove();
      if (header) header.removeAttribute('inert');
      if (main) main.removeAttribute('inert');
      document.body.classList.remove('intro-active');
      document.body.classList.add('intro-complete');
      return;
    }

    console.log('[Intro] Activating preloader and playing video...');

    // Set initial lock and inert attributes
    document.body.classList.add('intro-active');
    if (header) header.setAttribute('inert', '');
    if (main) main.setAttribute('inert', '');

    let isTransitionStarted = false;
    let stallTimer = null;
    let powerTimer = null;

    // Fast-path destruction & reveal
    function executeReveal(immediate = false) {
      if (isTransitionStarted) return;
      isTransitionStarted = true;
      markSessionSeen();

      clearTimeout(stallTimer);
      clearTimeout(powerTimer);

      // Release focus lock
      if (header) header.removeAttribute('inert');
      if (main) main.removeAttribute('inert');

      document.body.classList.remove('intro-active');
      document.body.classList.add('intro-reveal');

      if (immediate) {
        if (video) {
          video.pause();
          video.removeAttribute('src');
          video.load();
        }
        preloader.remove();
        document.body.classList.add('intro-complete');
        return;
      }

      // Smooth cinematic dissolve
      preloader.classList.add('is-fading-out');

      // Purge DOM and VRAM after CSS transition completes
      setTimeout(() => {
        if (video) {
          video.pause();
          video.removeAttribute('src');
          video.load();
        }
        preloader.remove();
        document.body.classList.add('intro-complete');
      }, 700);
    }

    // Show skip button smoothly after 1.5s
    setTimeout(() => {
      if (skipBtn && !isTransitionStarted) {
        skipBtn.classList.add('is-visible');
      }
    }, 1500);

    if (skipBtn) {
      skipBtn.addEventListener('click', (e) => {
        e.preventDefault();
        executeReveal(true);
      });
    }

    // Back-Forward Cache (bfcache) protection
    window.addEventListener('pageshow', (event) => {
      if (event.persisted) {
        executeReveal(true);
      }
    });

    if (!video) {
      executeReveal(true);
      return;
    }

    let hasStartedPlaying = false;

    // Fallback 1: Low Power Mode or Autoplay Block Safety Net (3 seconds)
    powerTimer = setTimeout(() => {
      if (!hasStartedPlaying) {
        console.warn('[Intro] Video did not start within timeout, revealing content.');
        executeReveal(true);
      }
    }, 3000);

    // Fallback 2: Network Hiccup / Stalled Buffer Guard (only active while playing)
    const resetStallWatchdog = () => {
      if (!hasStartedPlaying) return;
      clearTimeout(stallTimer);
      stallTimer = setTimeout(() => {
        console.warn('[Intro] Video buffer stalled during playback, transitioning gracefully.');
        executeReveal(false);
      }, 2500);
    };

    video.addEventListener('waiting', resetStallWatchdog);
    video.addEventListener('stalled', resetStallWatchdog);

    video.addEventListener('playing', () => {
      hasStartedPlaying = true;
      clearTimeout(stallTimer);
      clearTimeout(powerTimer);
      console.log('[Intro] Video playing smoothly...');
    });

    // Time-based seamless synchronization
    video.addEventListener('timeupdate', () => {
      clearTimeout(stallTimer);
      clearTimeout(powerTimer);

      if (video.currentTime >= TRANSITION_TRIGGER_TIME && !isTransitionStarted) {
        executeReveal(false);
      }
    });

    video.addEventListener('ended', () => {
      executeReveal(false);
    });

    // Attempt video playback safely without destroying preloader on benign AbortErrors
    const playPromise = video.play();
    if (playPromise !== undefined) {
      playPromise.catch((err) => {
        console.warn('[Intro] Video play caught:', err.name, err.message);
        // Do NOT instantly purge; let HTML5 autoplay or low power timer handle it gracefully
      });
    }
  }

  // Execute as early as DOM is interactive
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIntro);
  } else {
    initIntro();
  }
})();
