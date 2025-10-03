# Figma REST API Research
## Repository: https://github.com/figma/rest-api-spec

## Overview
The Figma REST API provides comprehensive HTTP-based access to Figma documents, components, styles, and design assets. It offers a well-documented, reliable interface for programmatic design data extraction, making it an excellent foundation for automated design system extraction tools. The API is based on OpenAPI specifications and includes TypeScript definitions for type-safe development.

## API Architecture & Capabilities

### Core API Structure
```typescript
// Base API configuration
interface FigmaAPIConfig {
  baseURL: 'https://api.figma.com/v1';
  version: '1.0';
  authentication: 'OAuth2' | 'Personal Access Token';
  rateLimit: {
    requestsPerHour: 3600; // Standard tier
    requestsPerMinute: 60;
  };
}

// Main API client structure
class FigmaAPIClient {
  private accessToken: string;
  private baseURL: string;

  constructor(accessToken: string) {
    this.accessToken = accessToken;
    this.baseURL = 'https://api.figma.com/v1';
  }

  // Core API methods
  async getFile(fileKey: string, options?: GetFileOptions): Promise<FigmaFile>;
  async getFileNodes(fileKey: string, ids: string[]): Promise<FigmaNodes>;
  async getImages(fileKey: string, ids: string[], format: ExportFormat): Promise<ImageUrls>;
  async getComments(fileKey: string): Promise<Comment[]>;
  async getComponents(fileKey: string): Promise<Component[]>;
  async getComponentSet(componentSetId: string): Promise<ComponentSet>;
}
```

### Authentication Methods
```typescript
// OAuth2 Authentication Flow
interface OAuth2Config {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  scopes: ('file_read' | 'file_write' | 'webhooks')[];
}

class OAuth2Authenticator {
  async getAuthorizationUrl(config: OAuth2Config): Promise<string> {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: config.clientId,
      redirect_uri: config.redirectUri,
      scope: config.scopes.join(' '),
      state: this.generateState()
    });

    return `https://www.figma.com/oauth?${params.toString()}`;
  }

  async exchangeCodeForToken(code: string, config: OAuth2Config): Promise<OAuth2Token> {
    const response = await fetch('https://www.figma.com/api/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        client_id: config.clientId,
        client_secret: config.clientSecret,
        code,
        redirect_uri: config.redirectUri,
        grant_type: 'authorization_code'
      })
    });

    return response.json();
  }
}

// Personal Access Token Authentication
class TokenAuthenticator {
  constructor(private accessToken: string) {}

  getAuthHeaders(): Record<string, string> {
    return {
      'X-Figma-Token': this.accessToken
    };
  }
}
```

## Core API Endpoints & Capabilities

### 1. **File Access & Analysis**
```typescript
// Primary file endpoint
interface GetFileOptions {
  geometry?: 'paths'; // Include vector data
  ids?: string[];     // Specific node IDs to include
  version?: number;   // Specific version
  depth?: number;     // Node depth (0-2)
}

class FileAnalyzer {
  async analyzeFile(fileKey: string, options?: GetFileOptions): Promise<FileAnalysis> {
    const response = await this.apiClient.getFile(fileKey, {
      geometry: 'paths',
      depth: 2,
      ...options
    });

    return {
      document: response.document,
      components: this.extractComponents(response.document),
      styles: this.extractStyles(response.document),
      canvas: this.extractCanvasInfo(response.document),
      metadata: {
        name: response.name,
        lastModified: response.lastModified,
        thumbnailUrl: response.thumbnailUrl,
        version: response.version
      }
    };
  }

  private extractComponents(document: DocumentNode): ComponentInfo[] {
    const components: ComponentInfo[] = [];

    const traverse = (node: SceneNode) => {
      if (node.type === 'COMPONENT' || node.type === 'COMPONENT_SET') {
        components.push({
          id: node.id,
          name: node.name,
          type: node.type,
          description: node.description,
          componentProperties: (node as ComponentNode).componentProperties,
          backgroundColor: this.extractBackgroundColor(node),
          boundingBox: node.absoluteBoundingBox
        });
      }

      if ('children' in node) {
        node.children.forEach(traverse);
      }
    };

    document.children.forEach(traverse);
    return components;
  }

