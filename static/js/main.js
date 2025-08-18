// Minimal progressive enhancement utilities
(function () {
  // Year badge
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Health badge
  var badge = document.querySelector("[data-health]");
  if (badge && window.fetch) {
    var cid =
      crypto && crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
    fetch("/health", { headers: { "X-Request-ID": cid } })
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject(r.status);
      })
      .then(function (j) {
        badge.textContent = j.status || "unknown";
      })
      .catch(function () {
        badge.textContent = "unknown";
      });
  }

  // Theme toggle with persistence
  var root = document.documentElement;
  var storageKey = "goldilocks-theme";
  var btn = document.querySelector("[data-toggle-theme]");

  function getSystemTheme() {
    return window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    if (theme) root.setAttribute("data-theme", theme);
    if (btn)
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    if (btn) btn.querySelector("[data-theme-label]").textContent = theme;
  }

  var saved = null;
  try {
    saved = localStorage.getItem(storageKey);
  } catch (_) {}
  var initial = saved || getSystemTheme();
  applyTheme(initial);

  if (btn) {
    btn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") || getSystemTheme();
      var next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem(storageKey, next);
      } catch (_) {}
    });
  }
})();
