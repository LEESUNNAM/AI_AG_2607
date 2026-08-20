/* Helinox static site — minimal vanilla JS
   Scope: mobile nav toggle, About accordion, desktop dropdown click-toggle
   (for touch), tap-to-reveal collaboration cards, scroll-reveal animation.
   No frameworks/build tools — per proposal Section 2 constraints. */
(function () {
  "use strict";

  /* ---- Mobile nav toggle ---- */
  var navToggle = document.querySelector(".nav-toggle");
  var mobilePanel = document.querySelector(".mobile-panel");
  if (navToggle && mobilePanel) {
    navToggle.addEventListener("click", function () {
      var isOpen = mobilePanel.classList.toggle("is-open");
      navToggle.classList.toggle("is-active", isOpen);
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
  }

  /* ---- Mobile "About" accordion ---- */
  document.querySelectorAll(".mp-accordion-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var isOpen = btn.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
      if (panel) panel.classList.toggle("is-open", isOpen);
    });
  });

  /* ---- Desktop dropdown: allow click/tap toggle in addition to hover ---- */
  document.querySelectorAll(".has-dropdown > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      var parent = btn.parentElement;
      var isOpen = parent.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    document.querySelectorAll(".has-dropdown.is-open").forEach(function (el) {
      if (!el.contains(e.target)) {
        el.classList.remove("is-open");
        var b = el.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      }
    });
  });

  /* ---- Tap-to-reveal collaboration detail cards (mobile) ---- */
  document.querySelectorAll(".collab-tile").forEach(function (tile) {
    tile.addEventListener("click", function () {
      tile.classList.toggle("is-open");
    });
  });

  /* ---- Scroll-reveal (purposeful, restrained motion per Section 5.3) ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }
})();
