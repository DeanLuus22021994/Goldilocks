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
      (window.crypto && crypto.randomUUID && crypto.randomUUID()) ||
      String(Date.now());
    fetch("/health", { headers: { "X-Request-ID": cid } })
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject(r.status);
      })
      .then(function (j) {
        badge.textContent = (j && j.status) || "unknown";
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
    if (btn) {
      var lab = btn.querySelector("[data-theme-label]");
      if (lab) lab.textContent = theme;
    }
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

  // Sidebar toggle
  var sidebar = document.querySelector("[data-sidebar]");
  var navToggle = document.querySelector("[data-nav-toggle]");
  if (sidebar && navToggle) {
    navToggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
  }

  // Profile dropdown (simple simulated auth via localStorage)
  var profileWrap = document.querySelector("[data-profile]");
  var profileMenu = document.querySelector("[data-profile-menu]");
  var profileBtn = document.querySelector("[data-profile-toggle]");
  var profileNameEls = document.querySelectorAll("[data-profile-name]");
  var AUTH_FLAG = "goldilocks-auth";

  function setProfileVisible(visible) {
    if (!profileWrap) return;
    if (visible) {
      profileWrap.removeAttribute("hidden");
    } else {
      profileWrap.setAttribute("hidden", "");
    }
  }

  function closeProfile() {
    if (!profileMenu || !profileBtn) return;
    profileMenu.classList.remove("open");
    profileBtn.setAttribute("aria-expanded", "false");
    document.removeEventListener("click", onDocClick, true);
    document.removeEventListener("keydown", onKeyDown, true);
  }

  function openProfile() {
    if (!profileMenu || !profileBtn) return;
    profileMenu.classList.add("open");
    profileBtn.setAttribute("aria-expanded", "true");
    setTimeout(function () {
      document.addEventListener("click", onDocClick, true);
      document.addEventListener("keydown", onKeyDown, true);
    });
  }

  function onDocClick(ev) {
    if (!profileWrap) return;
    if (!profileWrap.contains(ev.target)) closeProfile();
  }
  function onKeyDown(ev) {
    if (ev.key === "Escape") closeProfile();
  }

  try {
    var authData = JSON.parse(localStorage.getItem(AUTH_FLAG) || "null");
    if (authData && authData.loggedIn) {
      setProfileVisible(true);
      var name = authData.name || "User";
      profileNameEls.forEach(function (el) {
        el.textContent = name;
      });
    } else {
      setProfileVisible(false);
    }
  } catch (_) {
    setProfileVisible(false);
  }

  if (profileBtn && profileMenu) {
    profileBtn.addEventListener("click", function () {
      if (profileMenu.classList.contains("open")) closeProfile();
      else openProfile();
    });
    var signout = profileMenu.querySelector("[data-signout]");
    if (signout) {
      signout.addEventListener("click", function (e) {
        e.preventDefault();
        try {
          localStorage.removeItem(AUTH_FLAG);
        } catch (_) {}
        setProfileVisible(false);
        closeProfile();
      });
    }
  }
})();
