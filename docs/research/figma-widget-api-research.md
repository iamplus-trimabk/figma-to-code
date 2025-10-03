# Figma Widget API Research
## Repository: https://github.com/figma/widget-typings

## Overview
Figma Widgets are a specialized type of Figma plugin that run in a privileged "host environment" within Figma, providing enhanced capabilities for creating interactive UI elements directly in the Figma canvas. Widgets extend the plugin API with specific features for creating persistent, interactive elements that can be embedded in Figma designs and workflows.

## Widget Architecture & Capabilities

### Core Widget Structure
```typescript
// Widget extends plugin API with host environment types
interface WidgetAPI extends PluginAPI {
  // Widget-specific capabilities
  readonly widget: {
    // Widget lifecycle management
    onmessage: (message: WidgetMessage) => void;
    postMessage: (message: WidgetMessage) => void;

    // Canvas interaction
    setRectAsync: (rect: Rect) => Promise<void>;
    getRectAsync: () => Promise<Rect>;

    // Widget UI management
    autofit: boolean;
    resizing: boolean;
  };

  // Enhanced document access
  readonly document: DocumentNode;
  readonly currentPage: PageNode;

  // Widget-specific storage
  readonly widgetSync: AsyncStorage;
}
```

### Widget Environment Types
```typescript
// Host environment types without imports
declare global {
  const figma: WidgetAPI;
  const __html__: string;
}

// Widget message passing
interface WidgetMessage {
  type: string;
  data: any;
  widgetId: string;
  timestamp: number;
}
```

## Widget-Specific Features

### 1. **Canvas Embedding**
```typescript
// Widgets can be embedded directly in the Figma canvas
class CanvasWidget {
  async initialize(): Promise<void> {
    // Set widget dimensions and position
    await figma.widget.setRectAsync({
      x: 100,
      y: 100,
      width: 300,
      height: 200
    });

    // Enable auto-resizing
    figma.widget.autofit = true;

    // Enable manual resizing
    figma.widget.resizing = true;
  }

  async updatePosition(x: number, y: number): Promise<void> {
    const currentRect = await figma.widget.getRectAsync();
    await figma.widget.setRectAsync({
      ...currentRect,
      x,
      y
    });
  }
}
```

### 2. **Persistent Storage**
```typescript
// Widget-specific synchronized storage
class WidgetStorage {
  async saveDesignTokens(tokens: DesignTokens): Promise<void> {
    await figma.widgetSync.setAsync('designTokens', JSON.stringify(tokens));
  }

  async loadDesignTokens(): Promise<DesignTokens | null> {
    const stored = await figma.widgetSync.getAsync('designTokens');
    return stored ? JSON.parse(stored) : null;
  }

  async syncWithProject(projectData: ProjectData): Promise<void> {
    // Synchronize widget state with project
    await figma.widgetSync.setAsync('projectState', JSON.stringify(projectData));
  }
}
```

### 3. **Interactive UI Components**
```typescript
// Rich interactive components within Figma
class InteractiveWidget {
  private uiContainer: HTMLElement;
  private designSystemPanel: DesignSystemPanel;

  constructor() {
    this.uiContainer = document.createElement('div');
    this.designSystemPanel = new DesignSystemPanel();
    this.setupUI();
  }

  private setupUI(): void {
    // Create interactive design system explorer
    this.uiContainer.innerHTML = `
      <div class="widget-container">
        <div class="widget-header">
          <h3>Design System Explorer</h3>
          <button id="refresh-btn">Refresh</button>
        </div>
        <div class="widget-content">
          <div id="component-tree"></div>
          <div id="style-inspector"></div>
          <div id="export-options"></div>
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  private attachEventListeners(): void {
    const refreshBtn = document.getElementById('refresh-btn');
    refreshBtn?.addEventListener('click', () => {
      this.refreshDesignSystem();
    });
  }

  async refreshDesignSystem(): Promise<void> {
    // Extract current design system
    const designSystem = await this.extractDesignSystem();

    // Update UI
    this.updateComponentTree(designSystem.components);
    this.updateStyleInspector(designSystem.styles);

    // Notify parent plugin
    figma.widget.postMessage({
      type: 'DESIGN_SYSTEM_UPDATED',
      data: designSystem
    });
  }
}
```

## Advanced Widget Applications

### 1. **Design System Inspector Widget**
```typescript
// Interactive design system analysis and inspection
class DesignSystemInspector extends InteractiveWidget {
  private analysisEngine: DesignSystemAnalyzer;
  private visualizationEngine: VisualizationEngine;

