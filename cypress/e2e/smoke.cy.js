describe("Goldilocks App smoke tests", () => {
  it("loads the home page and shows key UI", () => {
    cy.visit("/");
    cy.contains("Goldilocks").should("be.visible");
    cy.contains("Features & Capabilities").should("be.visible");
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
