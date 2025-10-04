# Figma REST API Guide for Design System Extraction

## Overview

This guide consolidates research on the Figma REST API approach for automated design system extraction. It provides a comprehensive resource for implementing production-ready tools that convert Figma designs into React/TypeScript + shadcn/ui + Tailwind CSS components.

## Quick Reference

### Official Documentation
- **Main REST API Docs**: https://developers.figma.com/docs/rest-api/
- **API Specification**: https://github.com/figma/rest-api-spec
- **API Demo Project**: https://github.com/figma/figma-api-demo/tree/master/figma-to-react

### Core Architecture
```
Figma File → REST API → JSON Cache → Design Tokens → React Components
```

## 1. API Fundamentals

### Base Configuration
```typescript
interface FigmaAPIConfig {
  baseURL: 'https://api.figma.com/v1';
  version: '1.0';
  authentication: 'Personal Access Token';
  rateLimit: {
    requestsPerHour: 3600; // Standard tier
    requestsPerMinute: 60;
  };
}
```

### Authentication

#### Personal Access Token
```typescript
class PersonalTokenAuth {
  constructor(private accessToken: string) {}

  getHeaders(): Record<string, string> {
    return {
      'X-Figma-Token': this.accessToken,
      'Content-Type': 'application/json'
    };
  }

  async validateToken(): Promise<boolean> {
    try {
      const response = await fetch('https://api.figma.com/v1/me', {
        headers: this.getHeaders()
      });
      return response.ok;
    } catch {
      return false;
    }
  }
}
```

#### Personal Access Token Best Practices

1. **Token Generation**: Create tokens in Figma Settings → Account → Personal Access Tokens
2. **Scopes**: Only request necessary permissions for your use case
3. **Security**:
   - Never commit tokens to version control
   - Store tokens securely using environment variables or secret management
   - Use different tokens for different environments
   - Rotate tokens regularly
4. **Rate Limits**: Standard accounts have 3600 requests/hour
5. **Validation**: Always validate tokens before use

Example usage:
```python
# Python example (like our simple_figma_cache.py)
ACCESS_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN')  # Use environment variables
headers = {'X-Figma-Token': ACCESS_TOKEN}
```

## 2. Core API Endpoints

### File Access & Analysis
```typescript
// Primary file endpoint
interface GetFileOptions {
  geometry?: 'paths'; // Include vector data
  ids?: string[];     // Specific node IDs to include
  version?: number;   // Specific version
  depth?: number;     // Node depth (0-2)
}

// Get file structure
GET /v1/files/:file_key

// Get specific nodes only
GET /v1/files/:file_key/nodes?ids=nodeId1,nodeId2

// Export images
GET /v1/images/:file_key?ids=nodeId1,nodeId2&format=PNG&scale=2

// Get file comments
GET /v1/files/:file_key/comments

// Get components
GET /v1/files/:file_key/components
```

### File Structure Response
```typescript
interface FigmaFile {
  name: string;
  lastModified: string;
  thumbnailUrl: string;
  version: number;
  document: DocumentNode;
  schemaVersion: number;
  styles: {
    [key: string]: Style;
  };
  components: {
    [key: string]: Component;
  };
}

interface DocumentNode extends SceneNode {
  type: 'DOCUMENT';
  children: readonly PageNode[];
}
```

## 3. Design Token Extraction

