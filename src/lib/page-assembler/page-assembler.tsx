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
  private figmaToResponsiveLayout(component: ParsedComponent, index: number, totalComponents: number, screenLayout?: any): React.CSSProperties {
    const styles: React.CSSProperties = {}

    // Check if this is the main screen container
    if (component.name === 'Login' && component.type === 'frame') {
      // Use horizontal layout for the main login screen
      styles.display = 'flex'
      styles.flexDirection = 'row'
      styles.alignItems = 'stretch'
      styles.justifyContent = 'center'
      styles.minHeight = '100vh'
      styles.backgroundColor = screenLayout?.background_color || '#f4f4f4'
      styles.padding = '2rem'
      styles.gap = '2rem'
    } else if (component.name === 'bg') {
      // Handle the white background container - this should be a card container
      styles.display = 'flex'
      styles.flexDirection = 'column'
      styles.alignItems = 'center'
      styles.justifyContent = 'flex-start'
      styles.backgroundColor = component.style?.background_colors?.[0] || '#ffffff'
      styles.borderRadius = `${Math.min(component.style?.border_radius || 8, 16)}px`
      styles.padding = '2rem'
      styles.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)'
      styles.flex = '1'
      styles.maxWidth = '400px' // More constrained to match Figma design
      styles.width = '100%'
      styles.position = 'relative' // Allow proper positioning of child elements
    } else if (component.name === 'Illustration') {
      // Handle the illustration area
      styles.display = 'flex'
      styles.alignItems = 'center'
      styles.justifyContent = 'center'
      styles.flex = '1'
      styles.maxWidth = '600px'
    } else {
      // For form components, use proper spacing within the bg container
      styles.display = 'flex'
      styles.flexDirection = 'column'
      styles.alignItems = 'stretch'
      styles.margin = '0.5rem 0'
      styles.width = '100%'
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
      alignItems: 'stretch', // Changed from center to stretch for better alignment
      justifyContent: 'flex-start',
      margin: '0.5rem',
      padding: '0.5rem',
      width: '100%',
      maxWidth: '100%', // Use full width within constraints
    }

    // Handle text components with enhanced styling from Figma
    if (this.componentRegistry.isTextComponent(component.name)) {
      const textStyles: React.CSSProperties = {
        ...this.extractStyles(component),
        ...responsiveContainer,
        textAlign: 'left', // Changed from center to left alignment
        fontSize: '1.25rem',
        fontWeight: 'normal',
        alignSelf: 'flex-start', // Ensure left alignment within flex container
      }

      // Apply specific styling based on text component type
      switch (component.name) {
        case 'Welcome to Design School':
          textStyles.fontSize = '2rem'
          textStyles.fontWeight = 'bold'
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#2e2e2e'
          ;(textStyles as any).marginBottom = '1.5rem'
          // Remove background color to show text properly
          ;(textStyles as any).backgroundColor = 'transparent'
          ;(textStyles as any).textAlign = 'left'
          ;(textStyles as any).alignSelf = 'flex-start'
          break

        case 'or':
          textStyles.fontSize = '1rem'
          ;(textStyles as any).color = '#6b7280'
          textStyles.margin = '1rem 0'
          ;(textStyles as any).position = 'relative'
          ;(textStyles as any).backgroundColor = 'transparent'
          ;(textStyles as any).textAlign = 'center' // Keep "or" centered
          ;(textStyles as any).alignSelf = 'center'
          break

        case "Don't have an account? Register":
          textStyles.fontSize = '0.875rem'
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#000000'
          ;(textStyles as any).marginTop = '1rem'
          ;(textStyles as any).backgroundColor = 'transparent'
          ;(textStyles as any).textAlign = 'left'
          ;(textStyles as any).alignSelf = 'flex-start'
          break

        default:
          ;(textStyles as any).color = component.style?.background_colors?.[0] || '#374151'
          ;(textStyles as any).backgroundColor = 'transparent'
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
          // Apply Google button styling with border and proper colors
          ;(styles as any).backgroundColor = '#ffffff'
          ;(styles as any).color = '#000000'
          ;(styles as any).border = '1px solid #dadce0'
          ;(styles as any).borderRadius = '8px'
          ;(styles as any).padding = '12px 16px'
          ;(styles as any).fontSize = '16px'
          ;(styles as any).fontWeight = '500'
          ;(styles as any).display = 'flex'
          ;(styles as any).alignItems = 'center'
          ;(styles as any).justifyContent = 'center'
          ;(styles as any).gap = '8px'
          ;(styles as any).transition = 'all 0.2s ease'
          ;(styles as any).cursor = 'pointer'
          ;(styles as any).zIndex = '10'
          break

        case 'Login with facebook':
          componentProps.children = 'Continue with Facebook'
          componentProps.variant = 'outline'
          componentProps.className += ' facebook-btn'
          // Apply Facebook button styling with border and proper colors
          ;(styles as any).backgroundColor = '#1877f2'
          ;(styles as any).color = '#ffffff'
          ;(styles as any).border = '1px solid #1877f2'
          ;(styles as any).borderRadius = '8px'
          ;(styles as any).padding = '12px 16px'
          ;(styles as any).fontSize = '16px'
          ;(styles as any).fontWeight = '500'
          ;(styles as any).display = 'flex'
          ;(styles as any).alignItems = 'center'
          ;(styles as any).justifyContent = 'center'
          ;(styles as any).gap = '8px'
          ;(styles as any).transition = 'all 0.2s ease'
          ;(styles as any).cursor = 'pointer'
          ;(styles as any).zIndex = '10'
          break

        case 'button':
          componentProps.children = 'Login'
          componentProps.variant = 'default'
          componentProps.type = 'submit'
          componentProps.className += ' login-btn'
          // Apply primary purple color for login button
          ;(styles as any).backgroundColor = '#6257db' // Primary purple from design tokens
          ;(styles as any).color = '#ffffff'
          ;(styles as any).border = 'none'
          ;(styles as any).fontWeight = '500'
          ;(styles as any).fontSize = '16px'
          ;(styles as any).padding = '12px 24px'
          ;(styles as any).cursor = 'pointer'
          ;(styles as any).transition = 'all 0.2s ease'
          // Apply button styling from Figma
          if (component.style?.border_radius) {
            ;(styles as any).borderRadius = `${component.style.border_radius}px`
          } else {
            ;(styles as any).borderRadius = '8px'
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
          // Fix alignment - use flex with left alignment
          ;(styles as any).display = 'flex'
          ;(styles as any).alignItems = 'center'
          ;(styles as any).justifyContent = 'flex-start'
          ;(styles as any).textAlign = 'left'
          ;(styles as any).alignSelf = 'flex-start'
          ;(styles as any).width = '100%'
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
          ;(styles as any).textAlign = 'right'
          ;(styles as any).alignSelf = 'flex-end'
          ;(styles as any).fontSize = '14px'
          ;(styles as any).marginTop = '-1rem' // Position it properly next to Remember me
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

    // For the Login screen, use horizontal layout with illustration and form card
    if (screenName === 'Login') {
      const loginScreenStyles: React.CSSProperties = {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        minHeight: '100vh',
        backgroundColor: screen.backgroundColor || '#f4f4f4',
        padding: '2rem',
        gap: '2rem'
      }

      // Separate illustration and form components
      const illustrationComponent = components.find(c => c.name === 'Illustration')
      const bgComponent = components.find(c => c.name === 'bg')
      const otherComponents = components.filter(c => c.name !== 'Illustration' && c.name !== 'bg')

      return React.createElement(
        'div',
        {
          className: 'responsive-screen-login',
          style: loginScreenStyles
        },
        // Illustration side
        illustrationComponent && React.createElement(
          'div',
          {
            key: 'illustration-side',
            style: {
              flex: '1',
              maxWidth: '600px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }
          },
          this.assembleComponent({
            component: illustrationComponent,
            index: 0,
            totalComponents: 1
          })
        ),
        // Form card side (white background)
        bgComponent && React.createElement(
          'div',
          {
            key: 'form-card-side',
            style: {
              flex: '1',
              maxWidth: '400px',
              width: '100%',
              backgroundColor: bgComponent.style?.background_colors?.[0] || '#ffffff',
              borderRadius: `${Math.min(bgComponent.style?.border_radius || 8, 16)}px`,
              padding: '2rem',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'flex-start'
            }
          },
          // Render all form components within the white card with proper layout
          otherComponents.map((component, index) => {
            const assembledComponent = this.assembleComponent({
              component,
              index,
              totalComponents: otherComponents.length
            })

            // Special handling for Remember me and Forgot Password to position them side by side
            if (component.name === 'Remember me' || component.name === 'Forgot Password?') {
              return React.createElement(
                'div',
                {
                  key: `${component.name}-${component.index || index}-wrapper`,
                  style: {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: '100%',
                    margin: '0.5rem 0'
                  }
                },
                assembledComponent
              )
            }

            if (React.isValidElement(assembledComponent)) {
              return React.cloneElement(assembledComponent, {
                key: `${component.name}-${component.index || index}`,
                style: {
                  ...assembledComponent.props.style,
                  width: '100%',
                  maxWidth: '100%',
                  margin: '0.5rem 0'
                }
              })
            }
            return assembledComponent
          })
        )
      )
    }

    // Default screen assembly for non-login screens
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
      overflow: 'visible',
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