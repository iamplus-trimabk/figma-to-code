/**
 * CanvasRenderer - Handles pixel-perfect rendering of design elements to HTML5 canvas
 * Part of the SimFlo Design Format system
 */
class CanvasRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
    }

    clear() {
        // Clear all pixels
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Reset canvas context state completely
        this.ctx.resetTransform();
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);

        // Reset all context properties to defaults
        this.ctx.globalAlpha = 1;
        this.ctx.globalCompositeOperation = 'source-over';
        this.ctx.strokeStyle = '#000000';
        this.ctx.fillStyle = '#000000';
        this.ctx.lineWidth = 1;
        this.ctx.lineCap = 'butt';
        this.ctx.lineJoin = 'miter';
        this.ctx.miterLimit = 10;
        this.ctx.lineDashOffset = 0;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
        this.ctx.shadowBlur = 0;
        this.ctx.shadowColor = 'rgba(0, 0, 0, 0)';
        this.ctx.font = '10px sans-serif';
        this.ctx.textAlign = 'start';
        this.ctx.textBaseline = 'alphabetic';
        this.ctx.direction = 'ltr';
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'low';

        // Clear any existing clipping paths
        this.ctx.restore();
        this.ctx.save();
    }

    renderElement(element) {
        const { type, bounds, styles, content, nestedElements } = element;

        // Skip rendering if bounds are invalid
        if (!bounds || bounds.x === null || bounds.y === null || bounds.width === null || bounds.height === null) {
            console.warn(`Skipping element with invalid bounds:`, element);
            return;
        }

        // Save context state
        this.ctx.save();

        try {
            // Apply common styles
            this.applyStyles(styles);

            // Draw element based on type
            switch (type) {
                case 'rectangle':
                    this.drawRectangle(bounds);
                    break;
                case 'rounded-rectangle':
                    this.drawRoundedRectangle(bounds, styles.borderRadius || 0);
                    break;
                case 'text':
                    this.drawText(bounds, content);
                    break;
                case 'input-field':
                    this.drawInputField(bounds, styles, content);
                    break;
                case 'button':
                    this.drawButton(bounds, styles, content);
                    break;
            }

            // Render nested elements if they exist
            if (nestedElements && Array.isArray(nestedElements) && nestedElements.length > 0) {
                this.renderNestedElements(nestedElements, bounds);
            }
        } catch (error) {
            console.error('Error rendering element:', element, error);
        } finally {
            // Always restore context state
            this.ctx.restore();
        }
    }

    renderNestedElements(nestedElements, parentBounds) {
        // Create a new context state for nested elements
        this.ctx.save();

        try {
            // Translate to parent container position - this creates parent-relative coordinate system
            this.ctx.translate(parentBounds.x, parentBounds.y);

            // Create clipping region to constrain nested elements to parent bounds
            this.ctx.beginPath();
            this.ctx.rect(0, 0, parentBounds.width, parentBounds.height);
            this.ctx.clip();

            // Reset shadow for nested elements to avoid parent shadows affecting children
            this.ctx.shadowColor = 'transparent';
            this.ctx.shadowBlur = 0;
            this.ctx.shadowOffsetX = 0;
            this.ctx.shadowOffsetY = 0;

            // Render nested elements with parent-relative coordinates
            for (const nestedElement of nestedElements) {
                // Create a copy of the element with adjusted bounds for parent-relative positioning
                const adjustedElement = {
                    ...nestedElement,
                    bounds: {
                        ...nestedElement.bounds,
                        // Nested elements should already have parent-relative coordinates
                        // from LayoutConverter, so we don't need additional transformation
                    }
                };
                this.renderElement(adjustedElement);
            }
        } catch (error) {
            console.error('Error rendering nested elements:', error);
        } finally {
            // Restore context state to return to global coordinate system
            this.ctx.restore();
        }
    }

    applyStyles(styles) {
        // Apply background
        if (styles.backgroundColor) {
            this.ctx.fillStyle = styles.backgroundColor;
        }

        // Apply shadow
        if (styles.shadowColor) {
            this.ctx.shadowColor = styles.shadowColor;
            this.ctx.shadowOffsetX = styles.shadowOffsetX || 0;
            this.ctx.shadowOffsetY = styles.shadowOffsetY || 0;
            this.ctx.shadowBlur = styles.shadowBlur || 0;
        }
    }

    drawRectangle(bounds) {
        this.ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
    }

    drawRoundedRectangle(bounds, radius) {
        const x = bounds.x;
        const y = bounds.y;
        const width = bounds.width;
        const height = bounds.height;

        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y);
        this.ctx.lineTo(x + width - radius, y);
        this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        this.ctx.lineTo(x + width, y + height - radius);
        this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        this.ctx.lineTo(x + radius, y + height);
        this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        this.ctx.lineTo(x, y + radius);
        this.ctx.quadraticCurveTo(x, y, x + radius, y);
        this.ctx.closePath();
        this.ctx.fill();

        // Reset shadow for border
        this.ctx.shadowColor = 'transparent';

        // Draw border if needed
        if (this.ctx.strokeStyle && this.ctx.lineWidth > 0) {
            this.ctx.stroke();
        }
    }

    drawText(bounds, content) {
        if (!content || !content.properties) return;

        const text = content.properties.text || '';
        const fontSize = content.properties.fontSize || 16;
        const fontFamily = content.properties.fontFamily || 'Inter, system-ui, sans-serif';
        const fontWeight = content.properties.fontWeight || '400';
        const textAlign = content.properties.textAlign || 'left';
        const color = content.properties.color || '#000000';

        // Enable subpixel rendering for better text quality
        this.ctx.textRenderingOptimization = 'optimizeQuality';
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';

        this.ctx.font = `${fontWeight} ${fontSize}px ${fontFamily}`;
        this.ctx.fillStyle = color;
        this.ctx.textAlign = textAlign;
        this.ctx.textBaseline = 'middle';

        // Add subtle text shadow for better readability (only if not in nested context)
        // Nested context shadows are already reset in renderNestedElements
        this.ctx.shadowColor = 'rgba(0, 0, 0, 0.1)';
        this.ctx.shadowBlur = 1;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;

        // Calculate text position within bounds
        let x = bounds.x;
        if (textAlign === 'center') {
            x = bounds.x + bounds.width / 2;
        } else if (textAlign === 'right') {
            x = bounds.x + bounds.width;
        }

        const y = bounds.y + bounds.height / 2;
        this.ctx.fillText(text, x, y);

        // Reset shadow
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
    }

    drawInputField(bounds, styles, content) {
        // Enable high quality rendering
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';

        // Draw background with subtle gradient
        if (styles.backgroundColor) {
            this.ctx.fillStyle = styles.backgroundColor;
            this.ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
        }

        // Add subtle gradient overlay for depth
        const gradient = this.ctx.createLinearGradient(
            bounds.x, bounds.y,
            bounds.x, bounds.y + bounds.height
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.02)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.02)');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);

        // Draw border with improved styling
        this.ctx.strokeStyle = styles.borderColor || '#d1d5db';
        this.ctx.lineWidth = styles.borderWidth || 1;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.strokeRect(bounds.x + 0.5, bounds.y + 0.5, bounds.width - 1, bounds.height - 1);

        // Draw placeholder text if no content
        if (content && content.properties && content.properties.placeholder) {
            const placeholderText = content.properties.placeholder;
            const fontSize = content.properties.fontSize || 16;
            const fontFamily = content.properties.fontFamily || 'Inter, system-ui, sans-serif';
            const placeholderColor = content.properties.placeholderColor || '#6b7280';

            this.ctx.textRenderingOptimization = 'optimizeQuality';
            this.ctx.font = `${fontSize}px ${fontFamily}`;
            this.ctx.fillStyle = placeholderColor;
            this.ctx.textAlign = 'left';
            this.ctx.textBaseline = 'middle';

            // Add slight text shadow for placeholder
            this.ctx.shadowColor = 'rgba(0, 0, 0, 0.05)';
            this.ctx.shadowBlur = 0.5;

            this.ctx.fillText(
                placeholderText,
                bounds.x + 16,
                bounds.y + bounds.height / 2
            );

            // Reset shadow
            this.ctx.shadowColor = 'transparent';
            this.ctx.shadowBlur = 0;
        }
    }

    drawButton(bounds, styles, content) {
        // Enable high quality rendering
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';

        // Draw button background with enhanced styling
        this.drawEnhancedButton(bounds, styles);

        // Draw text with improved quality
        if (content && content.properties) {
            const text = content.properties.text || '';
            const fontSize = content.properties.fontSize || 16;
            const fontFamily = content.properties.fontFamily || 'Inter, system-ui, sans-serif';
            const fontWeight = content.properties.fontWeight || '500';
            const color = content.properties.color || '#ffffff';

            // Enable subpixel rendering for better text quality
            this.ctx.textRenderingOptimization = 'optimizeQuality';
            this.ctx.font = `${fontWeight} ${fontSize}px ${fontFamily}`;
            this.ctx.fillStyle = color;
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';

            // Add subtle text shadow for better readability
            this.ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
            this.ctx.shadowBlur = 1;
            this.ctx.shadowOffsetX = 0;
            this.ctx.shadowOffsetY = 0.5;

            this.ctx.fillText(
                text,
                bounds.x + bounds.width / 2,
                bounds.y + bounds.height / 2
            );

            // Reset shadow
            this.ctx.shadowColor = 'transparent';
            this.ctx.shadowBlur = 0;
            this.ctx.shadowOffsetX = 0;
            this.ctx.shadowOffsetY = 0;
        }
    }

    drawEnhancedButton(bounds, styles) {
        const radius = styles.borderRadius || 8;
        const x = bounds.x;
        const y = bounds.y;
        const width = bounds.width;
        const height = bounds.height;

        // Create rounded rectangle path
        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y);
        this.ctx.lineTo(x + width - radius, y);
        this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        this.ctx.lineTo(x + width, y + height - radius);
        this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        this.ctx.lineTo(x + radius, y + height);
        this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        this.ctx.lineTo(x, y + radius);
        this.ctx.quadraticCurveTo(x, y, x + radius, y);
        this.ctx.closePath();

        // Apply button background color
        if (styles.backgroundColor) {
            this.ctx.fillStyle = styles.backgroundColor;
            this.ctx.fill();
        }

        // Add subtle gradient overlay for depth
        const gradient = this.ctx.createLinearGradient(
            x, y,
            x, y + height
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.1)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.1)');
        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // Draw button border if specified
        if (styles.borderColor && styles.borderWidth) {
            this.ctx.strokeStyle = styles.borderColor;
            this.ctx.lineWidth = styles.borderWidth;
            this.ctx.lineCap = 'round';
            this.ctx.lineJoin = 'round';
            this.ctx.stroke();
        }

        // Add subtle inner shadow for depth
        this.ctx.save();
        this.ctx.clip();
        this.ctx.shadowColor = 'rgba(0, 0, 0, 0.1)';
        this.ctx.shadowBlur = 4;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 2;

        // Draw inner shadow line
        this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y + height - 1);
        this.ctx.lineTo(x + width - radius, y + height - 1);
        this.ctx.stroke();
        this.ctx.restore();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CanvasRenderer;
}