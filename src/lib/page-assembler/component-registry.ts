/**
 * Component Registry - Maps Figma component names to React components
 *
 * This registry handles the mapping between Figma component names
 * and the actual React components generated in Stage 3.
 */

import React from 'react'
import { ComponentRegistry } from './types'

// Import generated components
import { Button } from '../../components/navigation/button'
import { Login } from '../../components/navigation/login'
import { ForgotPassword } from '../../components/navigation/forgot-password'
import { Search } from '../../components/forms/search'
import { Password } from '../../components/forms/password'
import { RememberMe } from '../../components/forms/remember-me'
import { Bg } from '../../components/display/bg'

// Import existing components
import { Email } from '../../components/display/email'

/**
 * Component Registry Mapping
 * Maps Figma component names to React components
 */
const componentRegistry: ComponentRegistry = {
  // Navigation components
  'button': Button,
  'Button': Button,
  'login': Login,
  'Login': Login,
  'Login with Google': Button,
  'Login with facebook': Button,
  'Forgot Password?': ForgotPassword,
  'forgot-password': ForgotPassword,

  // Form components
  'search': Search,
  'search 1': Search,
  'Search': Search,
  'password': Password,
  'Password': Password,
  'Email': Email,
  'email': Email,
  'Remember me': RememberMe,
  'remember-me': RememberMe,

  // Display components
  'bg': Bg,
  'Bg': Bg,
  'background': Bg,

  // Text components (handled as simple text)
  'Welcome to Design School': 'text',
  'or': 'text',
  "Don't have an account? Register": 'text',

  // Placeholder components for icons and illustrations
  'Illustration': 'placeholder',
  'Vector': 'placeholder',
  'Group': 'placeholder',
  'bi:eye-fill': 'placeholder',
}

/**
 * Component Registry Class
 */
export class ComponentRegistryManager {
  private registry: ComponentRegistry

  constructor(customRegistry?: ComponentRegistry) {
    this.registry = { ...componentRegistry, ...customRegistry }
  }

  /**
   * Get a React component by its Figma name
   */
  getComponent(figmaName: string): React.ComponentType<any> | null {
    const component = this.registry[figmaName]
    return component || null
  }

  /**
   * Check if a component exists in the registry
   */
  hasComponent(figmaName: string): boolean {
    return figmaName in this.registry
  }

  /**
   * Register a new component
   */
  registerComponent(figmaName: string, component: React.ComponentType<any>): void {
    this.registry[figmaName] = component
  }

  /**
   * Get all registered component names
   */
  getRegisteredNames(): string[] {
    return Object.keys(this.registry)
  }

  /**
   * Check if a component is a text component
   */
  isTextComponent(figmaName: string): boolean {
    const component = this.registry[figmaName]
    return component === 'text'
  }

  /**
   * Check if a component is a placeholder
   */
  isPlaceholderComponent(figmaName: string): boolean {
    const component = this.registry[figmaName]
    return component === 'placeholder'
  }
}

// Export singleton instance
export const componentRegistryManager = new ComponentRegistryManager()

// Export the default registry for reference
export { componentRegistry }