/**
 * Page Assembler - Main page assembly engine
 *
 * This module handles the assembly of complete pages from Figma layouts
 * by combining layout parsing, component registry, and responsive design.
 */

import React from 'react'
import { LayoutParser, ParsedScreen, ParsedComponent } from './layout-parser'
import { ComponentRegistryManager } from './component-registry'
import { LayoutStyle, ComponentPosition, ComponentSize } from './types'

export interface PageAssemblerProps {
  screenName: string
  className?: string
  style?: React.CSSProperties
  responsive?: boolean
}

export interface AssembledComponentProps {
  component: ParsedComponent
  index?: number
  totalComponents?: number
}

/**
 * Page Assembler Class
 */
export class PageAssembler {
  private layoutParser: LayoutParser
  private componentRegistry: ComponentRegistryManager

  constructor(screenLayoutsPath?: string) {
    this.layoutParser = new LayoutParser(screenLayoutsPath || '/extracted_login_assets_api/screen_layouts.json')
    this.componentRegistry = new ComponentRegistryManager()
  }

  /**
   * Convert Figma layout to responsive CSS layout
   */
  private figmaToResponsiveLayout(component: ParsedComponent, index: number, totalComponents: number): React.CSSProperties {
    const styles: React.CSSProperties = {}

    // Remove absolute positioning - use flexbox/grid instead
    // Use flexbox for responsive layout
    styles.display = 'flex'
    styles.flexDirection = 'column'
    styles.alignItems = 'center'
    styles.justifyContent = 'center'
    styles.margin = '0.5rem'
    styles.padding = '1rem'

    // Maintain aspect ratio using responsive sizing
    if (component.size) {
      const aspectRatio = component.size.width / component.size.height
      styles.maxWidth = '100%'
      styles.width = 'auto'
      styles.height = 'auto'
    }

    return styles
  }

  /**
   * Convert Figma size to CSS dimensions
   */
  private figmaSizeToCss(size: ComponentSize): Partial<LayoutStyle> {
    return {
      width: `${size.width}px`,
      height: `${size.height}px`,
    }
  }

  /**
   * Extract style properties from Figma component (responsive version)
   */
  private extractStyles(component: ParsedComponent): Partial<LayoutStyle> {
    const styles: Partial<LayoutStyle> = {}

    // Use responsive sizing instead of fixed Figma dimensions
    // Don't add absolute positioning - let flexbox handle layout

    // Add background color if present
    if (component.style?.background_colors?.length > 0) {
      styles.backgroundColor = component.style.background_colors[0]
    }

    // Add border radius if present
    if (component.style?.border_radius) {
      styles.borderRadius = `${Math.min(component.style.border_radius, 12)}px` // Cap border radius for mobile
    }

    // Add opacity if present
    if (component.style?.opacity !== undefined) {
      styles.opacity = component.style.opacity
    }

    // Add responsive padding/margins
    styles.padding = '0.75rem 1rem'
    styles.margin = '0.25rem'
    styles.maxWidth = '100%'

    return styles
  }