  constructor() {
    super();
    this.analysisEngine = new DesignSystemAnalyzer();
    this.visualizationEngine = new VisualizationEngine();
    this.setupInspectorUI();
  }

  private setupInspectorUI(): void {
    this.uiContainer.innerHTML = `
      <div class="inspector-widget">
        <div class="inspector-toolbar">
          <button id="analyze-btn">Analyze Design</button>
          <button id="export-btn">Export Tokens</button>
          <button id="validate-btn">Validate</button>
        </div>
        <div class="inspector-panels">
          <div class="panel" id="component-panel">
            <h4>Components</h4>
            <div id="component-list"></div>
          </div>
          <div class="panel" id="style-panel">
            <h4>Styles</h4>
            <div id="style-list"></div>
          </div>
          <div class="panel" id="pattern-panel">
            <h4>Patterns</h4>
            <div id="pattern-list"></div>
          </div>
        </div>
        <div class="inspector-console">
          <h4>Analysis Results</h4>
          <div id="analysis-output"></div>
        </div>
      </div>
    `;

    this.setupInspectorEventListeners();
  }

  async analyzeCurrentDesign(): Promise<void> {
    const analysis = await this.analysisEngine.analyzeDocument(figma.document);

    // Display results
    this.displayComponentAnalysis(analysis.components);
    this.displayStyleAnalysis(analysis.styles);
    this.displayPatternAnalysis(analysis.patterns);

    // Generate visualizations
    await this.generateVisualizations(analysis);
  }

  private displayComponentAnalysis(components: ComponentAnalysis[]): void {
    const componentList = document.getElementById('component-list');
    if (componentList) {
      componentList.innerHTML = components.map(comp => `
        <div class="component-item" data-component-id="${comp.id}">
          <div class="component-header">
            <span class="component-name">${comp.name}</span>
            <span class="component-count">${comp.instances.length} instances</span>
          </div>
          <div class="component-details">
            <div class="component-variants">
              ${comp.variants.map(v => `<span class="variant">${v}</span>`).join('')}
            </div>
            <div class="component-properties">
              ${Object.keys(comp.properties).map(prop =>
                `<span class="property">${prop}</span>`
              ).join('')}
            </div>
          </div>
        </div>
      `).join('');

      // Add interaction handlers
      this.attachComponentInteractions();
    }
  }
}
```

### 2. **Real-time Component Monitor**
```typescript
// Monitor design changes in real-time
class ComponentMonitor extends InteractiveWidget {
  private changeDetector: ChangeDetector;
  private notificationSystem: NotificationSystem;

  constructor() {
    super();
    this.changeDetector = new ChangeDetector();
    this.notificationSystem = new NotificationSystem();
    this.setupMonitoring();
  }

  private setupMonitoring(): void {
    // Monitor document changes
    figma.on('documentchange', async (event: DocumentChangeEvent) => {
      await this.handleDocumentChange(event);
    });

    // Monitor selection changes
    figma.on('selectionchange', async () => {
      await this.handleSelectionChange();
    });

    // Setup UI
    this.setupMonitorUI();
  }

