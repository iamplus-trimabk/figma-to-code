/**
 * Page Assembler Types
 *
 * Type definitions for the page layout engine
 */

export interface ComponentPosition {
  x: number
  y: number
}

export interface ComponentSize {
  width: number
  height: number
}

export interface LayoutConstraints {
  vertical: 'TOP' | 'CENTER' | 'BOTTOM' | 'SCALE'
  horizontal: 'LEFT' | 'CENTER' | 'RIGHT' | 'SCALE'
}

export interface ScreenLayout {
  name: string
  type: string
  size: ComponentSize
  position?: ComponentPosition
  children: ScreenComponent[]
  layout: {
    type: string
    direction?: string
    spacing?: number
  }
  backgroundColor?: string
}

export interface ScreenComponent {
  name: string
  type: string
  index: number
  size: ComponentSize
  position: ComponentPosition
  visible: boolean
  componentRef?: string | null
  style?: Record<string, any>
  constraints?: LayoutConstraints
  children?: ScreenComponent[]
}

export interface ComponentRegistry {
  [componentName: string]: React.ComponentType<any>
}

export interface PageAssemblerConfig {
  screenLayoutsPath: string
  componentRegistry: ComponentRegistry
  responsiveBreakpoints?: {
    mobile: number
    tablet: number
    desktop: number
  }
}

export interface ResponsiveLayout {
  mobile: React.ReactNode
  tablet: React.ReactNode
  desktop: React.ReactNode
}

export interface LayoutStyle {
  position: 'absolute' | 'relative' | 'fixed' | 'static'
  left?: string
  top?: string
  width?: string
  height?: string
  backgroundColor?: string
  borderRadius?: string
  opacity?: number
  zIndex?: number
}