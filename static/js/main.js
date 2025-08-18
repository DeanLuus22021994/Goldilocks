// Minimal progressive enhancement utilities
(function () {
  // Add current year to any element with data-year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Ping /health quickly and update a badge if present
  var badge = document.querySelector("[data-health]");
  if (badge) {
    fetch("/health", { headers: { "X-Request-ID": crypto.randomUUID() } })
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
})();
