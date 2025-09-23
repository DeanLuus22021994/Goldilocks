/* eslint-env node */
/** @type {import('cypress').DefinedConfig} */
module.exports = {
  e2e: {
    baseUrl: "http://localhost:9000",
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 8000,
  },
};
