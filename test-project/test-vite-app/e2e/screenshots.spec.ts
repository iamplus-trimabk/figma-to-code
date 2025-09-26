import { test, expect } from '@playwright/test'

test.describe('UI Screenshots and Visual Testing', () => {
  test('capture screenshots of the application', async ({ page }) => {
    await page.goto('/')

    // Full page screenshot
    await page.screenshot({ path: 'full-page.png', fullPage: true })

    // Screenshot of the main content area
    const card = page.locator('.card')
    await card.screenshot({ path: 'card-component.png' })

    // Screenshot of the button in different states
    const button = page.locator('button')
    await button.screenshot({ path: 'button-initial.png' })

    // Click button and take screenshot of updated state
    await button.click()
    await button.screenshot({ path: 'button-after-click.png' })

    // Mobile viewport screenshot
    await page.setViewportSize({ width: 375, height: 667 })
    await page.screenshot({ path: 'mobile-view.png', fullPage: true })
  })

  test('verify CSS custom properties are working', async ({ page }) => {
    await page.goto('/')

    // Check if CSS custom properties are applied to the root
    const rootStyles = await page.evaluate(() => {
      const root = document.documentElement
      const computedStyle = getComputedStyle(root)
      return {
        background: computedStyle.getPropertyValue('--background'),
        foreground: computedStyle.getPropertyValue('--foreground'),
        primary: computedStyle.getPropertyValue('--primary'),
        radius: computedStyle.getPropertyValue('--radius')
      }
    })

    expect(rootStyles.background).toBeTruthy()
    expect(rootStyles.foreground).toBeTruthy()
    expect(rootStyles.primary).toBeTruthy()
    expect(rootStyles.radius).toBeTruthy()
  })

  test('verify Tailwind CSS classes are applied', async ({ page }) => {
    await page.goto('/')

    // Check specific Tailwind classes on the button
    const buttonClasses = await page.locator('button').getAttribute('class') || ''

    // Verify some Tailwind utility classes are present
    expect(buttonClasses).toMatch(/inline-flex/)
    expect(buttonClasses).toMatch(/items-center/)
    expect(buttonClasses).toMatch(/justify-center/)
    expect(buttonClasses).toMatch(/rounded-md/)
    expect(buttonClasses).toMatch(/text-sm/)
    expect(buttonClasses).toMatch(/font-medium/)
  })

  test('verify Button component variants work', async ({ page }) => {
    await page.goto('/')

    // The current button uses default variant
    const button = page.locator('button')
    const buttonClasses = await button.getAttribute('class') || ''

    // Should have primary variant classes
    expect(buttonClasses).toMatch(/bg-primary/)
    expect(buttonClasses).toMatch(/text-primary-foreground/)
  })
})