  private async handleDocumentChange(event: DocumentChangeEvent): Promise<void> {
    const changes = await this.changeDetector.analyzeChanges(event);

    // Update UI with changes
    this.displayChanges(changes);

    // Check for design system impact
    const impact = await this.analyzeDesignSystemImpact(changes);
    if (impact.hasImpact) {
      this.notificationSystem.notify({
        type: 'DESIGN_SYSTEM_IMPACT',
        message: impact.description,
        severity: impact.severity
      });
    }
  }

  private async handleSelectionChange(): Promise<void> {
    const selection = figma.currentPage.selection;
    const analysis = await this.analyzeSelection(selection);
    this.updateSelectionInfo(analysis);
  }
}
```

### 3. **Interactive Export Tool**
```typescript
// Advanced export capabilities with user interaction
class InteractiveExportTool extends InteractiveWidget {
  private exportEngine: ExportEngine;
  private previewEngine: PreviewEngine;

  constructor() {
    super();
    this.exportEngine = new ExportEngine();
    this.previewEngine = new PreviewEngine();
    this.setupExportUI();
  }

  private setupExportUI(): void {
    this.uiContainer.innerHTML = `
      <div class="export-widget">
        <div class="export-header">
          <h3>Design System Export</h3>
          <div class="export-options">
            <select id="format-select">
              <option value="react">React Components</option>
              <option value="vue">Vue Components</option>
              <option value="angular">Angular Components</option>
              <option value="tokens">Design Tokens Only</option>
            </select>
            <select id="framework-select">
              <option value="tailwind">Tailwind CSS</option>
              <option value="styled-components">Styled Components</option>
              <option value="emotion">Emotion</option>
              <option value="css">CSS Variables</option>
            </select>
          </div>
        </div>
        <div class="export-content">
          <div class="export-preview" id="export-preview">
            <h4>Preview</h4>
            <div id="preview-content"></div>
          </div>
          <div class="export-config" id="export-config">
            <h4>Configuration</h4>
            <div id="config-options"></div>
          </div>
        </div>
        <div class="export-actions">
          <button id="preview-btn">Generate Preview</button>
          <button id="export-btn">Export Code</button>
          <button id="copy-btn">Copy to Clipboard</button>
        </div>
        <div class="export-status" id="export-status"></div>
      </div>
    `;

    this.setupExportEventListeners();
  }

  async generateExportPreview(): Promise<void> {
    const format = (document.getElementById('format-select') as HTMLSelectElement).value;
    const framework = (document.getElementById('framework-select') as HTMLSelectElement).value;

    // Generate export configuration
    const config: ExportConfig = {
      format,
      framework,
      components: await this.getSelectedComponents(),
      styles: await this.getSelectedStyles(),
      options: this.getExportOptions()
    };

    // Generate preview
    const preview = await this.previewEngine.generatePreview(config);
    this.displayPreview(preview);
  }

  async performExport(): Promise<void> {
    const config = this.getExportConfig();

    try {
      this.showExportStatus('Exporting...', 'loading');

      const exportResult = await this.exportEngine.export(config);

      this.showExportStatus('Export successful!', 'success');
      this.displayExportResult(exportResult);

      // Store export history
      await this.saveExportHistory(config, exportResult);

    } catch (error) {
      this.showExportStatus(`Export failed: ${error.message}`, 'error');
    }
  }
}
```

## Widget vs Plugin Comparison

### Enhanced Capabilities
| Feature | Plugin | Widget |
|---------|--------|--------|
| **Canvas Presence** | Floating UI | Embedded in canvas |
| **Persistence** | Session-based | Persistent across sessions |
| **Storage** | clientStorage only | clientStorage + widgetSync |
| **UI Flexibility** | Modal panels | Embedded interactive elements |
| **Real-time Updates** | Limited | Full real-time capabilities |
| **User Interaction** | Tool-based | Direct manipulation |

### Use Case Scenarios
```typescript
// Widget is ideal for persistent design system tools
class DesignSystemWidget extends InteractiveWidget {
  // Persistent design system monitoring
  async monitorDesignSystem(): Promise<void> {
    // Continuously monitor design changes
    figma.on('documentchange', this.handleDesignChange);
  }