### Color System Extraction
```typescript
class ColorExtractor {
  async extractColorPalette(file: FigmaFile): Promise<ColorPalette> {
    const paintStyles = this.extractPaintStyles(file.styles);
    const colorUsage = this.analyzeColorUsage(file.document);

    return {
      semantic: this.categorizeColors(paintStyles, 'semantic'),
      neutral: this.categorizeColors(paintStyles, 'neutral'),
      brand: this.categorizeColors(paintStyles, 'brand'),
      feedback: this.categorizeColors(paintStyles, 'feedback'),
      usage: colorUsage,
      palette: this.generateColorPalette(paintStyles)
    };
  }

  private categorizeColors(styles: PaintStyle[], category: string): Record<string, string> {
    const colors: Record<string, string> = {};

    styles.forEach(style => {
      if (style.style_type === 'FILL') {
        const color = this.extractPrimaryColor(style.fills);
        if (color) {
          const tokenName = this.toTokenName(style.name);
          colors[tokenName] = color;
        }
      }
    });

    return colors;
  }

  private extractPrimaryColor(fills: readonly Paint[]): string | null {
    const solidFill = fills.find(fill => fill.type === 'SOLID');
    if (!solidFill || solidFill.type !== 'SOLID') return null;

    const { r, g, b } = solidFill.color;
    return `#${Math.round(r * 255).toString(16).padStart(2, '0')}${Math.round(g * 255).toString(16).padStart(2, '0')}${Math.round(b * 255).toString(16).padStart(2, '0')}`;
  }

  private toTokenName(styleName: string): string {
    return styleName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  }
}
```

### Typography System Extraction
```typescript
class TypographyExtractor {
  async extractTypographySystem(file: FigmaFile): Promise<TypographySystem> {
    const textStyles = this.extractTextStyles(file.styles);
    const fontUsage = this.analyzeFontUsage(file.document);

    return {
      fontFamilies: this.extractFontFamilies(textStyles),
      fontSizes: this.extractFontSizes(textStyles),
      fontWeights: this.extractFontWeights(textStyles),
      lineHeights: this.extractLineHeights(textStyles),
      letterSpacing: this.extractLetterSpacing(textStyles),
      hierarchy: this.buildTypographyHierarchy(textStyles),
      usage: fontUsage
    };
  }

  private extractTextStyles(styles: Record<string, Style>): TextStyle[] {
    return Object.values(styles)
      .filter(style => style.style_type === 'TEXT')
      .map(style => style as TextStyle);
  }

  private buildTypographyHierarchy(textStyles: TextStyle[]): TypographyHierarchy {
    const hierarchy: TypographyHierarchy = {
      heading: {},
      subheading: {},
      body: {},
      caption: {},
      button: {}
    };

    textStyles.forEach(style => {
      const fontSize = style.fontSize;
      const fontWeight = style.fontWeight;
      const tokenName = this.toTokenName(style.name);

      if (fontSize >= 32) {
        hierarchy.heading[tokenName] = {
          fontSize,
          fontWeight,
          fontFamily: style.fontName.family,
          lineHeight: this.parseLineHeight(style.lineHeight)
        };
      } else if (fontSize >= 20) {
        hierarchy.subheading[tokenName] = {
          fontSize,
          fontWeight,
          fontFamily: style.fontName.family,
          lineHeight: this.parseLineHeight(style.lineHeight)
        };
      } else if (fontSize >= 16) {
        hierarchy.body[tokenName] = {
          fontSize,
          fontWeight,
          fontFamily: style.fontName.family,
          lineHeight: this.parseLineHeight(style.lineHeight)
        };
      } else {
        hierarchy.caption[tokenName] = {
          fontSize,
          fontWeight,
          fontFamily: style.fontName.family,
          lineHeight: this.parseLineHeight(style.lineHeight)
        };
      }
    });

    return hierarchy;
  }
}
```

### Spacing System Extraction
```typescript
class SpacingExtractor {
  async extractSpacingSystem(file: FigmaFile): Promise<SpacingSystem> {
    const spacingAnalysis = this.analyzeSpacingUsage(file.document);

    return {
      baseUnit: this.determineBaseUnit(spacingAnalysis),
      scale: this.generateSpacingScale(spacingAnalysis),
      semantic: this.categorizeSemanticSpacing(spacingAnalysis),
      usage: spacingAnalysis
    };
  }

