/**
 * LayoutConverter - Converts Design JSON to Render JSON with token resolution
 * Part of the SimFlo Design Format system
 */
class LayoutConverter {
    constructor(designTokens) {
        this.tokenResolver = new TokenResolver(designTokens);
    }

    convert(designJson, viewport, theme = 'light') {
        // Real implementation with token resolution:
        // 1. Resolve design tokens using TokenResolver
        // 2. Calculate layouts with proper dimensions
        // 3. Convert components to renderable elements
        // 4. Handle responsive behavior

        // Extract the actual screen data from the input
        const screenName = designJson.currentScreenName || 'Login';
        const screen = designJson.screen || designJson.screens?.[screenName] || designJson;
        const components = designJson.components || {};
        const designTokens = designJson.designTokens || {};

        // Update token resolver with current design tokens
        this.tokenResolver = new TokenResolver(designTokens, theme);

        return this.convertScreen(screen, viewport, components, screenName);
    }

    convertScreen(screen, viewport, components, screenName = 'Unknown') {
        const elements = [];

        // Add background
        const backgroundColor = this.tokenResolver.resolveColor('colors.background.secondary');
        elements.push({
            id: "background",
            type: "rectangle",
            bounds: { x: 0, y: 0, width: viewport.width, height: viewport.height },
            styles: { backgroundColor }
        });

        // Process screen children
        if (screen.children && screen.children.length > 0) {
            const screenElements = this.processChildren(screen.children, viewport, components);
            elements.push(...screenElements);
        }

        return {
            version: "1.0.0",
            viewport,
            metadata: {
                screenName: screenName,
                theme: this.tokenResolver.theme,
                generatedAt: new Date().toISOString()
            },
            elements
        };
    }

    processChildren(children, parentBounds, components) {
        const elements = [];

        // Calculate padding
        const padding = this.tokenResolver.parseDimension('spacing.6'); // 24px
        const availableWidth = parentBounds.width - (padding * 2);
        const availableHeight = parentBounds.height - (padding * 2);

        let currentY = parentBounds.y + padding;

        for (const child of children) {
            const element = this.processChild(child, {
                x: parentBounds.x + padding,
                y: currentY,
                width: availableWidth,
                height: availableHeight - (currentY - parentBounds.y)
            }, components);

            if (element) {
                elements.push(element);
                currentY += element.bounds.height + this.tokenResolver.parseDimension('spacing.4'); // 16px gap
            }
        }

        return elements;
    }

    processChild(child, parentBounds, components) {
        if (child.type === 'component') {
            return this.processComponent(child, parentBounds, components);
        } else if (child.type === 'text') {
            return this.processText(child, parentBounds);
        }
        return null;
    }

    processComponent(child, parentBounds, components) {
        const componentDef = components[child.name];
        if (!componentDef) {
            console.warn(`Component not found: ${child.name}`);
            return null;
        }

        // Calculate dimensions
        const width = this.calculateComponentWidth(child, componentDef, parentBounds.width);

        // Process nested content first to calculate proper height
        const content = this.resolveComponentContent(componentDef, child);
        let nestedElements = [];
        let calculatedHeight = this.calculateComponentHeight(child, componentDef);

        if (content && content.children && Array.isArray(content.children)) {
            // Calculate height based on nested content
            calculatedHeight = this.calculateContainerHeight(content.children, width);
            const nestedBounds = { x: 0, y: 0, width, height: calculatedHeight };
            nestedElements = this.processNestedContent(content.children, nestedBounds, components);

            // Adjust nested element coordinates to be relative to parent component's position
            const parentX = parentBounds.x + (parentBounds.width - width) / 2;
            const parentY = parentBounds.y;

            nestedElements.forEach(nested => {
                if (nested.bounds) {
                    nested.bounds.x += parentX;
                    nested.bounds.y += parentY;
                }
            });
        }

        // Center horizontally
        const x = parentBounds.x + (parentBounds.width - width) / 2;

        return {
            id: `${child.name.toLowerCase()}-${Date.now()}`,
            type: this.getElementType(child.name),
            bounds: { x, y: parentBounds.y, width, height: calculatedHeight },
            styles: this.resolveComponentStyles(componentDef, child.variant),
            content: content,
            nestedElements: nestedElements
        };
    }