  // Interactive component exploration
  async exploreComponents(): Promise<void> {
    // Allow users to interactively explore components
    this.setupComponentExplorer();
  }

  // Real-time validation
  async validateDesignSystem(): Promise<void> {
    // Provide real-time feedback on design system health
    this.setupValidationEngine();
  }
}
```

## Integration with Design System Extraction

### 1. **Interactive Extraction Assistant**
```typescript
// Widget for guiding extraction process
class ExtractionAssistantWidget extends InteractiveWidget {
  private extractionWizard: ExtractionWizard;
  private progressTracker: ProgressTracker;

  constructor() {
    super();
    this.extractionWizard = new ExtractionWizard();
    this.progressTracker = new ProgressTracker();
    this.setupAssistantUI();
  }

  private setupAssistantUI(): void {
    this.uiContainer.innerHTML = `
      <div class="extraction-assistant">
        <div class="wizard-header">
          <h3>Design System Extraction</h3>
          <div class="progress-bar">
            <div class="progress-fill" id="progress-fill"></div>
          </div>
        </div>
        <div class="wizard-content" id="wizard-content">
          <!-- Dynamic wizard steps -->
        </div>
        <div class="wizard-actions">
          <button id="prev-btn">Previous</button>
          <button id="next-btn">Next</button>
          <button id="extract-btn">Start Extraction</button>
        </div>
      </div>
    `;

    this.startExtractionWizard();
  }

  async startExtractionWizard(): Promise<void> {
    await this.extractionWizard.start({
      steps: [
        'select-components',
        'configure-options',
        'preview-extraction',
        'perform-extraction',
        'validate-results'
      ],
      onStepChange: this.handleWizardStepChange.bind(this),
      onComplete: this.handleWizardComplete.bind(this)
    });
  }

  private async handleWizardComplete(config: ExtractionConfig): Promise<void> {
    // Perform extraction with user configuration
    const result = await this.performExtraction(config);
    this.displayExtractionResults(result);
  }
}
```

### 2. **Visual Feedback System**
```typescript
// Real-time visual feedback during extraction
class VisualFeedbackWidget extends InteractiveWidget {
  private visualizationEngine: VisualizationEngine;
  private highlightingEngine: HighlightingEngine;

  constructor() {
    super();
    this.visualizationEngine = new VisualizationEngine();
    this.highlightingEngine = new HighlightingEngine();
    this.setupFeedbackUI();
  }

  async showExtractionProgress(extraction: ExtractionProcess): Promise<void> {
    // Visualize extraction progress on canvas
    for (const step of extraction.steps) {
      await this.highlightStep(step);
      await this.showStepProgress(step);
      await this.delay(500); // Visual feedback delay
    }
  }

  private async highlightStep(step: ExtractionStep): Promise<void> {
    // Highlight nodes being processed
    for (const nodeId of step.nodeIds) {
      const node = figma.getNodeById(nodeId);
      if (node) {
        await this.highlightingEngine.highlightNode(node, {
          color: step.status === 'complete' ? '#00ff00' : '#ffff00',
          duration: 1000
        });
      }
    }
  }

  async displayExtractionResults(results: ExtractionResults): Promise<void> {
    // Show extraction summary in widget
    this.uiContainer.querySelector('.results-panel')!.innerHTML = `
      <div class="extraction-summary">
        <h4>Extraction Complete</h4>
        <div class="stats">
          <div class="stat">
            <span class="stat-label">Components</span>
            <span class="stat-value">${results.components.length}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Styles</span>
            <span class="stat-value">${results.styles.length}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Patterns</span>
            <span class="stat-value">${results.patterns.length}</span>
          </div>
        </div>
        <div class="actions">
          <button id="view-results-btn">View Results</button>
          <button id="export-code-btn">Export Code</button>
        </div>
      </div>
    `;
  }
}
```

## Technical Implementation Considerations

### 1. **Widget Communication**
```typescript
// Robust message passing between widget and plugin
class WidgetCommunication {
  private messageQueue: WidgetMessage[] = [];
  private responseHandlers: Map<string, (response: any) => void> = new Map();