  private analyzeSpacingUsage(document: DocumentNode): SpacingAnalysis {
    const spacingValues: number[] = [];

    const traverse = (node: SceneNode) => {
      if ('absoluteBoundingBox' in node && 'children' in node && node.children.length > 1) {
        // Analyze spacing between siblings
        for (let i = 1; i < node.children.length; i++) {
          const prev = node.children[i - 1].absoluteBoundingBox;
          const curr = node.children[i].absoluteBoundingBox;

          if (prev && curr) {
            const spacing = curr.y - (prev.y + prev.height);
            if (spacing > 0 && spacing < 200) { // Reasonable spacing range
              spacingValues.push(spacing);
            }
          }
        }
      }

      if ('children' in node) {
        node.children.forEach(traverse);
      }
    };

    document.children.forEach(traverse);

    return {
      values: spacingValues,
      commonValues: this.findCommonSpacingValues(spacingValues),
      patterns: this.identifySpacingPatterns(spacingValues)
    };
  }

  private generateSpacingScale(analysis: SpacingAnalysis): SpacingScale {
    const baseUnit = this.determineBaseUnit(analysis);
    const scale: SpacingScale = {};

    // Generate scale from base unit
    for (let i = 0; i <= 10; i++) {
      scale[`spacing-${i}`] = baseUnit * i;
    }

    // Add semantic spacing based on common values
    analysis.commonValues.forEach(value => {
      const semanticName = this.inferSemanticSpacing(value);
      if (semanticName) {
        scale[semanticName] = value;
      }
    });

    return scale;
  }
}
```

## 4. Component Analysis & Extraction

### Component Detection
```typescript
class ComponentAnalyzer {
  async analyzeComponents(file: FigmaFile): Promise<ComponentAnalysis> {
    return {
      components: this.extractAllComponents(file.document),
      componentSets: this.extractComponentSets(file.document),
      variants: this.analyzeComponentVariants(file.document),
      instances: this.findComponentInstances(file.document),
      dependencies: this.analyzeComponentDependencies(file.document)
    };
  }

  private extractAllComponents(document: DocumentNode): ComponentInfo[] {
    const components: ComponentInfo[] = [];

    const traverse = (node: SceneNode, path: string[] = []) => {
      if (node.type === 'COMPONENT') {
        const component = this.analyzeComponent(node as ComponentNode);
        component.path = path;
        components.push(component);
      } else if (node.type === 'COMPONENT_SET') {
        const componentSet = this.analyzeComponentSet(node as ComponentSetNode);
        componentSet.path = path;
        components.push(...componentSet.components);
      }

      if ('children' in node) {
        node.children.forEach(child => traverse(child, [...path, node.name]));
      }
    };

    document.children.forEach(page => traverse(page));
    return components;
  }

  private analyzeComponent(component: ComponentNode): ComponentInfo {
    return {
      id: component.id,
      name: component.name,
      description: component.description,
      type: 'component',
      properties: this.extractComponentProperties(component),
      children: this.analyzeComponentChildren(component),
      styles: this.extractComponentStyles(component),
      constraints: this.extractConstraints(component),
      autoLayout: this.extractAutoLayout(component),
      instances: [], // Will be populated separately
      variants: []
    };
  }

  private categorizeComponent(component: ComponentInfo): ComponentCategory {
    const name = component.name.toLowerCase();

    if (name.includes('button')) return 'button';
    if (name.includes('input') || name.includes('field')) return 'input';
    if (name.includes('card')) return 'card';
    if (name.includes('modal') || name.includes('dialog')) return 'modal';
    if (name.includes('navigation') || name.includes('nav')) return 'navigation';
    if (name.includes('header')) return 'header';
    if (name.includes('footer')) return 'footer';
    if (name.includes('sidebar')) return 'sidebar';

    return 'generic';
  }
}
```

### Component Specification Generation
```typescript
class ComponentSpecGenerator {
  generateComponentSpec(
    component: ComponentInfo,
    styles: StyleCollection
  ): ComponentSpecification {
    return {
      name: component.name,
      description: component.description,
      category: this.categorizeComponent(component),
      props: this.extractPropsFromComponent(component),
      variants: component.variants.map(variant => ({
        name: variant.name,
        props: this.extractPropsFromVariant(variant),
        styles: this.mapStylesToDesignTokens(variant, styles),
        interactions: this.extractInteractions(variant)
      })),
      accessibility: this.analyzeAccessibility(component),
      responsive: this.analyzeResponsiveBehavior(component),
      dependencies: this.analyzeComponentDependencies(component)
    };
  }

