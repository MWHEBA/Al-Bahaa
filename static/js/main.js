window.bgroup = window.bgroup || {};

document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".site-header__menu-toggle");
  const nav = document.querySelector("#primary-navigation");

  if (!header || !toggle || !nav) {
    return;
  }

  const setOpen = (isOpen) => {
    header.classList.toggle("is-menu-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  };

  toggle.addEventListener("click", () => {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  const backdrop = header.querySelector(".site-header__backdrop");
  if (backdrop) {
    backdrop.addEventListener("click", () => {
      setOpen(false);
    });
  }

  document.addEventListener("click", (event) => {
    if (header.classList.contains("is-menu-open")) {
      if (!header.contains(event.target)) {
        setOpen(false);
      }
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1100 && header.classList.contains("is-menu-open")) {
      setOpen(false);
    }
  });

  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setOpen(false);
      toggle.focus();
    }
  });
});
