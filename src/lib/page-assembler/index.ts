/**
 * Page Assembler Module
 *
 * Complete page assembly system for Stage 4: Page Assembler
 *
 * This module provides:
 * - Layout parsing from Figma screen layouts
 * - Component registry mapping Figma names to React components
 * - Page assembly engine that renders complete screens
 * - Responsive layout utilities
 */

export { LayoutParser } from './layout-parser'
export { ComponentRegistryManager, componentRegistryManager } from './component-registry'
export { PageAssembler, PageAssemblerComponent, pageAssembler } from './page-assembler'
export * from './types'

// Re-export for convenience
export { layoutParser } from './layout-parser'
export { componentRegistry } from './component-registry'