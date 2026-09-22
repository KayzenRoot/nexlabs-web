import { expect, test } from "@playwright/test";

test.describe("static content", () => {
  test.use({ javaScriptEnabled: false });

  test("home page exposes semantic content and keyboard entry point", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("main")).toContainText("Infrastructure for AI-native software");
    await expect(page.locator(".context-core-static")).toBeVisible();
    await page.keyboard.press("Tab");
    await expect(page.locator("a.skip-link")).toBeFocused();
    await expect(page.locator("nav[aria-label='Primary navigation']")).toBeVisible();
  });

  test("all institutional routes expose a heading", async ({ page }) => {
    for (const route of ["/hive/", "/technology/", "/open-source/", "/about/", "/contact/", "/privacy/"]) {
      const response = await page.goto(route);
      expect(response?.status(), route).toBe(200);
      await expect(page.locator("main h1"), route).toBeVisible();
    }
  });

  test("unknown paths return the 404 shell", async ({ page }) => {
    const response = await page.goto("/not-a-real-route/");
    expect(response?.status()).toBe(404);
    await expect(page.locator("main")).toContainText("not part of the current NexLabs system");
  });
});

test("mobile menu and theme preference remain usable", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const menu = page.getByRole("button", { name: "Menu" });
  await menu.click();
  await expect(page.getByRole("navigation", { name: "Mobile primary navigation" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(menu).toBeFocused();
  await page.getByRole("combobox", { name: "Color theme" }).selectOption("dark");
  await expect.poll(() => page.evaluate(() => localStorage.getItem("nexlabs-theme"))).toBe("dark");
});

test.describe("CP-07 static-first runtime boundary", () => {
  test("keeps the static Context Core fallback and hero actions functional", async ({ page }) => {
    const modelRequests: string[] = [];
    page.on("request", (request) => {
      if (request.url().includes("/models/context-core/")) modelRequests.push(request.url());
    });
    await page.goto("/");
    await expect(page.locator(".context-core-boundary")).toBeVisible();
    await expect(page.locator(".context-core-static")).toBeVisible();
    await expect(page.locator("main")).toContainText("Infrastructure for AI-native software");
    await expect(page.getByRole("link", { name: "Explore HIVE", exact: true })).toBeVisible();
    expect(modelRequests.length).toBeLessThanOrEqual(1);
  });

  test("does not load the hero model on non-home routes", async ({ page }) => {
    const modelRequests: string[] = [];
    page.on("request", (request) => {
      if (request.url().includes("/models/context-core/")) modelRequests.push(request.url());
    });
    await page.goto("/technology/");
    await expect(page.locator("main h1")).toBeVisible();
    await page.waitForTimeout(250);
    expect(modelRequests).toHaveLength(0);
  });

  test("reduced motion remains static and responsive framing stays stable", async ({ page }) => {
    const modelRequests: string[] = [];
    page.on("request", (request) => {
      if (request.url().includes("/models/context-core/")) modelRequests.push(request.url());
    });
    await page.emulateMedia({ reducedMotion: "reduce" });
    for (const viewport of [{ width: 1440, height: 900 }, { width: 768, height: 900 }, { width: 390, height: 844 }]) {
      await page.setViewportSize(viewport);
      await page.goto("/");
      const boundary = page.locator(".context-core-boundary");
      await expect(boundary).toBeVisible();
      await expect(boundary.locator(".context-core-static")).toBeVisible();
      const box = await boundary.boundingBox();
      expect(box?.width).toBeGreaterThan(0);
      expect(box?.height).toBeGreaterThan(0);
    }
    expect(modelRequests).toHaveLength(0);
  });
});
