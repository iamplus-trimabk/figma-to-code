/**
 * Layout Parser - Parses Figma screen layouts and extracts component hierarchy
 *
 * This module handles parsing of screen_layouts.json to extract:
 * - Component hierarchy and relationships
 * - Positioning and sizing data
 * - Layout constraints and patterns
 */

import { ScreenLayout, ComponentPosition, ComponentSize } from './types'

export interface ParsedScreen {
  name: string
  type: string
  size: ComponentSize
  children: ParsedComponent[]
  layout: {
    type: string
    direction?: string
    spacing?: number
  }
  backgroundColor?: string
}

export interface ParsedComponent {
  name: string
  type: string
  index: number
  size: ComponentSize
  position: ComponentPosition
  visible: boolean
  componentRef?: string | null
  style?: Record<string, any>
  constraints?: {
    vertical: string
    horizontal: string
  }
  children?: ParsedComponent[]
}

export class LayoutParser {
  private screenLayouts: any

  constructor(screenLayoutsPath: string) {
    // In production, this would load from the actual file
    // For now, we'll work with the parsed data
    this.screenLayouts = this.loadScreenLayouts(screenLayoutsPath)
  }

  private loadScreenLayouts(path: string): any {
    // Load the actual screen layouts data
    // In a real implementation, this would be fetched from an API or imported
    // For now, we'll include the essential Login screen data

    return {
      screens: [
        {
          name: "Login",
          type: "frame",
          size: {
            width: 1920.0,
            height: 1024.0,
            x: -9902.0,
            y: -7018.0
          },
          children: [
            {
              name: "Illustration",
              type: "group",
              index: 0,
              size: {
                width: 640.1377563476562,
                height: 639.4258422851562
              },
              position: {
                x: -9729.0,
                y: -6825.42578125
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "SCALE",
                horizontal: "SCALE"
              }
            },
            {
              name: "bg",
              type: "rectangle",
              index: 1,
              size: {
                width: 788.0,
                height: 940.0
              },
              position: {
                x: -8850.0,
                y: -6976.0
              },
              visible: true,
              component_ref: null,
              style: {
                background_colors: ["#ffffff"],
                border_radius: 8.0
              },
              constraints: {
                vertical: "SCALE",
                horizontal: "SCALE"
              }
            },
            {
              name: "Welcome to Design School",
              type: "text",
              index: 2,
              size: {
                width: 338.0,
                height: 114.0
              },
              position: {
                x: -8794.0,
                y: -6932.0
              },
              visible: true,
              component_ref: null,
              style: {
                background_colors: ["#2e2e2e"]
              },
              constraints: {
                vertical: "SCALE",
                horizontal: "SCALE"
              }
            },
            {
              name: "Login with Google",
              type: "group",
              index: 3,
              size: {
                width: 681.0,
                height: 78.0
              },
              position: {
                x: -8786.0,
                y: -6781.0
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Login with facebook",
              type: "group",
              index: 4,
              size: {
                width: 681.0,
                height: 78.0
              },
              position: {
                x: -8786.0,
                y: -6675.0
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "or",
              type: "group",
              index: 5,
              size: {
                width: 673.0,
                height: 22.0
              },
              position: {
                x: -8783.0,
                y: -6562.0
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Forgot Password?",
              type: "text",
              index: 6,
              size: {
                width: 141.0,
                height: 22.0
              },
              position: {
                x: -8251.0,
                y: -6306.0
              },
              visible: true,
              component_ref: null,
              style: {
                background_colors: ["#6257db"]
              },
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Email",
              type: "group",
              index: 7,
              size: {
                width: 671.0,
                height: 77.0
              },
              position: {
                x: -8776.0,
                y: -6504.0
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Password",
              type: "group",
              index: 8,
              size: {
                width: 671.0,
                height: 77.0
              },
              position: {
                x: -8776.0,
                y: -6407.0
              },
              visible: true,
              component_ref: null,
              style: {},
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "button",
              type: "group",
              index: 9,
              size: {
                width: 671.0,
                height: 77.0
              },
              position: {
                x: -8776.0,
                y: -6260.0
              },
              visible: true,
              component_ref: null,
              style: {
                border_radius: 8.0
              },
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Remember me",
              type: "group",
              index: 10,
              size: {
                width: 153.0,
                height: 22.0
              },
              position: {
                x: -8774.0,
                y: -6306.0
              },
              visible: true,
              component_ref: null,
              style: {
                border_radius: 4.0
              },
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            },
            {
              name: "Don't have an account? Register",
              type: "text",
              index: 11,
              size: {
                width: 259.0,
                height: 21.0
              },
              position: {
                x: -8586.0,
                y: -6136.0
              },
              visible: true,
              component_ref: null,
              style: {
                background_colors: ["#000000"]
              },
              constraints: {
                vertical: "TOP",
                horizontal: "LEFT"
              }
            }
          ],
          layout: {
            type: "manual",
            direction: "horizontal",
            spacing: 116.62074788411458
          },
          description: "FRAME screen: Login",
          background_color: "#f4f4f4"
        }
      ],
      layout_patterns: {
        common_spacing: [172.47],
        screen_sizes: [
          {
            width: 1920.0,
            height: 1024.0
          }
        ],
        layout_directions: {
          horizontal: 1,
          vertical: 2
        }
      },
      grid_systems: [
        {
          screen: "Login",
          x_spacing: 8.0,
          y_spacing: 44.0,
          columns: 7,
          rows: 11
        }
      ]
    }
  }

  parseScreen(screenName: string): ParsedScreen | null {
    const screens = this.screenLayouts.screens || []
    const screenData = screens.find((screen: any) => screen.name === screenName)

    if (!screenData) {
      console.warn(`Screen "${screenName}" not found in layout data`)
      return null
    }

    return {
      name: screenData.name,
      type: screenData.type,
      size: screenData.size,
      children: this.parseComponents(screenData.children || []),
      layout: screenData.layout || { type: 'manual' },
      backgroundColor: screenData.background_color
    }
  }

  private parseComponents(children: any[]): ParsedComponent[] {
    return children.map((child: any, index: number) => ({
      name: child.name,
      type: child.type,
      index: child.index || index,
      size: child.size,
      position: child.position,
      visible: child.visible !== false,
      componentRef: child.component_ref,
      style: child.style || {},
      constraints: child.constraints,
      children: child.children ? this.parseComponents(child.children) : undefined
    }))
  }

  getAllScreens(): ParsedScreen[] {
    const screens = this.screenLayouts.screens || []
    return screens.map((screen: any) => ({
      name: screen.name,
      type: screen.type,
      size: screen.size,
      children: this.parseComponents(screen.children || []),
      layout: screen.layout || { type: 'manual' },
      backgroundColor: screen.background_color
    }))
  }

  /**
   * Get components for a specific screen that should be rendered
   * Filters out invisible components and sorts by index/z-order
   */
  getRenderableComponents(screenName: string): ParsedComponent[] {
    const screen = this.parseScreen(screenName)
    if (!screen) return []

    const filterRenderable = (components: ParsedComponent[]): ParsedComponent[] => {
      return components
        .filter(component => component.visible)
        .sort((a, b) => a.index - b.index)
        .map(component => ({
          ...component,
          children: component.children ? filterRenderable(component.children) : undefined
        }))
    }

    return filterRenderable(screen.children)
  }

  /**
   * Get layout patterns from the screen layouts
   */
  getLayoutPatterns(): any {
    return this.screenLayouts.layout_patterns || {}
  }

  /**
   * Get grid systems for responsive design
   */
  getGridSystems(): any {
    return this.screenLayouts.grid_systems || []
  }
}

// Export singleton instance
export const layoutParser = new LayoutParser('/extracted_login_assets_api/screen_layouts.json')