  private extractPropsFromComponent(component: ComponentInfo): ComponentProps {
    const props: ComponentProps = {
      className: { type: 'string', required: false },
      children: { type: 'ReactNode', required: false },
      disabled: { type: 'boolean', required: false }
    };

    // Extract props from component properties
    Object.entries(component.properties).forEach(([key, prop]) => {
      props[this.toPropName(key)] = {
        type: this.mapPropertyType(prop.type),
        required: prop.defaultValue === undefined,
        default: prop.defaultValue
      };
    });

    return props;
  }

  private mapStylesToDesignTokens(
    component: ComponentInfo,
    styles: StyleCollection
  ): StyleMapping {
    return {
      colors: this.mapColorStyles(component, styles),
      typography: this.mapTypographyStyles(component, styles),
      spacing: this.mapSpacingStyles(component, styles),
      effects: this.mapEffectStyles(component, styles)
    };
  }
}
```

## 5. Production Implementation

### Rate Limiting
```typescript
class RateLimiter {
  private requests: number[] = [];
  private readonly MAX_REQUESTS_PER_HOUR = 3600;
  private readonly MAX_REQUESTS_PER_MINUTE = 60;

  async executeRequest<T>(requestFn: () => Promise<T>): Promise<T> {
    await this.waitForAvailableSlot();

    try {
      const result = await requestFn();
      this.recordRequest();
      return result;
    } catch (error: any) {
      if (error.status === 429) {
        await this.handleRateLimitExceeded(error);
        return this.executeRequest(requestFn);
      }
      throw error;
    }
  }

