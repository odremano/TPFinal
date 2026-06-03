// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 10000,
  reporter: [
    ['list'],
    ['json', { outputFile: 'playwright-results/results.json' }],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
});