  private extractStyles(document: DocumentNode): StyleInfo[] {
    return {
      text: this.extractTextStyles(document),
      paint: this.extractPaintStyles(document),
      effect: this.extractEffectStyles(document),
      grid: this.extractGridStyles(document)
    };
  }
}
```

### 2. **Node Retrieval & Analysis**
```typescript
// Specific node extraction
class NodeAnalyzer {
  async getSpecificNodes(fileKey: string, nodeIds: string[]): Promise<NodeAnalysis> {
    const response = await this.apiClient.getFileNodes(fileKey, nodeIds);

    return {
      nodes: this.analyzeNodes(response.nodes),
      relationships: this.analyzeRelationships(response.nodes),
      dependencies: this.analyzeDependencies(response.nodes)
    };
  }

  private analyzeNodes(nodes: Record<string, SceneNode>): DetailedNodeInfo[] {
    return Object.entries(nodes).map(([id, node]) => ({
      id,
      name: node.name,
      type: node.type,
      visible: node.visible,
      locked: node.locked,
      componentProperties: this.extractComponentProperties(node),
      styles: this.extractNodeStyles(node),
      geometry: this.extractGeometry(node),
      children: this.extractChildren(node),
      parent: this.extractParentInfo(node)
    }));
  }

  private extractNodeStyles(node: SceneNode): NodeStyles {
    return {
      fills: this.extractFills(node),
      strokes: this.extractStrokes(node),
      effects: this.extractEffects(node),
      textStyle: this.extractTextStyle(node),
      layoutStyle: this.extractLayoutStyle(node)
    };
  }
}
```

### 3. **Image Export & Rendering**
```typescript
// Image and asset export
class ImageExporter {
  async exportImages(
    fileKey: string,
    nodeIds: string[],
    format: ExportFormat = 'PNG',
    scale: number = 1
  ): Promise<ExportResult> {
    const response = await this.apiClient.getImages(fileKey, nodeIds, {
      format,
      scale,
      include_id: true
    });

    return {
      images: response.images,
      metadata: {
        format,
        scale,
        totalCount: nodeIds.length,
        exportedCount: Object.keys(response.images).length
      }
    };
  }

  async exportComponentSet(
    fileKey: string,
    componentSetId: string,
    options: ExportOptions
  ): Promise<ComponentSetExport> {
    // Get component set details
    const componentSet = await this.apiClient.getComponentSet(componentSetId);

    // Extract all component node IDs
    const componentIds = componentSet.components.map(comp => comp.node_id);

    // Export all components
    const images = await this.exportImages(fileKey, componentIds, options.format, options.scale);

    return {
      componentSet,
      images,
      exportManifest: this.createExportManifest(componentSet, images)
    };
  }

  private createExportManifest(
    componentSet: ComponentSet,
    images: ImageUrls
  ): ExportManifest {
    return {
      name: componentSet.name,
      description: componentSet.description,
      components: componentSet.components.map(comp => ({
        id: comp.node_id,
        name: comp.name,
        description: comp.description,
        imageUrl: images.images[comp.node_id],
        variants: this.extractVariants(comp)
      })),
      exportedAt: new Date().toISOString(),
      totalComponents: componentSet.components.length
    };
  }
}
```

### 4. **Style & Design Token Extraction**
```typescript
// Style system extraction
class StyleExtractor {
  async extractDesignSystem(fileKey: string): Promise<DesignSystem> {
    const file = await this.apiClient.getFile(fileKey, { depth: 2 });

    return {
      colors: await this.extractColorSystem(file),
      typography: await this.extractTypographySystem(file),
      spacing: await this.extractSpacingSystem(file),
      effects: await this.extractEffectSystem(file),
      components: await this.extractComponentSystem(file)
    };
  }

