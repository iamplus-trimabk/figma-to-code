import { test, expect } from '@playwright/test'

test.describe('Vite React App UI Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('homepage has correct title and structure', async ({ page }) => {
    await expect(page).toHaveTitle(/Vite \+ React/)
    await expect(page.locator('h1')).toHaveText('Vite + React')
  })

  test('Vite and React logos are visible and have hover effects', async ({ page }) => {
    const viteLogo = page.locator('a[href="https://vitejs.dev"] img')
    const reactLogo = page.locator('a[href="https://react.dev"] img')

    await expect(viteLogo).toBeVisible()
    await expect(reactLogo).toBeVisible()

    // Check that logos have the correct CSS classes
    await expect(viteLogo).toHaveClass(/logo/)
    await expect(reactLogo).toHaveClass(/logo react/)
  })

  test('counter button works correctly with custom Button component', async ({ page }) => {
    const counterButton = page.locator('button')

    // Initial state
    await expect(counterButton).toHaveText('count is 0')

    // Click and verify increment
    await counterButton.click()
    await expect(counterButton).toHaveText('count is 1')

    // Click multiple times
    await counterButton.click()
    await counterButton.click()
    await expect(counterButton).toHaveText('count is 3')
  })

  test('Button component has proper styling classes', async ({ page }) => {
    const button = page.locator('button')

    // Check if button has Tailwind classes (using regex to match any of the button classes)
    await expect(button).toHaveClass(/inline-flex|items-center|justify-center|whitespace-nowrap|rounded-md|text-sm|font-medium|transition-colors/)
  })

  test('page has proper layout and styling', async ({ page }) => {
    // Check root container
    const root = page.locator('#root')
    await expect(root).toBeVisible()

    // Check card element
    const card = page.locator('.card')
    await expect(card).toBeVisible()

    // Check documentation text
    const docsText = page.locator('.read-the-docs')
    await expect(docsText).toBeVisible()
    await expect(docsText).toHaveText('Click on the Vite and React logos to learn more')
  })

  test('code element is properly displayed', async ({ page }) => {
    const codeElement = page.locator('code')
    await expect(codeElement).toBeVisible()
    await expect(codeElement).toHaveText('src/App.tsx')
  })

  test('responsive design - check mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })

    // Check that all elements are still visible and properly laid out
    await expect(page.locator('h1')).toBeVisible()
    await expect(page.locator('button')).toBeVisible()
    await expect(page.locator('.card')).toBeVisible()
  })

  test('check for console errors', async ({ page }) => {
    const consoleErrors: string[] = []

    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text())
      }
    })

    page.on('pageerror', error => {
      consoleErrors.push(error.message)
    })

    await page.reload()

    // Wait a bit for any potential errors
    await page.waitForTimeout(1000)

    expect(consoleErrors).toHaveLength(0)
  })

  test('links open in new tabs with correct attributes', async ({ page }) => {
    const viteLink = page.locator('a[href="https://vitejs.dev"]')
    const reactLink = page.locator('a[href="https://react.dev"]')

    await expect(viteLink).toHaveAttribute('target', '_blank')
    await expect(viteLink).toHaveAttribute('rel', 'noreferrer')
    await expect(reactLink).toHaveAttribute('target', '_blank')
    await expect(reactLink).toHaveAttribute('rel', 'noreferrer')
  })
})