# SimFlo Canvas Renderer UI/UX Specification V1.0

## 🎯 Purpose
Defines the user interface and user experience design for the SimFlo Canvas Renderer - a professional design preview and debugging tool for SimFlo design format JSON files.

## 🏗️ Architecture Overview

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                    Header (2-layer)                      │
├─────────────┬───────────────────────────┬─────────────────┤
│             │                           │                 │
│   Sidebar   │        Main Canvas        │   Right Panel   │
│  (Navbar)   │                           │  (Tabs)         │
│             │                           │                 │
│   240px     │         flex-1            │     320px       │
│             │                           │                 │
│             │                           │                 │
└─────────────┴───────────────────────────┴─────────────────┘
```

### Component Hierarchy
1. **App Container** - Root layout manager
2. **Header** - 2-layer control system
3. **Sidebar** - Navigation tree view
4. **Main Content** - Canvas area with controls
5. **Right Panel** - Tabbed JSON inspection

## 📱 Responsive Breakpoints

### Desktop (1200px+)
- Full 4-column layout
- All panels visible
- Maximum functionality

### Tablet (768px - 1199px)
- Collapsible sidebar
- Right panel slides over content
- Header controls simplified

### Mobile (320px - 767px)
- Slide-out navigation drawer
- Header simplified to essential controls
- Full-screen canvas view

## 🎨 Components Specification

### 1. App Container

#### Structure
```html
<div class="app-container" data-theme="light">
  <!-- Header -->
  <!-- Main Content Area -->
    <!-- Sidebar -->
    <!-- Canvas Area -->
    <!-- Right Panel -->
</div>
```

#### CSS Variables
```css
:root {
  /* Layout */
  --sidebar-width: 240px;
  --right-panel-width: 320px;
  --header-height: 96px; /* 48px * 2 layers */

  /* Colors - Light Theme */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-tertiary: #9ca3af;
  --border-color: #e5e7eb;
  --accent-color: #6257db;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;
}
```

### 2. Header Component

#### Layout Structure
```html
<header class="app-header">
  <!-- Layer 1: Primary Controls -->
  <div class="header-layer header-layer-1">
    <div class="header-section left">
      <button class="sidebar-toggle" aria-label="Toggle sidebar">
        <svg>...</svg>
      </button>
      <h1 class="app-title">SimFlo Canvas Renderer</h1>
    </div>

    <div class="header-section center">
      <div class="screen-info">
        <span class="screen-name">Login Screen</span>
        <span class="screen-platform">Mobile</span>
      </div>
    </div>

    <div class="header-section right">
      <div class="control-group">
        <!-- Theme Toggle -->
        <button class="control-button theme-toggle" aria-label="Toggle theme">
          <svg class="icon-sun">...</svg>
          <svg class="icon-moon">...</svg>
        </button>

        <!-- Screen Scale -->
        <div class="scale-control">
          <select class="scale-select" aria-label="Screen scale">
            <option value="0.25">25%</option>
            <option value="0.5">50%</option>
            <option value="0.75">75%</option>
            <option value="1" selected>100%</option>
            <option value="1.25">125%</option>
            <option value="1.5">150%</option>
            <option value="2">200%</option>
          </select>
        </div>

        <!-- Refresh -->
        <button class="control-button refresh-btn" aria-label="Refresh">
          <svg>...</svg>
        </button>

        <!-- Download -->
        <button class="control-button download-btn" aria-label="Download">
          <svg>...</svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Layer 2: Device Controls -->
  <div class="header-layer header-layer-2">
    <div class="device-controls">
      <div class="device-type-buttons">
        <button class="device-btn active" data-device="mobile" aria-label="Mobile">
          <svg>...</svg>
          <span>Mobile</span>
        </button>
        <button class="device-btn" data-device="tablet" aria-label="Tablet">
          <svg>...</svg>
          <span>Tablet</span>
        </button>
        <button class="device-btn" data-device="desktop" aria-label="Desktop">
          <svg>...</svg>
          <span>Desktop</span>
        </button>
      </div>

      <div class="orientation-controls">
        <button class="orientation-btn portrait active" data-orientation="portrait" aria-label="Portrait">
          <svg>...</svg>
        </button>
        <button class="orientation-btn landscape" data-orientation="landscape" aria-label="Landscape">
          <svg>...</svg>
        </button>
      </div>

      <div class="pipeline-status">
        <div class="status-indicator success" title="Pipeline successful">
          <span class="status-dot"></span>
          <span class="status-text">Ready</span>
        </div>
      </div>
    </div>
  </div>