  private async extractColorSystem(file: FigmaFile): Promise<ColorSystem> {
    const paintStyles = this.extractPaintStyles(file.document);
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

  private async extractTypographySystem(file: FigmaFile): Promise<TypographySystem> {
    const textStyles = this.extractTextStyles(file.document);
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

  private async extractSpacingSystem(file: FigmaFile): Promise<SpacingSystem> {
    const spacingAnalysis = this.analyzeSpacingUsage(file.document);

    return {
      baseUnit: this.determineBaseUnit(spacingAnalysis),
      scale: this.generateSpacingScale(spacingAnalysis),
      semantic: this.categorizeSemanticSpacing(spacingAnalysis),
      usage: spacingAnalysis
    };
  }
}
```

### 5. **Component Analysis & Extraction**
```typescript
// Advanced component analysis
class ComponentAnalyzer {
  async analyzeComponents(fileKey: string): Promise<ComponentAnalysis> {
    const file = await this.apiClient.getFile(fileKey, { depth: 2 });

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

  private analyzeComponentVariants(document: DocumentNode): ComponentVariant[] {
    const variants: ComponentVariant[] = [];

    // Find component sets and extract variants
    const traverse = (node: SceneNode) => {
      if (node.type === 'COMPONENT_SET') {
        const componentSet = node as ComponentSetNode;
        const setVariants = this.extractComponentSetVariants(componentSet);
        variants.push(...setVariants);
      }

      if ('children' in node) {
        node.children.forEach(traverse);
      }
    };

    document.children.forEach(traverse);
    return variants;
  }
}
```

## Advanced API Usage Patterns

### 1. **Batch Processing & Optimization**
```typescript
// Efficient batch processing
class BatchProcessor {
  private readonly MAX_IDS_PER_REQUEST = 100;
  private readonly RATE_LIMIT_DELAY = 1000; // 1 second between requests

  async processLargeFile(fileKey: string): Promise<BatchProcessingResult> {
    // Get file structure first
    const file = await this.apiClient.getFile(fileKey, { depth: 0 });
    const allNodeIds = this.extractAllNodeIds(file.document);

    // Process in batches
    const batches = this.createBatches(allNodeIds, this.MAX_IDS_PER_REQUEST);
    const results: ProcessingResult[] = [];

    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      console.log(`Processing batch ${i + 1}/${batches.length}`);

      try {
        const batchResult = await this.processBatch(fileKey, batch);
        results.push(batchResult);

        // Rate limiting
        if (i < batches.length - 1) {
          await this.delay(this.RATE_LIMIT_DELAY);
        }
      } catch (error) {
        console.error(`Batch ${i + 1} failed:`, error);
        results.push({ batch, error, success: false });
      }
    }

    return this.consolidateResults(results);
  }

  private async processBatch(fileKey: string, nodeIds: string[]): Promise<ProcessingResult> {
    const nodesResponse = await this.apiClient.getFileNodes(fileKey, nodeIds);
    const imagesResponse = await this.apiClient.getImages(fileKey, nodeIds, 'PNG', 2);

    return {
      nodes: nodesResponse.nodes,
      images: imagesResponse.images,
      success: true
    };
  }

  private createBatches<T>(items: T[], batchSize: number): T[][] {
    const batches: T[][] = [];
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }
    return batches;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 2. **Caching & Performance**
```typescript
// Intelligent caching system
class FigmaAPICache {
  private cache = new Map<string, CacheEntry>();
  private readonly DEFAULT_TTL = 5 * 60 * 1000; // 5 minutes

  async getCachedFile(fileKey: string, options?: GetFileOptions): Promise<FigmaFile | null> {
    const cacheKey = this.generateCacheKey('file', fileKey, options);
    const cached = this.cache.get(cacheKey);

    if (cached && !this.isExpired(cached)) {
      return cached.data;
    }

    return null;
  }

  async setCachedFile(
    fileKey: string,
    data: FigmaFile,
    options?: GetFileOptions,
    ttl?: number
  ): Promise<void> {
    const cacheKey = this.generateCacheKey('file', fileKey, options);
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now(),
      ttl: ttl || this.DEFAULT_TTL
    });
  }

  async getFileWithCache(
    fileKey: string,
    options?: GetFileOptions
  ): Promise<FigmaFile> {
    // Try cache first
    const cached = await this.getCachedFile(fileKey, options);
    if (cached) {
      console.log('Cache hit for file:', fileKey);
      return cached;
    }

    // Fetch from API
    console.log('Cache miss, fetching from API:', fileKey);
    const file = await this.apiClient.getFile(fileKey, options);

    // Cache the result
    await this.setCachedFile(fileKey, file, options);

    return file;
  }

  private generateCacheKey(type: string, ...params: any[]): string {
    return `${type}:${JSON.stringify(params)}`;
  }

  private isExpired(entry: CacheEntry): boolean {
    return Date.now() - entry.timestamp > entry.ttl;
  }

  clearCache(): void {
    this.cache.clear();
  }

  getCacheStats(): CacheStats {
    const entries = Array.from(this.cache.values());
    const expired = entries.filter(entry => this.isExpired(entry)).length;

    return {
      total: entries.length,
      expired,
      size: JSON.stringify(entries).length
    };
  }
}
```

### 3. **Error Handling & Resilience**
```typescript
// Robust error handling
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
    } catch (error) {
      if (this.shouldRetry(error) && retries < this.MAX_RETRIES) {
        console.log(`Retrying request (attempt ${retries + 1}/${this.MAX_RETRIES})`);
        await this.delay(this.RETRY_DELAY * Math.pow(2, retries)); // Exponential backoff
        return this.getFileWithRetry(fileKey, options, retries + 1);
      }
      throw error;
    }
  }

  private shouldRetry(error: any): boolean {
    // Retry on network errors and rate limiting
    return (
      error.code === 'ECONNRESET' ||
      error.code === 'ETIMEDOUT' ||
      error.status === 429 ||
      error.status >= 500
    );
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Data Structures & Response Formats

### 1. **Document Structure**
```typescript
// Complete document structure
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

### 2. **Component Structure**
```typescript
// Component and component set structures
interface ComponentNode extends SceneNode {
  type: 'COMPONENT';
  componentProperties: ComponentPropertyDefinitions;
  mainComponent: ComponentNode;
  instances: InstanceNode[];
}

interface ComponentSetNode extends SceneNode {
  type: 'COMPONENT_SET';
  componentProperties: ComponentPropertyDefinitions;
  children: readonly ComponentNode[];
}

interface ComponentPropertyDefinitions {
  [key: string]: {
    type: 'VARIANT' | 'TEXT' | 'BOOLEAN' | 'INSTANCE_SWAP';
    defaultValue: any;
    variantOptions?: string[];
  };
}
```

### 3. **Style Structure**
```typescript
// Style definitions
interface Style {
  key: string;
  name: string;
  description: string;
  style_type: 'FILL' | 'TEXT' | 'EFFECT' | 'GRID';
  thumbnailUrl: string;
  remote: boolean;
}

interface PaintStyle extends Style {
  style_type: 'FILL';
  fills: readonly Paint[];
}

interface TextStyle extends Style {
  style_type: 'TEXT';
  fontSize: number;
  fontWeight: number;
  lineHeight: LineHeight;
  letterSpacing: number;
  paragraphIndent: number;
  paragraphSpacing: number;
  textCase: TextCase;
  textDecoration: TextDecoration;
}
```

## Rate Limiting & Best Practices

### 1. **Rate Limit Management**
```typescript
// Intelligent rate limiting
class RateLimitManager {
  private requestCount = 0;
  private lastResetTime = Date.now();
  private readonly REQUESTS_PER_HOUR = 3600;
  private readonly REQUESTS_PER_MINUTE = 60;

  async makeRequest<T>(requestFn: () => Promise<T>): Promise<T> {
    await this.checkRateLimit();

    try {
      const result = await requestFn();
      this.incrementRequestCount();
      return result;
    } catch (error) {
      if (error.status === 429) {
        await this.handleRateLimitExceeded();
        return this.makeRequest(requestFn);
      }
      throw error;
    }
  }

  private async checkRateLimit(): Promise<void> {
    const now = Date.now();

    // Check hourly limit
    if (now - this.lastResetTime > 60 * 60 * 1000) {
      this.requestCount = 0;
      this.lastResetTime = now;
    }

    // Check if we're approaching limits
    if (this.requestCount >= this.REQUESTS_PER_HOUR * 0.9) {
      throw new Error('Approaching hourly rate limit');
    }
  }

  private async handleRateLimitExceeded(): Promise<void> {
    const waitTime = 60 * 1000; // Wait 1 minute
    console.log(`Rate limit exceeded, waiting ${waitTime / 1000} seconds`);
    await this.delay(waitTime);
  }

  private incrementRequestCount(): void {
    this.requestCount++;
  }
}
```

### 2. **Usage Optimization**
```typescript
// Optimize API usage
class OptimizedFigmaClient {
  private cache = new Map<string, any>();
  private batchProcessor = new BatchProcessor();

  async getOptimizedFileData(fileKey: string): Promise<OptimizedFileData> {
    // Check cache first
    const cacheKey = `optimized:${fileKey}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Get file structure with minimal depth
    const fileStructure = await this.getFile(fileKey, { depth: 1 });

    // Extract all node IDs for batch processing
    const allNodeIds = this.extractAllNodeIds(fileStructure.document);

    // Batch process nodes
    const nodeData = await this.batchProcessor.processBatch(fileKey, allNodeIds);

    // Process and cache results
    const optimizedData = this.optimizeData(fileStructure, nodeData);
    this.cache.set(cacheKey, optimizedData);

    return optimizedData;
  }

  private optimizeData(
    fileStructure: FigmaFile,
    nodeData: Record<string, SceneNode>
  ): OptimizedFileData {
    return {
      metadata: this.extractMetadata(fileStructure),
      components: this.optimizeComponents(nodeData),
      styles: this.optimizeStyles(fileStructure),
      assets: this.optimizeAssets(nodeData)
    };
  }
}
```

## Integration with Our Project

### 1. **Primary Data Source**
```typescript
// REST API as primary data source
class FigmaRESTExtractor implements DesignExtractor {
  private apiClient: FigmaAPIClient;
  private cache: FigmaAPICache;
  private batchProcessor: BatchProcessor;