  private async waitForAvailableSlot(): Promise<void> {
    const now = Date.now();

    // Clean old requests
    this.requests = this.requests.filter(time => now - time < 60 * 60 * 1000);

    // Check hourly limit
    if (this.requests.length >= this.MAX_REQUESTS_PER_HOUR) {
      const oldestRequest = Math.min(...this.requests);
      const waitTime = 60 * 60 * 1000 - (now - oldestRequest);
      console.log(`Hourly rate limit reached, waiting ${waitTime / 1000} seconds`);
      await this.delay(waitTime);
    }

    // Check minute limit
    const recentRequests = this.requests.filter(time => now - time < 60 * 1000);
    if (recentRequests.length >= this.MAX_REQUESTS_PER_MINUTE) {
      const waitTime = 60 * 1000 - (now - Math.min(...recentRequests));
      console.log(`Minute rate limit reached, waiting ${waitTime / 1000} seconds`);
      await this.delay(waitTime);
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private recordRequest(): void {
    this.requests.push(Date.now());
  }
}
```

### Caching Strategy
```typescript
class FigmaCacheManager {
  private memoryCache = new Map<string, CacheEntry>();
  private persistentCache?: PersistentCache;

  constructor(persistentCache?: PersistentCache) {
    this.persistentCache = persistentCache;
  }

  async get<T>(key: string): Promise<T | null> {
    // Check memory cache first
    const memoryEntry = this.memoryCache.get(key);
    if (memoryEntry && !this.isExpired(memoryEntry)) {
      return memoryEntry.data;
    }

    // Check persistent cache
    if (this.persistentCache) {
      const persistentEntry = await this.persistentCache.get(key);
      if (persistentEntry && !this.isExpired(persistentEntry)) {
        // Load into memory cache
        this.memoryCache.set(key, persistentEntry);
        return persistentEntry.data;
      }
    }

    return null;
  }

  async set<T>(key: string, data: T, ttl: number = 300000): Promise<void> {
    const entry: CacheEntry = {
      data,
      timestamp: Date.now(),
      ttl
    };

    // Set in memory cache
    this.memoryCache.set(key, entry);

    // Set in persistent cache
    if (this.persistentCache) {
      await this.persistentCache.set(key, entry);
    }
  }

  private isExpired(entry: CacheEntry): boolean {
    return Date.now() - entry.timestamp > entry.ttl;
  }
}
```

### Error Handling
```typescript
class ResilientFigmaClient {
  private readonly MAX_RETRIES = 3;
  private readonly RETRY_DELAY = 1000;

  async getFileWithRetry(
    fileKey: string,
    options?: GetFileOptions,
    retries: number = 0
  ): Promise<FigmaFile> {
    try {
      return await this.apiClient.getFile(fileKey, options);
    } catch (error: any) {
      if (this.shouldRetry(error) && retries < this.MAX_RETRIES) {
        console.log(`Retrying request (attempt ${retries + 1}/${this.MAX_RETRIES})`);
        await this.delay(this.RETRY_DELAY * Math.pow(2, retries)); // Exponential backoff
        return this.getFileWithRetry(fileKey, options, retries + 1);
      }
      throw error;
    }
  }

  private shouldRetry(error: any): boolean {
    return (
      error.code === 'ECONNRESET' ||
      error.code === 'ETIMEDOUT' ||
      error.status === 429 ||
      error.status >= 500
    );
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## 6. Code Generation

### React Component Generation
```typescript
class ReactComponentGenerator {
  generateComponent(spec: ComponentSpecification): string {
    const props = this.generatePropsInterface(spec);
    const styles = this.generateStyles(spec);
    const componentLogic = this.generateComponentLogic(spec);

    return `
import React from 'react';
import { cn } from '@/lib/utils';

${props}

export const ${spec.name}: React.FC<${spec.name}Props> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div
      className={cn(
        ${styles}
        className
      )}
      {...props}
    >
      ${componentLogic}
    </div>
  );
};
`;
  }

  private generatePropsInterface(spec: ComponentSpecification): string {
    const props = Object.entries(spec.props)
      .map(([name, prop]) => {
        const optional = prop.required ? '' : '?';
        return `  ${name}${optional}: ${prop.type};`;
      })
      .join('\n');

    return `interface ${spec.name}Props extends React.HTMLAttributes<HTMLDivElement> {
${props}
}`;
  }

  private generateStyles(spec: ComponentSpecification): string {
    const styles = Object.entries(spec.styles.colors)
      .map(([token, value]) => `'bg-${token}': '${value}'`)
      .join(',\n        ');

    return `{
      ${styles}
    }`;
  }
}
```

### Tailwind Configuration Generation
```typescript
class TailwindConfigGenerator {
  generateConfig(designTokens: DesignTokenSet): string {
    const colors = this.generateColorsConfig(designTokens.colors);
    const fontFamily = this.generateFontFamilyConfig(designTokens.typography);
    const fontSize = this.generateFontSizeConfig(designTokens.typography);

    return `/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
${colors}
      },
      fontFamily: {
${fontFamily}
      },
      fontSize: {
${fontSize}
      }
    }
  },
  plugins: [],
}`;
  }

  private generateColorsConfig(colors: ColorTokens): string {
    const configs: string[] = [];

    Object.entries(colors.semantic).forEach(([name, value]) => {
      configs.push(`        '${name}': '${value}',`);
    });

    Object.entries(colors.neutral).forEach(([name, value]) => {
      configs.push(`        '${name}': '${value}',`);
    });

    return configs.join('\n');
  }

  private generateFontFamilyConfig(typography: TypographyTokens): string {
    const fontFamilies = new Set<string>();

    Object.values(typography).forEach(style => {
      fontFamilies.add(style.fontFamily);
    });

    return Array.from(fontFamilies)
      .map(font => `        '${font.toLowerCase().replace(' ', '-')}': ['${font}'],`)
      .join('\n');
  }
}
```

