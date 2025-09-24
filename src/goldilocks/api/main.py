"""Main application routes blueprint."""

from flask import Blueprint

# Create main Blueprint
main_bp = Blueprint("main", __name__)

# HTML Template for main page
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="description"
      content="Goldilocks - Modern Flask Application with Advanced Development Environment"
    />
    <meta
      name="keywords"
      content="Flask, Python, Development, API, Modern Web App"
    />
    <meta name="author" content="Goldilocks Development Team" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="/" />
    <meta property="og:title" content="Goldilocks Flask App" />
    <meta
      property="og:description"
      content="Modern Flask Application with Advanced Development Environment"
    />

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image" />
    <meta property="twitter:url" content="/" />
    <meta property="twitter:title" content="Goldilocks Flask App" />
    <meta
      property="twitter:description"
      content="Modern Flask Application with Advanced Development Environment"
    />

    <title>Goldilocks Flask App</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg" />

    <!-- Preload critical resources for performance -->
    <link rel="preload" href="/static/css/variables.css" as="style" />
    <link rel="preload" href="/static/css/theme.css" as="style" />
    <link rel="preload" href="/static/css/base.css" as="style" />
    <link rel="preload" href="/static/css/layout.css" as="style" />
    <link rel="preload" href="/static/css/components.css" as="style" />
    <link rel="preload" href="/static/css/header.css" as="style" />
    <link rel="preload" href="/static/css/buttons.css" as="style" />
    <link rel="preload" href="/static/css/utilities.css" as="style" />
    <link rel="preload" href="/static/css/nav.css" as="style" />
    <link rel="preload" href="/static/css/footer.css" as="style" />

    <!-- Load stylesheets -->
    <link rel="stylesheet" href="/static/css/variables.css" />
    <link rel="stylesheet" href="/static/css/theme.css" />
    <link rel="stylesheet" href="/static/css/base.css" />
    <link rel="stylesheet" href="/static/css/layout.css" />
    <link rel="stylesheet" href="/static/css/components.css" />
    <link rel="stylesheet" href="/static/css/header.css" />
    <link rel="stylesheet" href="/static/css/buttons.css" />
    <link rel="stylesheet" href="/static/css/utilities.css" />
    <link rel="stylesheet" href="/static/css/nav.css" />
    <link rel="stylesheet" href="/static/css/footer.css" />
  </head>
  <body>
    <!-- Top header bar -->
    <header class="topbar">
      <div class="topbar-inner">
        <div class="left">
          <button class="icon-btn" data-nav-toggle aria-label="Toggle menu">
            <span aria-hidden="true">☰</span>
          </button>
          <strong class="brand">Goldilocks</strong>
          <span class="small hide-sm"
            >Health: <span class="badge" data-health>—</span></span
          >
        </div>
        <div class="right">
          <button
            class="icon-btn"
            data-toggle-theme
            aria-pressed="false"
            aria-label="Toggle color theme"
          >
            <span aria-hidden="true">🌓</span>
            <span class="hide-sm" data-theme-label>light</span>
          </button>

          {% if current_user.is_authenticated %}
            <!-- Profile (shown when logged in) -->
            <div class="profile" data-profile>
              <button
                class="icon-btn"
                data-profile-toggle
                aria-haspopup="menu"
                aria-expanded="false"
              >
                <img
                  class="avatar"
                  src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='8' r='5' fill='%23999'/%3E%3Crect x='4' y='15' width='16' height='7' rx='3' fill='%23999'/%3E%3C/svg%3E"
                  alt=""
                  width="24"
                  height="24"
                />
                <span class="hide-sm" data-profile-name>{{ current_user.full_name or current_user.username }}</span>
              </button>
              <div class="profile-menu" data-profile-menu role="menu">
                <div class="small muted profile-menu-header">
                  Signed in as <strong data-profile-name>{{ current_user.full_name or current_user.username }}</strong>
                </div>
                <hr />
                <a href="{{ url_for('auth.profile') }}" role="menuitem">Profile</a>
                <a href="{{ url_for('auth.dashboard') }}" role="menuitem">Dashboard</a>
                <hr />
                <a href="{{ url_for('auth.logout') }}" role="menuitem" data-signout>Sign out</a>
              </div>
            </div>
          {% else %}
            <!-- Auth links (shown when not logged in) -->
            <div class="auth-links" data-auth-links>
              <a href="{{ url_for('auth.login') }}" class="btn btn-sm btn-secondary">Login</a>
              <a href="{{ url_for('auth.register') }}" class="btn btn-sm btn-primary">Register</a>
            </div>
          {% endif %}
        </div>
      </div>
    </header>

    <div class="portal" data-portal>
      <!-- Sidebar navigation like Azure portal -->
      <aside class="sidebar" data-sidebar>
        <nav class="nav" aria-label="Main">
          <a class="nav-item" href="/">
            <span class="icon" aria-hidden="true">🏠</span>
            <span>Home</span>
          </a>
          <a class="nav-item" href="/health">
            <span class="icon" aria-hidden="true">❤️</span>
            <span>Health</span>
          </a>
          <a class="nav-item" href="/version">
            <span class="icon" aria-hidden="true">🧪</span>
            <span>Version</span>
          </a>
          {% if current_user.is_authenticated %}
            <a class="nav-item" href="{{ url_for('auth.dashboard') }}">
              <span class="icon" aria-hidden="true">📊</span>
              <span>Dashboard</span>
            </a>
            <a class="nav-item" href="{{ url_for('auth.profile') }}">
              <span class="icon" aria-hidden="true">👤</span>
              <span>Profile</span>
            </a>
          {% endif %}
        </nav>
      </aside>

      <!-- Main content -->
      <main class="content">
        <!-- Hero Section -->
        <section class="hero">
          <div class="container">
            <div class="hero-content">
              <h1 class="hero-title">
                <span class="gradient-text">Goldilocks</span>
                <span class="hero-subtitle">Flask Application</span>
              </h1>
              <p class="hero-description">
                A modern, containerized Flask application with advanced
                development environment, comprehensive testing, and
                production-ready infrastructure.
              </p>
              <div class="hero-actions">
                <a href="/health" class="btn btn-primary">
                  <span class="btn-icon">❤️</span>
                  Check Health
                </a>
                <a href="/version" class="btn btn-secondary">
                  <span class="btn-icon">🔍</span>
                  View Version
                </a>
              </div>
            </div>
            <div class="hero-visual">
              <div class="status-indicator">
                <div class="status-dot" data-health-indicator></div>
                <span class="status-text" data-health-text>Checking...</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Features Section -->
        <section class="features section">
          <div class="container">
            <h2 class="section-title">Features & Capabilities</h2>
            <div class="features-grid">
              <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>High Performance</h3>
                <p>
                  Optimized Flask application with structured logging,
                  correlation IDs, and efficient resource management.
                </p>
                <a href="/health" class="feature-link">Check Health →</a>
              </div>

              <div class="feature-card">
                <div class="feature-icon">🛠️</div>
                <h3>Developer Experience</h3>
                <p>
                  Advanced development container with pre-configured tools,
                  linting, testing, and debugging capabilities.
                </p>
                <a href="#" class="feature-link">Learn More →</a>
              </div>

              <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Monitoring & Observability</h3>
                <p>
                  Built-in health checks, version tracking, and comprehensive
                  logging for production readiness.
                </p>
                <a href="/version" class="feature-link">View Version →</a>
              </div>

              <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Security & Compliance</h3>
                <p>
                  Security-first design with input validation, dependency
                  scanning, and best practice implementations.
                </p>
                <a href="#" class="feature-link">Security →</a>
              </div>

              <div class="feature-card">
                <div class="feature-icon">🐳</div>
                <h3>Container Ready</h3>
                <p>
                  Docker-optimized with multi-stage builds, caching layers, and
                  production deployment configurations.
                </p>
                <a href="#" class="feature-link">Deploy →</a>
              </div>

              <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Modern Stack</h3>
                <p>
                  Latest Python 3.12, Flask 3.x, with cutting-edge development
                  tools and CI/CD pipelines.
                </p>
                <a href="#" class="feature-link">Tech Stack →</a>
              </div>
            </div>
          </div>
        </section>

        <!-- API Endpoints Section -->
        <section class="api-section section">
          <div class="container">
            <h2 class="section-title">API Endpoints</h2>
            <div class="api-grid">
              <div class="api-card">
                <div class="api-method get">GET</div>
                <div class="api-details">
                  <h3 class="api-endpoint">/health</h3>
                  <p class="api-description">
                    Health check endpoint for monitoring service availability
                  </p>
                  <div class="api-response">
                    <span class="response-label">Response:</span>
                    <code class="response-code">{"status": "ok"}</code>
                  </div>
                  <a href="/health" class="api-test-btn">Test Endpoint</a>
                </div>
              </div>

              <div class="api-card">
                <div class="api-method get">GET</div>
                <div class="api-details">
                  <h3 class="api-endpoint">/version</h3>
                  <p class="api-description">
                    Application version and runtime information
                  </p>
                  <div class="api-response">
                    <span class="response-label">Response:</span>
                    <code class="response-code"
                      >{"app": "...", "python": "...", "flask": "..."}</code
                    >
                  </div>
                  <a href="/version" class="api-test-btn">Test Endpoint</a>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Stats Section -->
        <section class="stats section">
          <div class="container">
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value" data-stat="uptime">--</div>
                <div class="stat-label">Uptime</div>
              </div>
              <div class="stat-item">
                <div class="stat-value" data-stat="requests">0</div>
                <div class="stat-label">Requests</div>
              </div>
              <div class="stat-item">
                <div class="stat-value" data-stat="version">--</div>
                <div class="stat-label">Version</div>
              </div>
              <div class="stat-item">
                <div class="stat-value" data-stat="python">--</div>
                <div class="stat-label">Python</div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <footer class="site-footer">
      <div class="container">
        <div class="flex items-center justify-between wrap gap-3">
          <span class="muted">© <span data-year></span> Goldilocks</span>
          <span class="small">
            <a href="/version">Version</a> ·
            <a
              href="https://flask.palletsprojects.com/"
              rel="noreferrer noopener"
              >Flask</a
            >
          </span>
        </div>
      </div>
    </footer>

    <script src="/static/js/main.js" defer></script>
  </body>
</html>
"""


@main_bp.get("/")
def index():
    """Main application index page."""
    from flask import render_template_string
    return render_template_string(INDEX_TEMPLATE)
