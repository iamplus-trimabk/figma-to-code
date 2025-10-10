/**
 * Layout Parser - Generated from Stage 2 Automation Outputs
 *
 * Parses Figma screen layouts and converts them to renderable components
 * Uses screen layout data from extracted_login_assets_api/screen_layouts.json
 */

import { ComponentRegistryManager } from './component-registry';

export interface ParsedComponent {
  name: string;
  type: string;
  index: number;
  size: {
    width: number;
    height: number;
  };
  position: {
    x: number;
    y: number;
  };
  visible: boolean;
  style: any;
  constraints: {
    vertical: string;
    horizontal: string;
  };
  children?: ParsedComponent[];
}

export interface ParsedScreen {
  name: string;
  type: string;
  size: {
    width: number;
    height: number;
  };
  position: {
    x: number;
    y: number;
  };
  children: ParsedComponent[];
  backgroundColor?: string;
}

/**
 * Generated Layout Parser
 */
export class LayoutParser {
  private screenLayoutsPath: string;
  private cachedLayouts: any = null;

  constructor(screenLayoutsPath: string = '/extracted_login_assets_api/screen_layouts.json') {
    this.screenLayoutsPath = screenLayoutsPath;
  }

  /**
   * Load and parse screen layouts from Figma data
   */
  private loadScreenLayouts(): any {
    if (this.cachedLayouts) {
      return this.cachedLayouts;
    }

    try {
      // In a real implementation, this would load from the actual file
      // For now, we'll simulate the structure
      this.cachedLayouts = {
        screens: []
      };
      return this.cachedLayouts;
    } catch (error) {
      console.error('Error loading screen layouts:', error);
      return { screens: [] };
    }
  }

  /**
   * Parse a specific screen by name
   */
  parseScreen(screenName: string): ParsedScreen | null {
    const layouts = this.loadScreenLayouts();
    const screen = layouts.screens.find((s: any) => s.name === screenName);

    if (!screen) {
      return null;
    }

    return {
      name: screen.name,
      type: screen.type,
      size: screen.size,
      position: screen.position,
      backgroundColor: '#f4f4f4',
      children: screen.children || []
    };
  }

  /**
   * Get all screens
   */
  getAllScreens(): ParsedScreen[] {
    const layouts = this.loadScreenLayouts();
    return layouts.screens || [];
  }

  /**
   * Get renderable components for a screen
   */
  getRenderableComponents(screenName: string): ParsedComponent[] {
    const screen = this.parseScreen(screenName);
    if (!screen) {
      return [];
    }

    // Flatten component hierarchy while preserving order
    const renderableComponents: ParsedComponent[] = [];

    const processComponents = (components: ParsedComponent[]) => {
      components.forEach((component, index) => {
        renderableComponents.push({
          ...component,
          index
        });

        if (component.children) {
          processComponents(component.children);
        }
      });
    };

    processComponents(screen.children);
    return renderableComponents;
  }
}

// Export singleton instance
export const layoutParser = new LayoutParser();