</header>
```

#### CSS Styling
```css
.app-header {
  height: var(--header-height);
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.header-layer {
  height: 48px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 16px;
}

.header-layer-1 {
  border-bottom: 1px solid var(--border-color);
  justify-content: space-between;
}

.header-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-button {
  width: 36px;
  height: 36px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
}

.control-button:hover {
  background: var(--bg-tertiary);
  border-color: var(--accent-color);
}

.scale-select {
  padding: 6px 8px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  min-width: 70px;
}

.device-controls {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 1;
}

.device-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.device-btn.active {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-indicator.success {
  background: #dcfce7;
  color: #166534;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
```

### 3. Sidebar Navigation

#### Structure
```html
<aside class="sidebar" data-expanded="true">
  <div class="sidebar-header">
    <h2 class="sidebar-title">Screens</h2>
    <div class="sidebar-controls">
      <button class="collapse-btn" aria-label="Collapse sidebar">
        <svg>...</svg>
      </button>
    </div>
  </div>

  <div class="sidebar-content">
    <!-- Search -->
    <div class="search-container">
      <input type="text" class="search-input" placeholder="Search screens..." />
      <button class="search-clear" aria-label="Clear search">
        <svg>...</svg>
      </button>
    </div>

    <!-- Screen Tree -->
    <div class="screen-tree">
      <div class="tree-group" data-group="authentication">
        <div class="tree-group-header">
          <button class="tree-toggle" aria-expanded="true">
            <svg>...</svg>
          </button>
          <span class="tree-group-label">Authentication</span>
          <span class="tree-group-count">3</span>
        </div>
        <div class="tree-group-content">
          <div class="tree-item active" data-screen="Login">
            <div class="tree-item-content">
              <svg class="tree-item-icon">...</svg>
              <span class="tree-item-label">Login</span>
              <span class="tree-item-badge">mobile</span>
            </div>
          </div>
          <div class="tree-item" data-screen="Register">
            <div class="tree-item-content">
              <svg class="tree-item-icon">...</svg>
              <span class="tree-item-label">Register</span>
              <span class="tree-item-badge">mobile</span>
            </div>
          </div>
          <div class="tree-item" data-screen="ForgotPassword">
            <div class="tree-item-content">
              <svg class="tree-item-icon">...</svg>
              <span class="tree-item-label">Forgot Password</span>
              <span class="tree-item-badge">mobile</span>
            </div>
          </div>
        </div>
      </div>

      <div class="tree-group" data-group="onboarding">
        <div class="tree-group-header">
          <button class="tree-toggle" aria-expanded="false">
            <svg>...</svg>
          </button>
          <span class="tree-group-label">Onboarding</span>
          <span class="tree-group-count">4</span>
        </div>
        <div class="tree-group-content" hidden>
          <!-- Screen items -->
        </div>
      </div>
    </div>
  </div>
</aside>
```

#### CSS Styling
```css
.sidebar {
  width: var(--sidebar-width);
  height: calc(100vh - var(--header-height));
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: var(--transition-normal);
}

.sidebar[data-expanded="false"] {
  width: 0;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.search-container {
  padding: 12px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 8px 32px 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  font-size: 14px;
}

.search-clear {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--text-tertiary);
}

.screen-tree {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.tree-group {
  margin-bottom: 8px;
}

.tree-group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: var(--transition-fast);
}

.tree-group-header:hover {
  background: var(--bg-tertiary);
}

.tree-toggle {
  width: 16px;
  height: 16px;
  border: none;
  background: none;
  cursor: pointer;
  transition: var(--transition-fast);
}

.tree-toggle[aria-expanded="true"] {
  transform: rotate(90deg);
}

.tree-group-label {
  flex: 1;
  font-weight: 500;
  color: var(--text-primary);
}

.tree-group-count {
  font-size: 12px;
  color: var(--text-tertiary);
  background: var(--bg-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
}

.tree-item {
  margin-left: 16px;
  margin-bottom: 2px;
}

.tree-item-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: var(--transition-fast);
}

.tree-item:hover .tree-item-content {
  background: var(--bg-tertiary);
}

.tree-item.active .tree-item-content {
  background: var(--accent-color);
  color: white;
}

.tree-item-label {
  flex: 1;
  font-size: 14px;
  color: inherit;
}

.tree-item-badge {
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 3px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  text-transform: uppercase;
}

.tree-item.active .tree-item-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}
```

### 4. Main Canvas Area

#### Structure
```html
<main class="main-content">
  <div class="canvas-container">
    <!-- Canvas Controls -->
    <div class="canvas-controls">
      <div class="control-group">
        <button class="zoom-control zoom-out" aria-label="Zoom out">
          <svg>...</svg>
        </button>
        <span class="zoom-level">100%</span>
        <button class="zoom-control zoom-in" aria-label="Zoom in">
          <svg>...</svg>
        </button>
        <button class="zoom-control zoom-fit" aria-label="Fit to screen">
          <svg>...</svg>
        </button>
      </div>

      <div class="control-group">
        <button class="grid-toggle" aria-label="Toggle grid">
          <svg>...</svg>
        </button>
        <button class="rulers-toggle" aria-label="Toggle rulers">
          <svg>...</svg>
        </button>
      </div>
    </div>

    <!-- Canvas Viewport -->
    <div class="canvas-viewport">
      <div class="canvas-wrapper" data-scale="1">
        <!-- Device Frame -->
        <div class="device-frame mobile portrait">
          <div class="device-screen">
            <canvas id="renderCanvas" width="390" height="844"></canvas>
          </div>
        </div>

        <!-- Grid Overlay -->
        <div class="grid-overlay" hidden>
          <!-- SVG grid lines -->
        </div>

        <!-- Rulers -->
        <div class="rulers" hidden>
          <div class="ruler-horizontal"></div>
          <div class="ruler-vertical"></div>
        </div>
      </div>
    </div>
  </div>
</main>
```

#### CSS Styling
```css
.main-content {
  flex: 1;
  height: calc(100vh - var(--header-height));
  display: flex;
  flex-direction: column;
  background: var(--bg-tertiary);
}

.canvas-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.canvas-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  display: flex;
  gap: 8px;
  background: var(--bg-primary);
  padding: 8px;
  border-radius: 8px;
  box-shadow: var(--shadow-md);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 8px;
  border-right: 1px solid var(--border-color);
}

.control-group:last-child {
  border-right: none;
}

.zoom-control {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
}

.zoom-control:hover {
  background: var(--bg-secondary);
}

.zoom-level {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  min-width: 40px;
  text-align: center;
}

.canvas-viewport {
  flex: 1;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
}

.canvas-wrapper {
  position: relative;
  transition: var(--transition-normal);
  transform-origin: center center;
}

.device-frame {
  background: var(--bg-primary);
  border-radius: 24px;
  box-shadow: var(--shadow-lg);
  padding: 8px;
  position: relative;
}

.device-frame.mobile {
  width: 390px;
  height: 844px;
}

.device-frame.tablet {
  width: 768px;
  height: 1024px;
  border-radius: 16px;
}

.device-frame.desktop {
  width: 1440px;
  height: 900px;
  border-radius: 8px;
}

.device-screen {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  background: white;
}

#renderCanvas {
  width: 100%;
  height: 100%;
  display: block;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0.3;
}