  constructor(accessToken: string) {
    this.apiClient = new FigmaAPIClient(accessToken);
    this.cache = new FigmaAPICache();
    this.batchProcessor = new BatchProcessor(this.apiClient);
  }

  async extractDesignSystem(fileKey: string): Promise<DesignSystemExtraction> {
    // Get file structure
    const file = await this.cache.getFileWithCache(fileKey, { depth: 2 });

    // Extract components
    const components = await this.extractComponents(file);

    // Extract styles
    const styles = await this.extractStyles(file);

    // Extract design tokens
    const tokens = await this.extractDesignTokens(file);

    // Generate visual assets
    const assets = await this.generateVisualAssets(fileKey, components);

    return {
      components,
      styles,
      tokens,
      assets,
      metadata: this.extractMetadata(file)
    };
  }
}
```

### 2. **Hybrid Approach Integration**
```typescript
// Combine with other approaches
class HybridFigmaExtractor {
  private restExtractor: FigmaRESTExtractor;
  private pluginExtractor?: PluginExtractor;
  private playwrightExtractor?: PlaywrightExtractor;

  async extractWithFallback(fileKey: string): Promise<DesignSystemExtraction> {
    try {
      // Primary: REST API extraction
      console.log('Attempting REST API extraction...');
      return await this.restExtractor.extractDesignSystem(fileKey);

    } catch (restError) {
      console.warn('REST API extraction failed, trying plugin approach...');

      if (this.pluginExtractor) {
        try {
          return await this.pluginExtractor.extractDesignSystem(fileKey);
        } catch (pluginError) {
          console.warn('Plugin extraction failed, trying Playwright...');
        }
      }

      if (this.playwrightExtractor) {
        return await this.playwrightExtractor.extractDesignSystem(fileKey);
      }

      throw new Error('All extraction methods failed');
    }
  }
}
```

## Limitations & Considerations

### 1. **API Limitations**
- **Rate Limiting**: 3600 requests/hour for standard tier
- **File Size**: Large files may require batch processing
- **Real-time Updates**: No real-time change notifications
- **Write Access**: Limited write capabilities (requires OAuth2)

### 2. **Data Constraints**
- **Vector Data**: Must be explicitly requested with `geometry: 'paths'`
- **Image Export**: Requires separate API calls
- **Component Instances**: Limited instance relationship data
- **Version History**: Limited version access

### 3. **Performance Considerations**
- **Network Latency**: API calls depend on network speed
- **Large Files**: May require significant processing time
- **Concurrent Requests**: Need careful rate limit management
- **Memory Usage**: Large design files can consume significant memory

## Conclusion

The Figma REST API provides a robust, well-documented foundation for automated design system extraction. Its comprehensive coverage of design data, reliable performance, and extensive TypeScript support make it an excellent primary data source for our project.

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

**Recommendation**: Use the REST API as the primary extraction method, supplemented by Playwright for visual validation and Plugin API for advanced interactive features.

---

*Research completed: Figma REST API analysis for comprehensive design system extraction capabilities.*