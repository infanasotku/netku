import { test, expect } from "@playwright/test";

test("has logo", async ({ page }) => {
  await page.goto("/");

  const sidebar = page.locator(".sidebar");
  await expect(sidebar).toBeVisible();

  const logo = sidebar.locator(".logo");
  await expect(logo).toBeVisible();

  const logoIcon = logo.locator(".icon");
  await expect(logoIcon).toBeVisible();

  const title = logo.locator(".title");
  await expect(title).toBeVisible();
  await expect(title).toHaveText("Netku");
});