.rulers {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.ruler-horizontal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
}

.ruler-vertical {
  position: absolute;
  top: 0;
  left: 0;
  width: 20px;
  height: 100%;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
}
```

### 5. Right Panel (JSON Inspector)

#### Structure
```html
<aside class="right-panel" data-expanded="true">
  <!-- Tab Headers -->
  <div class="panel-tabs">
    <button class="tab-btn active" data-tab="preview" aria-selected="true">
      <svg>...</svg>
      <span>Preview</span>
    </button>
    <button class="tab-btn" data-tab="design-json" aria-selected="false">
      <svg>...</svg>
      <span>Design JSON</span>
    </button>
    <button class="tab-btn" data-tab="render-json" aria-selected="false">
      <svg>...</svg>
      <span>Render JSON</span>
    </button>
    <button class="tab-btn" data-tab="details" aria-selected="false">
      <svg>...</svg>
      <span>Details</span>
    </button>
  </div>

  <!-- Tab Content -->
  <div class="panel-content">
    <!-- Preview Tab -->
    <div class="tab-pane active" data-tab="preview">
      <div class="preview-content">
        <div class="preview-section">
          <h3 class="section-title">Screen Information</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Screen Name</label>
              <span class="info-value">Login</span>
            </div>
            <div class="info-item">
              <label>Platform</label>
              <span class="info-value">Mobile</span>
            </div>
            <div class="info-item">
              <label>Resolution</label>
              <span class="info-value">390 × 844</span>
            </div>
            <div class="info-item">
              <label>Components</label>
              <span class="info-value">4</span>
            </div>
          </div>
        </div>

        <div class="preview-section">
          <h3 class="section-title">Component Tree</h3>
          <div class="component-tree">
            <div class="component-node">
              <span class="component-name">Login Screen</span>
              <div class="component-children">
                <div class="component-node">
                  <span class="component-name">Card</span>
                  <div class="component-children">
                    <div class="component-node">
                      <span class="component-name">Title Text</span>
                    </div>
                    <div class="component-node">
                      <span class="component-name">Email Input</span>
                    </div>
                    <div class="component-node">
                      <span class="component-name">Password Input</span>
                    </div>
                    <div class="component-node">
                      <span class="component-name">Sign In Button</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Design JSON Tab -->
    <div class="tab-pane" data-tab="design-json">
      <div class="json-container">
        <div class="json-header">
          <h3 class="json-title">Design JSON</h3>
          <div class="json-controls">
            <button class="json-control copy-btn" aria-label="Copy JSON">
              <svg>...</svg>
            </button>
            <button class="json-control download-btn" aria-label="Download JSON">
              <svg>...</svg>
            </button>
            <button class="json-control format-btn" aria-label="Format JSON">
              <svg>...</svg>
            </button>
          </div>
        </div>
        <div class="json-editor">
          <pre class="json-content"><code id="designJsonContent">{
  "version": "1.0.0",
  "screenType": "mobile",
  "designTokens": {
    // ... JSON content
  }
}</code></pre>
        </div>
      </div>
    </div>

    <!-- Render JSON Tab -->
    <div class="tab-pane" data-tab="render-json">
      <div class="json-container">
        <div class="json-header">
          <h3 class="json-title">Render JSON</h3>
          <div class="json-controls">
            <button class="json-control copy-btn" aria-label="Copy JSON">
              <svg>...</svg>
            </button>
            <button class="json-control download-btn" aria-label="Download JSON">
              <svg>...</svg>
            </button>
            <button class="json-control format-btn" aria-label="Format JSON">
              <svg>...</svg>
            </button>
          </div>
        </div>
        <div class="json-editor">
          <pre class="json-content"><code id="renderJsonContent">{
  "version": "1.0.0",
  "viewport": {
    "width": 390,
    "height": 844
  },
  "elements": [
    // ... JSON content
  ]
}</code></pre>
        </div>
      </div>
    </div>

    <!-- Details Tab -->
    <div class="tab-pane" data-tab="details">
      <div class="details-content">
        <div class="details-section">
          <h3 class="section-title">Pipeline Information</h3>
          <div class="pipeline-status">
            <div class="status-item">
              <span class="status-label">Layout Conversion</span>
              <span class="status-value success">✓ Success</span>
            </div>
            <div class="status-item">
              <span class="status-label">Token Resolution</span>
              <span class="status-value success">✓ Success</span>
            </div>
            <div class="status-item">
              <span class="status-label">Element Generation</span>
              <span class="status-value success">✓ Success</span>
            </div>
            <div class="status-item">
              <span class="status-label">Canvas Rendering</span>
              <span class="status-value success">✓ Success</span>
            </div>
          </div>
        </div>

        <div class="details-section">
          <h3 class="section-title">Performance Metrics</h3>
          <div class="metrics-grid">
            <div class="metric-item">
              <span class="metric-label">Render Time</span>
              <span class="metric-value">12ms</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Elements</span>
              <span class="metric-value">6</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Tokens Resolved</span>
              <span class="metric-value">24</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Memory Usage</span>
              <span class="metric-value">2.1MB</span>
            </div>
          </div>
        </div>

        <div class="details-section">
          <h3 class="section-title">Error Log</h3>
          <div class="error-log">
            <div class="log-entry empty">
              <span class="log-message">No errors or warnings</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</aside>
