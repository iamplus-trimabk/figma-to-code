/**
 * Page Assembler Types - Generated from Stage 2 Automation Outputs
 */

export interface LayoutStyle {
  width?: string | number
  height?: string | number
  backgroundColor?: string
  backgroundOpacity?: number
  borderRadius?: string | number
  display?: "block" | "inline" | "flex" | "grid" | "none"
  overflow?: "visible" | "hidden" | "scroll" | "auto"
  opacity?: number
  padding?: string | number
  margin?: string | number
  border?: string
  color?: string
  textAlign?: "left" | "center" | "right" | "justify"
  fontSize?: string | number
  fontWeight?: string | number
  textDecoration?: string
  cursor?: string
  zIndex?: string | number
  transition?: string
  gap?: string | number
}

export interface ComponentPosition {
  x?: number
  y?: number
}

export interface ComponentSize {
  width: number
  height: number
}

export interface ComponentStyle {
  background_colors?: string[]
  border_radius?: number
  opacity?: number
}

export interface ComponentConstraints {
  vertical: string
  horizontal: string
}
