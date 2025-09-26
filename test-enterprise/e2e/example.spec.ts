import { test, expect } from '@playwright/test'

test('homepage has correct title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/Vite [+][+] React/)
})

test('counter works correctly', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('button')).toHaveText('count is 0')
  await page.locator('button').click()
  await expect(page.locator('button')).toHaveText('count is 1')
})