```

#### CSS Styling
```css
.right-panel {
  width: var(--right-panel-width);
  height: calc(100vh - var(--header-height));
  background: var(--bg-primary);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: var(--transition-normal);
}

.right-panel[data-expanded="false"] {
  width: 0;
  overflow: hidden;
}

.panel-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.tab-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border: none;
  background: none;
  cursor: pointer;
  transition: var(--transition-fast);
  border-bottom: 2px solid transparent;
}

.tab-btn:hover {
  background: var(--bg-tertiary);
}

.tab-btn.active {
  background: var(--bg-primary);
  border-bottom-color: var(--accent-color);
  color: var(--accent-color);
}

.tab-btn svg {
  width: 16px;
  height: 16px;
}

.tab-btn span {
  font-size: 11px;
  font-weight: 500;
}

.panel-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.tab-pane {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  visibility: hidden;
  transition: var(--transition-normal);
}

.tab-pane.active {
  opacity: 1;
  visibility: visible;
}

.preview-content {
  padding: 16px;
  height: 100%;
  overflow-y: auto;
}

.preview-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
}

.info-item label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

.info-value {
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 500;
}

.component-tree {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 12px;
}

.component-node {
  margin-left: 16px;
  padding: 4px 0;
}

.component-node:first-child {
  margin-left: 0;
}