  constructor() {
    this.setupMessageHandlers();
  }

  private setupMessageHandlers(): void {
    figma.widget.onmessage = async (msg: WidgetMessage) => {
      if (msg.type === 'RESPONSE') {
        const handler = this.responseHandlers.get(msg.id);
        if (handler) {
          handler(msg.data);
          this.responseHandlers.delete(msg.id);
        }
      } else {
        await this.handleRequest(msg);
      }
    };
  }

  async sendRequest<T>(type: string, data: any): Promise<T> {
    const messageId = this.generateMessageId();

    return new Promise((resolve, reject) => {
      this.responseHandlers.set(messageId, (response) => {
        if (response.error) {
          reject(new Error(response.error));
        } else {
          resolve(response.data);
        }
      });

      figma.widget.postMessage({
        id: messageId,
        type,
        data,
        timestamp: Date.now()
      });
    });
  }
}
```

### 2. **Performance Optimization**
```typescript
// Efficient widget performance
class WidgetPerformance {
  private debouncedUpdate: DebouncedFunction;
  private cache: Map<string, any> = new Map();

  constructor() {
    this.debouncedUpdate = debounce(this.performUpdate.bind(this), 100);
  }

  async updateVisualization(data: any): Promise<void> {
    // Cache expensive operations
    const cacheKey = JSON.stringify(data);
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Debounce updates to prevent excessive rendering
    this.debouncedUpdate(data);
  }

  private async performUpdate(data: any): Promise<void> {
    // Perform expensive visualization updates
    const result = await this.generateVisualization(data);
    this.cache.set(JSON.stringify(data), result);
    this.renderVisualization(result);
  }
}
```

## Recommendations for Our Project

### 1. **Widget Use Cases**
- **Interactive Extraction Assistant**: Guide users through extraction process
- **Real-time Progress Monitor**: Show extraction progress on canvas
- **Visual Validation Tool**: Highlight extracted components and patterns
- **Configuration Interface**: Interactive configuration of extraction options

### 2. **Integration Strategy**
```typescript
// Recommended widget integration
class FigmaToCodeWidget extends InteractiveWidget {
  private extractionEngine: ExtractionEngine;
  private visualizationEngine: VisualizationEngine;
  private configurationEngine: ConfigurationEngine;

  constructor() {
    super();
    this.extractionEngine = new ExtractionEngine();
    this.visualizationEngine = new VisualizationEngine();
    this.configurationEngine = new ConfigurationEngine();
    this.initializeWidget();
  }

  private async initializeWidget(): Promise<void> {
    // Setup persistent design system monitoring
    await this.setupMonitoring();

    // Create interactive extraction interface
    await this.createExtractionInterface();

    // Initialize real-time feedback system
    await this.setupFeedbackSystem();
  }
}
```

### 3. **Key Advantages**
- **Persistent Presence**: Always available in Figma canvas
- **Real-time Interaction**: Immediate feedback and updates
- **Enhanced UX**: Direct manipulation and visualization
- **Seamless Integration**: Native Figma experience

## Conclusion

Figma Widgets offer unique capabilities for creating persistent, interactive design system extraction tools directly within the Figma canvas. While they require widget development and have some limitations compared to traditional plugins, they provide superior user experience for certain use cases.

**Key Advantages**:
- Persistent canvas presence
- Real-time interaction capabilities
- Enhanced user experience
- Direct visualization and feedback
- Seamless Figma integration

**Recommendation**: Implement widgets for user-facing extraction tools and interactive assistants, while using traditional plugins for heavy-duty background processing and REST API for initial data access.

---

*Research completed: Figma Widget API analysis for interactive design system extraction tools.*