  /**
   * Assemble a single component (responsive version)
   */
  private assembleComponent({ component, index, totalComponents }: AssembledComponentProps): React.ReactNode {
    const Component = this.componentRegistry.getComponent(component.name)

    // Create responsive container for all components
    const responsiveContainer = {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      margin: '0.5rem',
      padding: '0.5rem',
      width: '100%',
      maxWidth: '400px', // Reasonable max width for mobile
    }

    // Handle text components with enhanced styling from Figma
    if (this.componentRegistry.isTextComponent(component.name)) {
      const textStyles: React.CSSProperties = {
        ...this.extractStyles(component),
        ...responsiveContainer,
        textAlign: 'center',
        fontSize: '1.25rem',
        fontWeight: 'normal',
      }

      // Apply specific styling based on text component type
      switch (component.name) {
        case 'Welcome to Design School':
          textStyles.fontSize = '2rem'
          textStyles.fontWeight = 'bold'
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#2e2e2e'
          ;(textStyles as any).marginBottom = '1.5rem'
          break

        case 'or':
          textStyles.fontSize = '1rem'
          ;(textStyles as any).color = '#6b7280'
          textStyles.margin = '1rem 0'
          ;(textStyles as any).position = 'relative'
          break

        case "Don't have an account? Register":
          textStyles.fontSize = '0.875rem'
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#000000'
          ;(textStyles as any).marginTop = '1rem'
          break

        default:
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#374151'
      }

      return React.createElement(
        'div',
        {
          key: `${component.name}-${index}`,
          style: textStyles,
          className: `text-component ${component.name.toLowerCase().replace(/\s+/g, '-')}`
        },
        component.name
      )
    }

    // Handle placeholder components (icons, illustrations)
    if (this.componentRegistry.isPlaceholderComponent(component.name)) {
      const placeholderStyles: React.CSSProperties = {
        ...this.extractStyles(component),
        ...responsiveContainer,
        backgroundColor: '#f0f0f0',
        border: '1px dashed #ccc',
        borderRadius: '8px',
        minHeight: '80px',
        fontSize: '12px',
        color: '#666',
        textAlign: 'center',
      }

      return React.createElement(
        'div',
        {
          key: `${component.name}-${index}`,
          style: placeholderStyles,
          className: `placeholder ${component.name.toLowerCase().replace(/\s+/g, '-')}`
        },
        component.name
      )
    }

    // Handle actual React components
    if (Component) {
      const styles: React.CSSProperties = {
        ...this.extractStyles(component),
        ...responsiveContainer,
      }

      const componentProps: any = {
        style: styles,
        className: `responsive-component ${component.name.toLowerCase().replace(/\s+/g, '-')}`,
      }

      // Enhanced component-specific props based on Figma component names
      switch (component.name) {
        case 'Login with Google':
          componentProps.children = 'Continue with Google'
          componentProps.variant = 'outline'
          componentProps.className += ' google-btn'
          // Apply Google brand colors from Figma if available
          if (component.style?.background_colors?.length > 0) {
            ;(styles as any).backgroundColor = '#4285f4'
            ;(styles as any).color = '#ffffff'
          }
          break

        case 'Login with facebook':
          componentProps.children = 'Continue with Facebook'
          componentProps.variant = 'outline'
          componentProps.className += ' facebook-btn'
          // Apply Facebook brand colors from Figma if available
          if (component.style?.background_colors?.length > 0) {
            ;(styles as any).backgroundColor = '#1877f2'
            ;(styles as any).color = '#ffffff'
          }
          break

        case 'button':
          componentProps.children = 'Login'
          componentProps.variant = 'default'
          componentProps.type = 'submit'
          componentProps.className += ' login-btn'
          // Apply button styling from Figma
          if (component.style?.background_colors?.length > 0) {
            ;(styles as any).backgroundColor = component.style.background_colors[0]
          }
          if (component.style?.border_radius) {
            ;(styles as any).borderRadius = `${component.style.border_radius}px`
          }
          break

        case 'Email':
          componentProps.placeholder = 'Enter your email'
          componentProps.type = 'email'
          componentProps.className += ' email-input'
          // Apply input styling from Figma
          ;(styles as any).width = '100%'
          ;(styles as any).padding = '12px 16px'
          ;(styles as any).border = '1px solid #d1d5db'
          ;(styles as any).borderRadius = '6px'
          break

        case 'Password':
          componentProps.placeholder = 'Enter your password'
          componentProps.type = 'password'
          componentProps.className += ' password-input'
          // Apply input styling from Figma
          ;(styles as any).width = '100%'
          ;(styles as any).padding = '12px 16px'
          ;(styles as any).border = '1px solid #d1d5db'
          ;(styles as any).borderRadius = '6px'
          break

        case 'Remember me':
          componentProps.children = 'Remember me'
          componentProps.type = 'checkbox'
          componentProps.className += ' remember-me-checkbox'
          // Apply checkbox styling from Figma
          if (component.style?.border_radius) {
            ;(styles as any).borderRadius = `${component.style.border_radius}px`
          }
          break

        case 'Forgot Password?':
          componentProps.children = 'Forgot Password?'
          componentProps.variant = 'link'
          componentProps.className += ' forgot-password-link'
          // Apply link styling from Figma
          if (component.style?.background_colors?.length > 0) {
            ;(styles as any).color = component.style.background_colors[0]
          }
          ;(styles as any).textDecoration = 'underline'
          ;(styles as any).cursor = 'pointer'
          break

        case 'Welcome to Design School':
          // Welcome text is handled by text component logic
          break

        case 'bg':
          // Background component - apply proper styling from Figma
          if (component.style?.background_colors?.length > 0) {
            ;(styles as any).backgroundColor = component.style.background_colors[0]
          }
          if (component.style?.border_radius) {
            ;(styles as any).borderRadius = `${component.style.border_radius}px`
          }
          ;(styles as any).minHeight = '400px' // Ensure background has proper height
          ;(styles as any).padding = '2rem'
          break

        default:
          // Fallback for unknown components
          if (component.name.toLowerCase().includes('button')) {
            componentProps.children = component.name
            componentProps.className += ' btn-primary'
          }
      }

      return React.createElement(Component, componentProps, componentProps.children)
    }

    // Fallback: render as a div
    const fallbackStyles: React.CSSProperties = {
      ...this.extractStyles(component),
      ...responsiveContainer,
    }

    return React.createElement(
      'div',
      {
        key: `${component.name}-${index}`,
        style: fallbackStyles,
        className: `component-fallback ${component.name.toLowerCase().replace(/\s+/g, '-')}`,
        'data-component-name': component.name,
        'data-component-type': component.type
      },
      component.name
    )
  }