.component-name {
  color: var(--text-primary);
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 3px;
}

.component-name:hover {
  background: var(--bg-secondary);
}

.component-children {
  margin-left: 16px;
  border-left: 1px solid var(--border-color);
  padding-left: 8px;
}

.json-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.json-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-secondary);
}

.json-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.json-controls {
  display: flex;
  gap: 4px;
}

.json-control {
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-primary);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
}

.json-control:hover {
  background: var(--bg-tertiary);
}

.json-editor {
  flex: 1;
  overflow: auto;
  padding: 16px;
  background: var(--bg-primary);
}

.json-content {
  margin: 0;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 12px;
  line-height: 1.5;
  color: var(--text-primary);
  background: var(--bg-secondary);
  padding: 12px;
  border-radius: 6px;
  overflow: auto;
}

.details-content {
  padding: 16px;
  height: 100%;
  overflow-y: auto;
}

.pipeline-status {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
}

.status-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

.status-value.success {
  font-size: 12px;
  color: #166534;
  font-weight: 500;
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.metric-item {
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.metric-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.error-log {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 11px;
}

.log-entry {
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 4px;
}

.log-entry.empty {
  background: #dcfce7;
  color: #166534;
  font-style: italic;
}

.log-entry.error {
  background: #fef2f2;
  color: #dc2626;
}

.log-entry.warning {
  background: #fef3c7;
  color: #d97706;
}
```

## 🎯 Interactive Features

### 1. Screen Navigation
- Click sidebar items to switch screens
- Keyboard navigation (Arrow keys, Enter)
- Search/filter screens in real-time
- Active screen highlighting

### 2. Device & Orientation Controls
- Device type switching with visual feedback
- Orientation toggle with animation
- Canvas resizing based on device type
- Preserve zoom level across device changes

### 3. Zoom & Pan Controls
- Mouse wheel zoom (Ctrl + wheel)
- Pan by dragging canvas
- Zoom to fit button
- Zoom level indicator

### 4. JSON Inspection
- Live JSON updates when switching screens
- Syntax highlighting for JSON content
- Collapsible/expandable JSON sections
- Copy JSON to clipboard
- Download JSON files

### 5. Theme Switching
- Light/dark theme toggle
- Smooth color transitions
- Persistent theme preference
- System theme detection

### 6. Export Features
- Download canvas as PNG/JPEG
- Copy canvas to clipboard
- Export JSON files
- Generate shareable links

## 🔧 Technical Implementation

### JavaScript Architecture
```javascript
class CanvasRendererApp {
  constructor() {
    this.state = {
      currentScreen: null,
      currentDevice: 'mobile',
      currentOrientation: 'portrait',
      currentScale: 1,
      theme: 'light',
      activeTab: 'preview',
      sidebarExpanded: true,
      rightPanelExpanded: true
    };

    this.components = {
      sidebar: new SidebarComponent(),
      header: new HeaderComponent(),
      canvas: new CanvasComponent(),
      rightPanel: new RightPanelComponent()
    };

    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadInitialScreen();
    this.render();
  }

  setupEventListeners() {
    // Navigation events
    this.components.sidebar.on('screen-select', this.handleScreenSelect.bind(this));

    // Device controls
    this.components.header.on('device-change', this.handleDeviceChange.bind(this));
    this.components.header.on('orientation-change', this.handleOrientationChange.bind(this));

    // Theme controls
    this.components.header.on('theme-toggle', this.handleThemeToggle.bind(this));

    // Canvas controls
    this.components.canvas.on('zoom-change', this.handleZoomChange.bind(this));

    // Tab controls
    this.components.rightPanel.on('tab-change', this.handleTabChange.bind(this));
  }

  handleScreenSelect(screenName) {
    this.state.currentScreen = screenName;
    this.loadScreenData(screenName);
    this.render();
  }

  async loadScreenData(screenName) {
    try {
      const designJson = await this.loadDesignJson(screenName);
      const renderJson = await this.convertToRenderJson(designJson);

      this.components.canvas.render(renderJson);
      this.components.rightPanel.updateJson(designJson, renderJson);
      this.components.header.updateScreenInfo(screenName, designJson);

    } catch (error) {
      this.handleError(error);
    }
  }

  render() {
    // Update UI based on current state
    this.updateLayout();
    this.updateTheme();
    this.updateActiveStates();
  }
}

class CanvasComponent {
  constructor(container) {
    this.container = container;
    this.canvas = null;
    this.scale = 1;
    this.setupCanvas();
    this.setupControls();
  }

  setupCanvas() {
    this.canvas = this.container.querySelector('#renderCanvas');
    this.ctx = this.canvas.getContext('2d');
  }

  render(renderJson) {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Render elements
    renderJson.elements.forEach(element => {
      this.renderElement(element);
    });
  }

  renderElement(element) {
    const { type, bounds, styles, content } = element;

    this.ctx.save();

    // Apply styles
    this.applyStyles(styles);

    // Draw element based on type
    switch (type) {
      case 'rectangle':
        this.drawRectangle(bounds);
        break;
      case 'rounded-rectangle':
        this.drawRoundedRectangle(bounds, styles.borderRadius);
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

    this.ctx.restore();
  }
}
```

### Event System
```javascript
class EventEmitter {
  constructor() {
    this.events = {};
  }

  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  }

  emit(event, data) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
  }

  off(event, callback) {
    if (this.events[event]) {
      this.events[event] = this.events[event].filter(cb => cb !== callback);
    }
  }
}
```

### State Management
```javascript
class StateManager {
  constructor(initialState) {
    this.state = initialState;
    this.subscribers = [];
  }

  setState(updates) {
    this.state = { ...this.state, ...updates };
    this.notifySubscribers();
  }

  getState() {
    return this.state;
  }

  subscribe(callback) {
    this.subscribers.push(callback);
    return () => {
      this.subscribers = this.subscribers.filter(sub => sub !== callback);
    };
  }

  notifySubscribers() {
    this.subscribers.forEach(callback => callback(this.state));
  }
}
```

## 📱 Responsive Implementation

### Mobile Adaptations
```css
@media (max-width: 767px) {
  :root {
    --sidebar-width: 100%;
    --right-panel-width: 100%;
    --header-height: 120px;
  }

  .app-container {
    overflow: hidden;
  }

  .sidebar {
    position: fixed;
    top: var(--header-height);
    left: 0;
    z-index: 100;
    transform: translateX(-100%);
  }

  .sidebar[data-expanded="true"] {
    transform: translateX(0);
  }

  .right-panel {
    position: fixed;
    top: var(--header-height);
    right: 0;
    z-index: 100;
    transform: translateX(100%);
  }

  .right-panel[data-expanded="true"] {
    transform: translateX(0);
  }

  .header-layer-1 {
    flex-wrap: wrap;
    height: auto;
    min-height: 48px;
  }

  .header-layer-2 {
    height: auto;
    min-height: 48px;
  }

  .device-controls {
    flex-wrap: wrap;
    gap: 12px;
  }

  .canvas-controls {
    top: 8px;
    right: 8px;
  }
}
```

### Tablet Adaptations
```css
@media (min-width: 768px) and (max-width: 1199px) {
  :root {
    --sidebar-width: 200px;
    --right-panel-width: 280px;
  }

  .sidebar {
    transition: var(--transition-normal);
  }

  .sidebar[data-collapsed="true"] {
    width: 48px;
  }

  .sidebar[data-collapsed="true"] .sidebar-title,
  .sidebar[data-collapsed="true"] .tree-group-label,
  .sidebar[data-collapsed="true"] .tree-item-label {
    display: none;
  }

  .right-panel {
    transition: var(--transition-normal);
  }

  .right-panel[data-overlay="true"] {
    position: fixed;
    top: var(--header-height);
    right: 0;
    height: calc(100vh - var(--header-height));
    z-index: 50;
    box-shadow: -4px 0 12px rgba(0, 0, 0, 0.15);
  }
}
```

## ♿ Accessibility Features

### ARIA Implementation
```html
<!-- Sidebar Navigation -->
<nav class="sidebar" role="navigation" aria-label="Screen navigation">
  <div class="tree-group" role="tree">
    <div class="tree-group-header" role="treeitem" aria-expanded="true">
      <button class="tree-toggle" aria-label="Toggle Authentication group">
        <svg aria-hidden="true">...</svg>
      </button>
      <span class="tree-group-label">Authentication</span>
    </div>
    <div class="tree-group-content" role="group">
      <div class="tree-item" role="treeitem" aria-selected="true">
        <button class="tree-item-content" aria-describedby="screen-login-desc">
          <svg aria-hidden="true">...</svg>
          <span class="tree-item-label">Login</span>
          <span class="tree-item-badge" aria-hidden="true">mobile</span>
        </button>
        <div id="screen-login-desc" class="sr-only">
          Mobile login screen with email and password fields
        </div>
      </div>
    </div>
  </div>
</nav>

<!-- Canvas Controls -->
<div class="canvas-controls" role="toolbar" aria-label="Canvas controls">
  <div class="control-group" role="group" aria-label="Zoom controls">
    <button class="zoom-control zoom-out" aria-label="Zoom out" tabindex="0">
      <svg aria-hidden="true">...</svg>
    </button>
    <span class="zoom-level" aria-live="polite" aria-atomic="true">100%</span>
    <button class="zoom-control zoom-in" aria-label="Zoom in" tabindex="0">
      <svg aria-hidden="true">...</svg>
    </button>
  </div>
</div>

<!-- Tab System -->
<div class="panel-tabs" role="tablist">
  <button class="tab-btn"
          role="tab"
          data-tab="preview"
          aria-selected="true"
          aria-controls="preview-panel"
          tabindex="0">
    <svg aria-hidden="true">...</svg>
    <span>Preview</span>
  </button>
  <button class="tab-btn"
          role="tab"
          data-tab="design-json"
          aria-selected="false"
          aria-controls="design-json-panel"
          tabindex="-1">
    <svg aria-hidden="true">...</svg>
    <span>Design JSON</span>
  </button>
</div>

<div class="panel-content">
  <div class="tab-pane"
       role="tabpanel"
       id="preview-panel"
       aria-labelledby="preview-tab"
       tabindex="0">
    <!-- Preview content -->
  </div>
</div>
```

### Keyboard Navigation
```javascript
class KeyboardNavigation {
  constructor() {
    this.setupKeyboardHandlers();
  }

  setupKeyboardHandlers() {
    document.addEventListener('keydown', this.handleKeyDown.bind(this));
  }

  handleKeyDown(event) {
    switch (event.key) {
      case 'ArrowDown':
        this.handleArrowDown(event);
        break;
      case 'ArrowUp':
        this.handleArrowUp(event);
        break;
      case 'ArrowLeft':
        this.handleArrowLeft(event);
        break;
      case 'ArrowRight':
        this.handleArrowRight(event);
        break;
      case 'Enter':
      case ' ':
        this.handleActivate(event);
        break;
      case 'Escape':
        this.handleEscape(event);
        break;
      case 'Tab':
        // Default tab behavior
        break;
      default:
        if (event.ctrlKey || event.metaKey) {
          this.handleModiferKey(event);
        }
    }
  }

  handleArrowDown(event) {
    const focusable = this.getFocusableElements();
    const currentIndex = focusable.indexOf(document.activeElement);
    const nextIndex = (currentIndex + 1) % focusable.length;
    focusable[nextIndex].focus();
    event.preventDefault();
  }

  handleArrowUp(event) {
    const focusable = this.getFocusableElements();
    const currentIndex = focusable.indexOf(document.activeElement);
    const prevIndex = currentIndex === 0 ? focusable.length - 1 : currentIndex - 1;
    focusable[prevIndex].focus();
    event.preventDefault();
  }

  getFocusableElements() {
    return Array.from(document.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )).filter(el => !el.disabled && !el.hidden);
  }
}
```

### Screen Reader Support
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.focus-visible {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --border-color: #000000;
    --text-primary: #000000;
    --bg-primary: #ffffff;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 🎯 Performance Optimization

### Canvas Rendering Optimization
```javascript
class OptimizedCanvasRenderer {
  constructor() {
    this.offscreenCanvas = null;
    this.renderCache = new Map();
    this.rafId = null;
  }

