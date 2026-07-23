/* =====================================================================
   The Crash Course on Volleyball — home page interactions
   - Scroll-reveal via IntersectionObserver (Apple-style fade/slide-in)
   - Staggered reveals for grouped items (officers, portal cards)
   - Subtle hero parallax
   - "Coming soon" toast for sections not yet built
   ===================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Staggering: number items within each group so CSS can delay them ---- */
  function applyStagger(selector) {
    document.querySelectorAll(selector).forEach(function (group) {
      var kids = group.querySelectorAll(":scope > .reveal");
      kids.forEach(function (el, i) {
        el.style.setProperty("--i", i);
      });
    });
  }
  applyStagger(".roster");
  applyStagger(".portal-grid");
  applyStagger(".skill-row");
  applyStagger(".ref-grid");
  applyStagger(".duo-grid");
  applyStagger(".phil-body");

  /* ---- Scroll reveal ---- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(".reveal"));

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });

    revealEls.forEach(function (el) { io.observe(el); });

    /* Safety: anything already in view on load reveals immediately */
    requestAnimationFrame(function () {
      revealEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 0.9) el.classList.add("in");
      });
    });
  }

  /* ---- Coming-soon toast for not-yet-live portal links ---- */
  var toast = document.getElementById("toast");
  var toastTimer = null;
  function showToast() {
    if (!toast) return;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 2600);
  }
  document.querySelectorAll("a[data-soon]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      showToast();
    });
  });

  /* ---- Info dock (top-right): tap-to-toggle on touch; outside-click / Esc closes.
     Desktop hover is handled purely in CSS; this only adds the tap + a11y wiring. ---- */
  var infoDock = document.querySelector(".info-dock");
  if (infoDock) {
    var infoToggle = infoDock.querySelector(".info-dock__toggle");
    var setInfoOpen = function (open) {
      infoDock.classList.toggle("is-open", open);
      if (infoToggle) infoToggle.setAttribute("aria-expanded", open ? "true" : "false");
    };
    if (infoToggle) {
      infoToggle.addEventListener("click", function (e) {
        e.stopPropagation();
        setInfoOpen(!infoDock.classList.contains("is-open"));
      });
    }
    document.addEventListener("click", function (e) {
      if (!infoDock.contains(e.target)) setInfoOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setInfoOpen(false);
    });
  }
})();
