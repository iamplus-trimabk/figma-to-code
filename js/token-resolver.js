/**
 * TokenResolver - Handles design token resolution with caching and fallbacks
 * Part of the SimFlo Design Format system
 */
class TokenResolver {
    constructor(designTokens, theme = 'light') {
        this.tokens = designTokens || {};
        this.theme = theme;
        this.cache = new Map();
        this.initializeCommonValues();
    }

    initializeCommonValues() {
        // Pre-resolve common values for performance
        this.commonValues = {
            spacing: {
                '3': 12,  // 12px
                '4': 16,  // 16px
                '6': 24,  // 24px
                '8': 32   // 32px
            },
            fontSize: {
                'base': 16,   // 16px
                'lg': 18,     // 18px
                'xl': 20,     // 20px
                '2xl': 24     // 24px
            },
            borderRadius: {
                'md': 8,     // 8px
                'lg': 12     // 12px
            }
        };
    }

    resolve(tokenPath) {
        // Check cache first
        if (this.cache.has(tokenPath)) {
            return this.cache.get(tokenPath);
        }

        const resolved = this.resolveTokenPath(tokenPath);

        // Cache the result
        this.cache.set(tokenPath, resolved);
        return resolved;
    }

    resolveTokenPath(tokenPath) {
        const parts = tokenPath.split('.');
        let current = this.tokens;

        for (const part of parts) {
            if (current && typeof current === 'object' && part in current) {
                current = current[part];
            } else {
                // Try common values fallback
                if (parts[0] === 'spacing' && this.commonValues.spacing[parts[1]]) {
                    return `${this.commonValues.spacing[parts[1]]}px`;
                }
                if (parts[0] === 'fontSize' && this.commonValues.fontSize[parts[1]]) {
                    return `${this.commonValues.fontSize[parts[1]]}px`;
                }
                if (parts[0] === 'borderRadius' && this.commonValues.borderRadius[parts[1]]) {
                    return `${this.commonValues.borderRadius[parts[1]]}px`;
                }

                console.warn(`Token not found: ${tokenPath}`);
                return tokenPath; // Return the original path as fallback
            }
        }

        return current;
    }

    parseDimension(value, parentDimension = 0) {
        if (typeof value === 'number') {
            return value;
        }

        if (typeof value === 'string') {
            // Handle pixel values
            if (value.endsWith('px')) {
                return parseFloat(value);
            }

            // Handle percentage values
            if (value.endsWith('%')) {
                const percentage = parseFloat(value) / 100;
                return parentDimension * percentage;
            }

            // Handle token references
            if (value.startsWith('spacing.') || value.startsWith('fontSize.') || value.startsWith('borderRadius.')) {
                const resolved = this.resolve(value);
                return this.parseDimension(resolved, parentDimension);
            }

            // Handle plain numbers (assume pixels)
            const numericValue = parseFloat(value);
            if (!isNaN(numericValue)) {
                return numericValue;
            }
        }

        console.warn(`Unable to parse dimension: ${value}`);
        return 0;
    }

    resolveColor(colorPath) {
        const color = this.resolve(colorPath);

        // Ensure color is in a usable format
        if (typeof color === 'string' && color.startsWith('#')) {
            return color;
        }

        // Fallback colors
        const fallbackColors = {
            'primary': '#6257db',
            'secondary': '#8b5cf6',
            'background': '#ffffff',
            'text': '#111827',
            'border': '#d1d5db'
        };

        return fallbackColors[color] || color || '#000000';
    }

    clearCache() {
        this.cache.clear();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TokenResolver;
}