## 7. Our Implementation Architecture

### Main Extractor Class
```typescript
class FigmaRESTExtractor {
  private apiClient: ResilientFigmaClient;
  private cache: FigmaCacheManager;
  private rateLimiter: RateLimiter;
  private colorExtractor: ColorExtractor;
  private typographyExtractor: TypographyExtractor;
  private spacingExtractor: SpacingExtractor;
  private componentAnalyzer: ComponentAnalyzer;

  constructor(accessToken: string) {
    this.apiClient = new ResilientFigmaClient(accessToken);
    this.cache = new FigmaCacheManager();
    this.rateLimiter = new RateLimiter();
    this.colorExtractor = new ColorExtractor();
    this.typographyExtractor = new TypographyExtractor();
    this.spacingExtractor = new SpacingExtractor();
    this.componentAnalyzer = new ComponentAnalyzer();
  }

  async extractDesignSystem(fileKey: string): Promise<DesignSystemExtraction> {
    // Get file structure with caching
    const file = await this.getFileWithCache(fileKey, { depth: 2 });

    // Extract design tokens
    const colors = await this.colorExtractor.extractColorPalette(file);
    const typography = await this.typographyExtractor.extractTypographySystem(file);
    const spacing = await this.spacingExtractor.extractSpacingSystem(file);

    // Analyze components
    const components = await this.componentAnalyzer.analyzeComponents(file);

    // Generate output files
    const output = {
      designTokens: {
        colors,
        typography,
        spacing
      },
      components,
      metadata: this.extractMetadata(file)
    };

    return output;
  }

  private async getFileWithCache(fileKey: string, options?: GetFileOptions): Promise<FigmaFile> {
    const cacheKey = this.generateCacheKey(fileKey, options);

    // Try cache first
    const cached = await this.cache.get<FigmaFile>(cacheKey);
    if (cached) {
      console.log('Cache hit for file:', fileKey);
      return cached;
    }

    // Fetch from API
    console.log('Cache miss, fetching from API:', fileKey);
    const file = await this.rateLimiter.executeRequest(() =>
      this.apiClient.getFileWithRetry(fileKey, options)
    );

    // Cache the result
    await this.cache.set(cacheKey, file, 5 * 60 * 1000); // 5 minutes

    return file;
  }
}
```

### Integration with Our Current Workflow
```typescript
// Integration with our existing simple cache approach
class DesignSystemExtractor {
  async extractFromCachedJSON(jsonPath: string): Promise<void> {
    // Load cached JSON from our simple cache script
    const figmaData = JSON.parse(await fs.readFile(jsonPath, 'utf8'));

    // Extract design tokens
    const colors = this.extractColorsFromJSON(figmaData);
    const typography = this.extractTypographyFromJSON(figmaData);
    const components = this.extractComponentsFromJSON(figmaData);

    // Generate output files
    await this.generateCSSVariables(colors);
    await this.generateTailwindConfig(colors, typography);
    await this.generateReactComponents(components);

    console.log('✅ Design system extraction complete!');
  }

  private extractColorsFromJSON(figmaData: any): ColorPalette {
    const colors = new Set<string>();

    const extractFromNode = (node: any) => {
      // Extract from fills
      if (node.fills) {
        node.fills.forEach((fill: any) => {
          if (fill.type === 'SOLID' && fill.color) {
            const hex = this.rgbToHex(fill.color);
            colors.add(hex);
          }
        });
      }

      // Extract from strokes
      if (node.strokes) {
        node.strokes.forEach((stroke: any) => {
          if (stroke.type === 'SOLID' && stroke.color) {
            const hex = this.rgbToHex(stroke.color);
            colors.add(hex);
          }
        });
      }

      // Recursively check children
      if (node.children) {
        node.children.forEach(extractFromNode);
      }
    };

    extractFromNode(figmaData.document);
    return this.categorizeColors(Array.from(colors));
  }
}
```

