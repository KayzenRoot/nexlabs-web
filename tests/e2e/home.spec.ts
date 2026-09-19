import { expect, test } from "@playwright/test";

test.use({ javaScriptEnabled: false });

test("home page exposes semantic content and keyboard entry point", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main")).toContainText("Build with AI");
  await page.keyboard.press("Tab");
  await expect(page.locator("a.skip-link")).toBeFocused();
  await expect(page.locator("nav[aria-label='Primary navigation']")).toBeVisible();
});

test("unknown paths return the basic 404 shell", async ({ page }) => {
  const response = await page.goto("/not-a-real-route/");
  expect(response?.status()).toBe(404);
  await expect(page.locator("main")).toContainText("not part of the current system");
});
