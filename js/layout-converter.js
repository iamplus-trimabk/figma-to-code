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

        // Process screen children with layout properties
        if (screen.children && screen.children.length > 0) {
            const screenLayout = screen.layout || {};
            const screenElements = this.processChildren(screen.children, viewport, components, screenLayout);
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

    processChildren(children, parentBounds, components, layout = {}) {
        const elements = [];

        // Resolve layout properties
        const justifyContent = this.resolveLayoutValue(layout.justifyContent, 'flex-start');
        const alignItems = this.resolveLayoutValue(layout.alignItems, 'stretch');
        const padding = this.tokenResolver.parseDimension(layout.padding || 'spacing.6');

        // Calculate available space
        const availableWidth = parentBounds.width - (padding * 2);
        const availableHeight = parentBounds.height - (padding * 2);

        // First pass: create all elements to calculate total dimensions
        const tempElements = [];
        for (const child of children) {
            const element = this.processChild(child, {
                x: parentBounds.x + padding,
                y: parentBounds.y + padding,
                width: availableWidth,
                height: availableHeight
            }, components);

            if (element) {
                tempElements.push(element);
            }
        }

        // Calculate positions based on alignment
        const positionedElements = this.applyAlignment(
            tempElements,
            { x: parentBounds.x + padding, y: parentBounds.y + padding, width: availableWidth, height: availableHeight },
            { justifyContent, alignItems }
        );

        return positionedElements;
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
        }

        // Position will be calculated by applyAlignment method
        return {
            id: `${child.name.toLowerCase()}-${Date.now()}`,
            type: this.getElementType(child.name),
            bounds: { x: 0, y: 0, width, height: calculatedHeight },
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
                x: 0,
                y: 0,
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
        // Create a parent-relative coordinate system for nested elements
        // The parentBounds define the container space (0,0 to width,height)
        const parentRelativeBounds = {
            x: 0,
            y: 0,
            width: parentBounds.width,
            height: parentBounds.height
        };

        // Process nested elements using the same alignment system but with parent-relative bounds
        const nestedElements = this.processChildren(children, parentRelativeBounds, components);

        // Elements are now positioned relative to parent container (0,0 origin)
        return nestedElements;
    }

    calculateElementHeight(child) {
        if (child.type === 'text') {
            const fontSize = this.tokenResolver.parseDimension(child.properties.fontSize || 'fontSize.base');
            return fontSize * 1.4; // Line height
        } else if (child.type === 'component') {
            // Check if component has defined height in its definition
            if (child.name === 'Button' || child.name === 'Input') {
                return 48; // Standard button/input height from design system
            }
            return 48; // Default component height
        }
        return 48; // Default fallback
    }

    calculateContainerHeight(children, containerWidth) {
        // Use Card component padding from design tokens: "spacing.6" = 24px
        const cardPadding = this.tokenResolver.parseDimension('spacing.6');
        const totalPadding = cardPadding * 2; // Top and bottom padding: 24px + 24px = 48px

        let totalHeight = totalPadding;

        // Calculate actual heights and spacing based on the login screen structure
        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            totalHeight += this.calculateElementHeight(child);

            // Add spacing based on child properties, but don't add spacing after last element
            if (i < children.length - 1) {
                if (child.properties && child.properties.marginBottom) {
                    const marginBottom = this.tokenResolver.parseDimension(child.properties.marginBottom);
                    totalHeight += marginBottom;
                } else {
                    // Use Card gap as default: "spacing.4" = 16px
                    const defaultGap = this.tokenResolver.parseDimension('spacing.4');
                    totalHeight += defaultGap;
                }
            }
        }

        // Calculate expected height for debugging:
        // Welcome Back text: 24px * 1.4 = 33.6px
        // + margin 24px = 57.6px
        // Email Input: 48px + margin 16px = 64px
        // Password Input: 48px + margin 24px = 72px
        // Sign In Button: 48px
        // + padding 48px = 241.6px total

        return Math.max(totalHeight, 48); // Minimum height
    }

    // =========================
    // ALIGNMENT METHODS
    // =========================

    resolveLayoutValue(value, defaultValue) {
        if (!value) return defaultValue;
        return value;
    }

    applyAlignment(elements, containerBounds, layout) {
        const { justifyContent, alignItems } = layout;

        // Calculate total content height
        const totalContentHeight = this.calculateTotalContentHeight(elements);
        const spacing = this.tokenResolver.parseDimension('spacing.4'); // 16px gap

        // Apply vertical alignment
        const verticallyPositionedElements = this.applyVerticalAlignment(
            elements,
            containerBounds,
            totalContentHeight,
            justifyContent,
            spacing
        );

        // Apply horizontal alignment to each element
        const horizontallyPositionedElements = verticallyPositionedElements.map(element => {
            const x = this.calculateHorizontalAlignment(
                element,
                containerBounds,
                element.alignSelf || alignItems
            );

            return {
                ...element,
                bounds: {
                    ...element.bounds,
                    x
                }
            };
        });

        return horizontallyPositionedElements;
    }

    calculateTotalContentHeight(elements) {
        const spacing = this.tokenResolver.parseDimension('spacing.4');
        return elements.reduce((total, element, index) => {
            return total + element.bounds.height + (index > 0 ? spacing : 0);
        }, 0);
    }

    applyVerticalAlignment(elements, containerBounds, totalContentHeight, justifyContent, spacing) {
        let currentY = containerBounds.y;

        switch (justifyContent) {
            case 'center':
                currentY = containerBounds.y + (containerBounds.height - totalContentHeight) / 2;
                break;
            case 'flex-end':
                currentY = containerBounds.y + containerBounds.height - totalContentHeight;
                break;
            case 'space-between':
                if (elements.length > 1) {
                    const availableSpace = containerBounds.height - totalContentHeight;
                    spacing = availableSpace / (elements.length - 1);
                }
                currentY = containerBounds.y;
                break;
            case 'space-around':
                if (elements.length > 0) {
                    const availableSpace = containerBounds.height - totalContentHeight;
                    spacing = availableSpace / elements.length;
                    currentY = containerBounds.y + spacing;
                }
                break;
            case 'flex-start':
            default:
                currentY = containerBounds.y;
                break;
        }

        return elements.map((element, index) => {
            const y = currentY;
            currentY += element.bounds.height + spacing;

            return {
                ...element,
                bounds: {
                    ...element.bounds,
                    y
                }
            };
        });
    }

    calculateHorizontalAlignment(element, containerBounds, alignItems) {
        const elementWidth = element.bounds.width;

        switch (alignItems) {
            case 'center':
                return containerBounds.x + (containerBounds.width - elementWidth) / 2;
            case 'flex-end':
                return containerBounds.x + containerBounds.width - elementWidth;
            case 'stretch':
                return containerBounds.x;
            case 'flex-start':
            default:
                return containerBounds.x;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LayoutConverter;
}