    processText(child, parentBounds) {
        const fontSize = this.tokenResolver.parseDimension(child.properties.fontSize || 'fontSize.base');
        const lineHeight = fontSize * 1.4;

        return {
            id: `text-${Date.now()}`,
            type: "text",
            bounds: {
                x: parentBounds.x,
                y: parentBounds.y,
                width: parentBounds.width,
                height: lineHeight
            },
            styles: {
                color: this.tokenResolver.resolveColor(child.properties.color || 'colors.text.primary'),
                fontSize: `${fontSize}px`,
                fontFamily: this.tokenResolver.resolve('fontFamily.primary') || 'Inter, system-ui, sans-serif',
                fontWeight: this.tokenResolver.resolve(child.properties.fontWeight) || 'normal',
                textAlign: child.properties.align || 'left'
            },
            content: {
                type: 'text',
                properties: {
                    text: child.properties.value || '',
                    maxLines: child.properties.maxLines || 1
                }
            }
        };
    }

    calculateComponentWidth(child, componentDef, parentWidth) {
        const layout = { ...componentDef.layout, ...child.layout };

        if (layout.width === '100%') {
            return parentWidth;
        }

        if (typeof layout.width === 'string' && layout.width.endsWith('%')) {
            return parentWidth * (parseFloat(layout.width) / 100);
        }

        if (layout.maxWidth) {
            const maxWidth = this.tokenResolver.parseDimension(layout.maxWidth, parentWidth);
            return Math.min(parentWidth, maxWidth);
        }

        return this.tokenResolver.parseDimension(layout.width, parentWidth) || parentWidth;
    }

    calculateComponentHeight(child, componentDef) {
        const layout = { ...componentDef.layout, ...child.layout };
        return this.tokenResolver.parseDimension(layout.height) || 48; // Default height
    }

    getElementType(componentName) {
        if (componentName === 'Button') return 'button';
        if (componentName === 'Input') return 'input-field';
        return 'rounded-rectangle';
    }

    resolveComponentStyles(componentDef, variant = 'default') {
        const styles = { ...componentDef.styles };

        // Apply variant styles
        if (componentDef.variants) {
            const variantDef = componentDef.variants.find(v => v.name === variant);
            if (variantDef) {
                Object.assign(styles, variantDef.styles);
            }
        }

        // Resolve tokens
        const resolvedStyles = {};
        for (const [key, value] of Object.entries(styles)) {
            if (key.includes('Color')) {
                resolvedStyles[key] = this.tokenResolver.resolveColor(value);
            } else if (key.includes('Radius') || key.includes('Width') || key.includes('Blur')) {
                resolvedStyles[key] = this.tokenResolver.parseDimension(value);
            } else {
                resolvedStyles[key] = this.tokenResolver.resolve(value) || value;
            }
        }

        return resolvedStyles;
    }

    resolveComponentContent(componentDef, child) {
        if (child.content) {
            return child.content;
        }
        return componentDef.content;
    }

    processNestedContent(children, parentBounds, components) {
        const elements = [];
        const padding = this.tokenResolver.parseDimension('spacing.4'); // 16px
        let currentY = parentBounds.y + padding;

        for (const child of children) {
            const childBounds = {
                x: parentBounds.x + padding,
                y: currentY,
                width: parentBounds.width - (padding * 2),
                height: this.calculateElementHeight(child)
            };

            let element;
            if (child.type === 'text') {
                element = this.processText(child, childBounds);
            } else if (child.type === 'component') {
                element = this.processComponent(child, childBounds, components);
            }

            if (element) {
                // Make sure the element has proper bounds
                if (!element.bounds) {
                    element.bounds = childBounds;
                }
                elements.push(element);
                currentY += element.bounds.height + this.tokenResolver.parseDimension('spacing.3'); // 12px gap
            }
        }

        return elements;
    }

    calculateElementHeight(child) {
        if (child.type === 'text') {
            const fontSize = this.tokenResolver.parseDimension(child.properties.fontSize || 'fontSize.base');
            return fontSize * 1.4; // Line height
        } else if (child.type === 'component') {
            return 48; // Default component height
        }
        return 48; // Default fallback
    }

    calculateContainerHeight(children, containerWidth) {
        const padding = this.tokenResolver.parseDimension('spacing.4') * 2; // Top and bottom padding
        const spacing = this.tokenResolver.parseDimension('spacing.3'); // Gap between elements
        let totalHeight = padding;

        for (const child of children) {
            totalHeight += this.calculateElementHeight(child);
            totalHeight += spacing; // Add gap after each element
        }

        // Remove the last gap
        totalHeight -= spacing;

        return Math.max(totalHeight, 48); // Minimum height
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LayoutConverter;
}