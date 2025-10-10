/**
 * Component Registry - Generated from Stage 2 Automation Outputs
 *
 * Automatically maps Figma component names to React components
 * Uses component interfaces from stage_2_outputs/component_interfaces.json
 */

import React from 'react'

// Generated component imports from stage 2 interfaces
import { Bg as GeneratedBg } from "@/components/display/bg"
import { Search as GeneratedSearch } from "@/components/forms/search"
import { ForgotPassword as GeneratedForgotPassword } from "@/components/navigation/forgot-password"
import { Email as GeneratedEmail } from "@/components/display/email"
import { Password as GeneratedPassword } from "@/components/forms/password"
import { Button as GeneratedButton } from "@/components/navigation/button"
import { RememberMe as GeneratedRememberMe } from "@/components/forms/remember-me"
import { Login as GeneratedLogin } from "@/components/navigation/login"
import { Image as GeneratedImage } from "@/components/display/image"


/**
 * Generated Component Registry Manager
 */
export class ComponentRegistryManager {
  private componentMap = new Map<string, React.ComponentType<any>>([
    ['Bg', GeneratedBg],
    ['Search', GeneratedSearch],
    ['ForgotPassword', GeneratedForgotPassword],
    ['Email', GeneratedEmail],
    ['Password', GeneratedPassword],
    ['Button', GeneratedButton],
    ['RememberMe', GeneratedRememberMe],
    ['Login', GeneratedLogin],
    ['Image', GeneratedImage],
  ]);

  /**
   * Get React component for Figma component name
   */
  getComponent(componentName: string): React.ComponentType<any> | null {
    return this.componentMap.get(componentName) || null;
  }

  /**
   * Check if component is a text component
   */
  isTextComponent(componentName: string): boolean {
    const textComponents = [
      'Welcome to Design School',
      'or',
      "Don't have an account? Register",
      'Remember me'
    ];
    return textComponents.includes(componentName);
  }

  /**
   * Check if component is a placeholder component
   */
  isPlaceholderComponent(componentName: string): boolean {
    const placeholderComponents = [
      'Illustration',
      'Vector',
      'Group',
      'image 1'
    ];
    return placeholderComponents.includes(componentName);
  }

  /**
   * Get all registered components
   */
  getRegisteredComponents(): string[] {
    return Array.from(this.componentMap.keys());
  }
}

// Export singleton instance
export const componentRegistry = new ComponentRegistryManager();
