describe("Goldilocks App smoke tests", () => {
  it("loads the home page and shows key UI", () => {
    cy.visit("/");
    cy.contains("Goldilocks").should("be.visible");
    cy.contains("Features & Capabilities").should("be.visible");
    // Check auth links are visible when not logged in
    cy.get("[data-auth-links]").should("be.visible");
    cy.contains("Login").should("be.visible");
    cy.contains("Register").should("be.visible");
  });

  it("health endpoint returns ok and sets headers", () => {
    cy.request("/health").then((resp) => {
      expect(resp.status).to.eq(200);
      expect(resp.body).to.have.property("status", "ok");
      expect(resp.headers).to.have.property("x-request-id");
      expect(resp.headers).to.have.property("x-response-time-ms");
    });
  });

  it("version endpoint returns expected keys", () => {
    cy.request("/version").then((resp) => {
      expect(resp.status).to.eq(200);
      expect(resp.body).to.have.all.keys("app", "python", "flask", "platform");
    });
  });
});

describe("Authentication Flow", () => {
  beforeEach(() => {
    // Clear any existing sessions
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it("shows login and register links on homepage", () => {
    cy.visit("/");
    cy.get("[data-auth-links]").should("be.visible");
    cy.contains("a", "Login")
      .should("be.visible")
      .and("have.attr", "href", "/login");
    cy.contains("a", "Register")
      .should("be.visible")
      .and("have.attr", "href", "/register");
  });

  it("can access login page", () => {
    cy.visit("/login");
    cy.contains("h1", "Login to Goldilocks").should("be.visible");
    cy.get('input[name="email"]').should("be.visible");
    cy.get('input[name="password"]').should("be.visible");
    cy.get('input[name="remember_me"]').should("be.visible");
    cy.get('button[type="submit"]').should("contain", "Login");
  });

  it("can access register page", () => {
    cy.visit("/register");
    cy.contains("h1", "Create Account").should("be.visible");
    cy.get('input[name="full_name"]').should("be.visible");
    cy.get('input[name="username"]').should("be.visible");
    cy.get('input[name="email"]').should("be.visible");
    cy.get('input[name="password"]').should("be.visible");
    cy.get('input[name="confirm_password"]').should("be.visible");
    cy.get('input[name="terms_accepted"]').should("be.visible");
    cy.get('button[type="submit"]').should("contain", "Create Account");
  });

  it("shows validation errors for empty login form", () => {
    cy.visit("/login");
    cy.get('button[type="submit"]').click();
    cy.get(".form-error").should("exist");
  });

  it("shows validation errors for empty register form", () => {
    cy.visit("/register");
    cy.get('button[type="submit"]').click();
    cy.get(".form-error").should("exist");
  });

  it("can register a new user and login", () => {
    const testUser = {
      fullName: "Test User",
      username: `testuser_${Date.now()}`,
      email: `test_${Date.now()}@example.com`,
      password: "TestPass123!",
    };

    // Register new user
    cy.visit("/register");
    cy.get('input[name="full_name"]').type(testUser.fullName);
    cy.get('input[name="username"]').type(testUser.username);
    cy.get('input[name="email"]').type(testUser.email);
    cy.get('input[name="password"]').type(testUser.password);
    cy.get('input[name="confirm_password"]').type(testUser.password);
    cy.get('input[name="terms_accepted"]').check();
    cy.get('button[type="submit"]').click();

    // Should redirect to dashboard after successful registration
    cy.url().should("include", "/dashboard");
    cy.contains("Welcome back").should("be.visible");
    cy.contains(testUser.fullName).should("be.visible");

    // Logout
    cy.contains("a", "Logout").click();
    cy.url().should("eq", Cypress.config().baseUrl + "/");

    // Login with the same credentials
    cy.visit("/login");
    cy.get('input[name="email"]').type(testUser.email);
    cy.get('input[name="password"]').type(testUser.password);
    cy.get('button[type="submit"]').click();

    // Should redirect to dashboard after successful login
    cy.url().should("include", "/dashboard");
    cy.contains("Welcome back").should("be.visible");
  });

  it("can access and update profile", () => {
    // First register and login a user
    const testUser = {
      fullName: "Profile Test User",
      username: `profileuser_${Date.now()}`,
      email: `profile_${Date.now()}@example.com`,
      password: "TestPass123!",
    };

    cy.visit("/register");
    cy.get('input[name="full_name"]').type(testUser.fullName);
    cy.get('input[name="username"]').type(testUser.username);
    cy.get('input[name="email"]').type(testUser.email);
    cy.get('input[name="password"]').type(testUser.password);
    cy.get('input[name="confirm_password"]').type(testUser.password);
    cy.get('input[name="terms_accepted"]').check();
    cy.get('button[type="submit"]').click();

    // Access profile page
    cy.contains("a", "Profile").click();
    cy.url().should("include", "/profile");
    cy.contains("h1", "Edit Profile").should("be.visible");

    // Update profile information
    cy.get('textarea[name="bio"]').type("This is my test bio");
    cy.get('input[name="location"]').type("Test City");
    cy.get('input[name="company"]').type("Test Company");
    cy.get('input[name="job_title"]').type("Test Developer");
    cy.get('button[type="submit"]').click();

    // Should show success message
    cy.contains("Profile updated successfully").should("be.visible");
  });

  it("redirects unauthenticated users to login", () => {
    cy.visit("/dashboard");
    cy.url().should("include", "/login");
    cy.contains("Please log in to access this page").should("be.visible");

    cy.visit("/profile");
    cy.url().should("include", "/login");
  });

  it("can login with admin user", () => {
    // Try to login with the default admin user
    cy.visit("/login");
    cy.get('input[name="email"]').type("admin@goldilocks.local");
    cy.get('input[name="password"]').type("admin123!");
    cy.get('button[type="submit"]').click();

    // Should redirect to dashboard
    cy.url().should("include", "/dashboard");
    cy.contains("Welcome back").should("be.visible");
    cy.contains("Administrator").should("be.visible");
  });
});

describe("Dashboard Functionality", () => {
  beforeEach(() => {
    // Login as admin for dashboard tests
    cy.visit("/login");
    cy.get('input[name="email"]').type("admin@goldilocks.local");
    cy.get('input[name="password"]').type("admin123!");
    cy.get('button[type="submit"]').click();
    cy.url().should("include", "/dashboard");
  });

  it("shows dashboard with user stats", () => {
    cy.contains("Welcome back").should("be.visible");
    cy.contains("Your Account").should("be.visible");
    cy.contains("System Statistics").should("be.visible");
    cy.contains("Quick Actions").should("be.visible");

    // Check stats are displayed
    cy.contains("Total Users").should("be.visible");
    cy.contains("Active Users").should("be.visible");
    cy.contains("Recent Logins").should("be.visible");
    cy.contains("Administrators").should("be.visible");
  });

  it("has working navigation links", () => {
    cy.contains("a", "Profile")
      .should("be.visible")
      .and("have.attr", "href", "/profile");
    cy.contains("a", "Logout")
      .should("be.visible")
      .and("have.attr", "href", "/logout");
  });

  it("has working quick action links", () => {
    cy.contains("a", "Update Profile").should("have.attr", "href", "/profile");
    cy.contains("a", "Check System Health").should(
      "have.attr",
      "href",
      "/health"
    );
    cy.contains("a", "View System Info").should(
      "have.attr",
      "href",
      "/version"
    );
    cy.contains("a", "Back to Home").should("have.attr", "href", "/");
  });
});