## 8. Best Practices

### Performance Optimization
- Use intelligent caching with appropriate TTL
- Implement batch processing for large files
- Optimize request patterns to minimize API calls
- Use compression for large data transfers
- Implement proper error handling and retry logic

### Security Considerations
- Store access tokens securely
- Use HTTPS for all API communications
- Validate and sanitize all API responses
- Keep access tokens private and never commit them to version control

### Monitoring & Observability
- Track API usage and rate limits
- Monitor cache hit/miss ratios
- Log extraction times and success rates
- Implement proper error tracking
- Set up alerts for API failures

## 9. Complete Workflow Example

```typescript
// Complete end-to-end workflow
async function completeWorkflow(fileKey: string, accessToken: string): Promise<void> {
  console.log('🚀 Starting Figma design system extraction...');

  try {
    // Step 1: Initialize extractor
    const extractor = new FigmaRESTExtractor(accessToken);

    // Step 2: Extract design system
    const designSystem = await extractor.extractDesignSystem(fileKey);

    // Step 3: Generate output files
    const outputDir = path.join(process.cwd(), 'design_system_output');
    await fs.ensureDir(outputDir);

    // Generate CSS variables
    await generateCSSVariables(designSystem.designTokens.colors, outputDir);

    // Generate Tailwind config
    await generateTailwindConfig(designSystem.designTokens, outputDir);

    // Generate React components
    await generateReactComponents(designSystem.components, outputDir);

    // Generate design tokens JSON
    await generateDesignTokensJSON(designSystem.designTokens, outputDir);

    console.log(`✅ Design system extraction complete! Output saved to: ${outputDir}`);
    console.log(`📊 Extracted ${Object.keys(designSystem.designTokens.colors).length} colors`);
    console.log(`📝 Extracted ${Object.keys(designSystem.designTokens.typography).length} typography styles`);
    console.log(`🧩 Extracted ${designSystem.components.length} components`);

  } catch (error) {
    console.error('❌ Extraction failed:', error);
    throw error;
  }
}
```

## 10. Limitations & Considerations

### API Limitations
- **Rate Limiting**: 3600 requests/hour for standard tier
- **File Size**: Large files may require batch processing
- **Real-time Updates**: No real-time change notifications
- **Write Access**: Limited write capabilities

### Data Constraints
- **Vector Data**: Must be explicitly requested with `geometry: 'paths'`
- **Image Export**: Requires separate API calls
- **Component Instances**: Limited instance relationship data
- **Version History**: Limited version access

### Performance Considerations
- **Network Latency**: API calls depend on network speed
- **Large Files**: May require significant processing time
- **Concurrent Requests**: Need careful rate limit management
- **Memory Usage**: Large design files can consume significant memory

## Conclusion

The Figma REST API provides a robust, well-documented foundation for automated design system extraction. When combined with our caching approach and code generation patterns, it offers a complete solution for converting Figma designs into production-ready React components.

**Key Advantages**:
- Comprehensive data access
- Reliable and well-documented
- TypeScript support
- No browser automation complexity
- Good performance for structured data

**Best Use Cases**:
- Primary data extraction method
- Large file processing with batching
- Design token and style extraction
- Component analysis and cataloging

**Recommendation**: Use the REST API as the primary extraction method, supplemented by local caching for offline processing and performance optimization.

---

## Official Reference Links

For the most up-to-date and comprehensive information, refer to these official sources:

- **Main REST API Documentation**: https://developers.figma.com/docs/rest-api/
- **API Specification**: https://github.com/figma/rest-api-spec
- **Official Demo Project**: https://github.com/figma/figma-api-demo/tree/master/figma-to-react
- **Personal Access Token Guide**: https://developers.figma.com/docs/rest-api/authentication/
- **Rate Limiting**: https://developers.figma.com/docs/rest-api/rate-limits/

*This guide consolidates research from multiple sources and provides practical implementation patterns for production-ready design system extraction.*