  /**
   * Assemble a complete screen (responsive version)
   */
  public assembleScreen(screenName: string): React.ReactNode {
    const screen = this.layoutParser.parseScreen(screenName)
    if (!screen) {
      return React.createElement(
        'div',
        { className: 'error-screen' },
        React.createElement('h2', null, 'Screen Not Found'),
        React.createElement('p', null, `Screen "${screenName}" could not be found in the layout data.`)
      )
    }

    const components = this.layoutParser.getRenderableComponents(screenName)

    // Responsive screen styles - no more fixed dimensions!
    const screenStyles: React.CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      maxWidth: '100%',
      minHeight: '100vh',
      padding: '2rem 1rem',
      backgroundColor: screen.backgroundColor || '#ffffff',
      overflow: 'visible', // Changed from hidden to visible
    }

    return React.createElement(
      'div',
      {
        className: `responsive-screen-${screen.name.toLowerCase().replace(/\s+/g, '-')}`,
        style: screenStyles
      },
      components.map((component, index) => {
        const assembledComponent = this.assembleComponent({
          component,
          index,
          totalComponents: components.length
        })
        // Ensure the assembled component has a key
        if (React.isValidElement(assembledComponent)) {
          return React.cloneElement(assembledComponent, {
            key: `${component.name}-${component.index || index}`
          })
        }
        return assembledComponent
      })
    )
  }

  /**
   * Get available screens
   */
  public getAvailableScreens(): string[] {
    const screens = this.layoutParser.getAllScreens()
    return screens.map(screen => screen.name)
  }

  /**
   * Get screen metadata
   */
  public getScreenMetadata(screenName: string): ParsedScreen | null {
    return this.layoutParser.parseScreen(screenName)
  }
}

/**
 * React Component for Page Assembly
 */
export const PageAssemblerComponent: React.FC<PageAssemblerProps> = ({
  screenName,
  className,
  style,
  responsive = false
}) => {
  const assembler = new PageAssembler()

  if (responsive) {
    // TODO: Implement responsive layout with breakpoints
    // For now, just render the standard screen
  }

  const screenContent = assembler.assembleScreen(screenName)

  return React.createElement(
    'div',
    {
      className: `page-assembler ${className || ''}`,
      style
    },
    screenContent
  )
}

// Export singleton instance
export const pageAssembler = new PageAssembler()