  async render(renderJson) {
    // Check cache first
    const cacheKey = this.generateCacheKey(renderJson);
    if (this.renderCache.has(cacheKey)) {
      return this.renderCache.get(cacheKey);
    }

    // Use offscreen canvas for complex rendering
    if (this.shouldUseOffscreen(renderJson)) {
      return this.renderOffscreen(renderJson);
    }

    // Throttle rendering with requestAnimationFrame
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
    }

    this.rafId = requestAnimationFrame(() => {
      this.performRender(renderJson);
      this.cacheResult(cacheKey, renderJson);
    });
  }

  shouldUseOffscreen(renderJson) {
    return renderJson.elements.length > 100;
  }

  renderOffscreen(renderJson) {
    if (!this.offscreenCanvas) {
      this.offscreenCanvas = new OffscreenCanvas(this.canvas.width, this.canvas.height);
    }

    const ctx = this.offscreenCanvas.getContext('2d');
    // Render to offscreen canvas
    // Then transfer to main canvas
  }
}
```

### JSON Parsing Optimization
```javascript
class OptimizedJSONParser {
  constructor() {
    this.workerPool = [];
    this.maxWorkers = navigator.hardwareConcurrency || 4;
  }

  async parseLargeJSON(jsonString) {
    if (jsonString.length > 1024 * 1024) { // 1MB
      return this.parseInWorker(jsonString);
    }

    return JSON.parse(jsonString);
  }

  async parseInWorker(jsonString) {
    const worker = this.getAvailableWorker();

    return new Promise((resolve, reject) => {
      worker.onmessage = (event) => {
        this.releaseWorker(worker);
        resolve(event.data);
      };

      worker.onerror = (error) => {
        this.releaseWorker(worker);
        reject(error);
      };

      worker.postMessage(jsonString);
    });
  }

  getAvailableWorker() {
    return this.workerPool.find(w => !w.busy) || this.createWorker();
  }

  createWorker() {
    const worker = new Worker('/js/json-worker.js');
    worker.busy = false;
    this.workerPool.push(worker);
    return worker;
  }
}
```

This comprehensive specification provides a complete blueprint for implementing a professional canvas renderer UI that matches modern design tools while maintaining excellent usability and accessibility standards.