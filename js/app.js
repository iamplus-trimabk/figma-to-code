/**
 * SimFlo Canvas Renderer - Main Application
 * Contains state management and application logic
 */

// =========================
// APP STATE MANAGEMENT
// =========================
class AppState {
    constructor() {
        this.currentScreen = 'Login';
        this.currentDevice = 'mobile';
        this.currentOrientation = 'portrait';
        this.currentScale = 1;
        this.theme = 'light';
        this.activeTab = 'preview';
        this.sidebarExpanded = true;
        this.rightPanelExpanded = true;
        this.gridVisible = false;
        this.rulersVisible = false;
    }

    update(updates) {
        Object.assign(this, updates);
        this.notifySubscribers();
    }

    subscribe(callback) {
        this.subscribers = this.subscribers || [];
        this.subscribers.push(callback);
    }

    notifySubscribers() {
        if (this.subscribers) {
            this.subscribers.forEach(callback => callback(this));
        }
    }
}

// =========================
// MAIN APPLICATION
// =========================
class CanvasRendererApp {
    constructor() {
        this.state = new AppState();
        this.components = {};
        this.currentDesignJson = null;
        this.currentRenderJson = null;
        this.layoutConverter = null;
        this.canvasRenderer = null;
        this.isRendering = false;
        this.pendingRender = null;
        this.renderTimeout = null;

        this.init();
    }

    init() {
        this.initComponents();
        this.setupEventListeners();
        this.loadInitialScreen();
        this.state.subscribe(this.render.bind(this));
    }

    initComponents() {
        // Initialize layout converter
        this.layoutConverter = new LayoutConverter(null); // Will be updated with actual tokens when converting

        // Initialize canvas renderer
        const canvas = document.getElementById('renderCanvas');
        this.canvasRenderer = new CanvasRenderer(canvas);

        // Store UI components
        this.components = {
            sidebar: document.getElementById('sidebar'),
            rightPanel: document.getElementById('rightPanel'),
            deviceFrame: document.getElementById('deviceFrame'),
            canvasWrapper: document.getElementById('canvasWrapper'),
            tabButtons: document.querySelectorAll('.tab-btn'),
            tabPanes: document.querySelectorAll('.tab-pane')
        };

        // Initialize resize observer for container sync
        this.initResizeObserver();
    }

  initResizeObserver() {
        // Create a resize observer to detect container size changes
        this.resizeObserver = new ResizeObserver((entries) => {
            for (const entry of entries) {
                if (entry.target === this.components.deviceFrame ||
                    entry.target === this.canvasRenderer.canvas.parentElement) {
                    // Debounce resize events
                    if (this.resizeTimeout) {
                        clearTimeout(this.resizeTimeout);
                    }

                    this.resizeTimeout = setTimeout(() => {
                        // Only re-render if we have current data
                        if (this.currentRenderJson) {
                            this.renderToCanvas(this.currentRenderJson);
                        }
                    }, 100); // 100ms debounce
                }
            }
        });

        // Observe the device frame for size changes
        this.resizeObserver.observe(this.components.deviceFrame);

        // Also observe the canvas container as fallback
        const canvasContainer = this.canvasRenderer.canvas.parentElement;
        this.resizeObserver.observe(canvasContainer);
    }

    setupEventListeners() {
        // Sidebar toggle
        document.getElementById('sidebarToggle').addEventListener('click', () => {
            this.toggleSidebar();
        });

        document.getElementById('sidebarCollapse').addEventListener('click', () => {
            this.toggleSidebar();
        });

        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Screen scale
        document.getElementById('scaleSelect').addEventListener('change', (e) => {
            this.setScale(parseFloat(e.target.value));
        });

        // Refresh
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshCurrentScreen();
        });

        // Download
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadCanvas();
        });

        // Device controls
        document.querySelectorAll('.device-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setDevice(e.currentTarget.dataset.device);
            });
        });

        // Orientation controls
        document.querySelectorAll('.orientation-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setOrientation(e.currentTarget.dataset.orientation);
            });
        });

        // Zoom controls
        document.getElementById('zoomIn').addEventListener('click', () => {
            this.zoom(0.1);
        });

        document.getElementById('zoomOut').addEventListener('click', () => {
            this.zoom(-0.1);
        });

        document.getElementById('zoomFit').addEventListener('click', () => {
            this.zoomToFit();
        });

        // Grid and rulers toggle
        document.getElementById('gridToggle').addEventListener('click', () => {
            this.toggleGrid();
        });

        document.getElementById('rulersToggle').addEventListener('click', () => {
            this.toggleRulers();
        });

        // Screen navigation
        document.querySelectorAll('.tree-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const screenName = e.currentTarget.dataset.screen;

                // Check if screen is unavailable
                if (e.currentTarget.classList.contains('unavailable')) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.updatePipelineStatus('Screen not available', 'error');
                    this.addErrorLogEntry(`Screen "${screenName}" is not available in the current design data.`);
                    return;
                }

                if (screenName) {
                    this.selectScreen(screenName);
                }
            });
        });

        // Tree group toggles
        document.querySelectorAll('.tree-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                const header = e.currentTarget.closest('.tree-group-header');
                const content = header.nextElementSibling;
                const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

                toggle.setAttribute('aria-expanded', !isExpanded);
                content.hidden = isExpanded;
            });
        });

        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabName = e.currentTarget.dataset.tab;
                this.setActiveTab(tabName);
            });
        });

        // JSON controls
        document.getElementById('copyDesignJson').addEventListener('click', () => {
            this.copyJsonToClipboard('designJsonContent');
        });

        document.getElementById('copyRenderJson').addEventListener('click', () => {
            this.copyJsonToClipboard('renderJsonContent');
        });

        document.getElementById('downloadDesignJson').addEventListener('click', () => {
            this.downloadJson('design', this.currentDesignJson);
        });

        document.getElementById('downloadRenderJson').addEventListener('click', () => {
            this.downloadJson('render', this.currentRenderJson);
        });

        // Search functionality
        const searchInput = document.getElementById('screenSearch');
        const searchClear = document.getElementById('searchClear');

        searchInput.addEventListener('input', (e) => {
            this.filterScreens(e.target.value);
        });

        searchClear.addEventListener('click', () => {
            searchInput.value = '';
            this.filterScreens('');
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcut(e);
        });
    }

    async loadInitialScreen() {
        await this.loadScreen('Login');
    }

    async loadScreen(screenName) {
        try {
            // Update pipeline status
            this.updatePipelineStatus('Loading...', 'loading');

            // Load design JSON
            const designJson = await this.loadDesignJson(screenName);
            this.currentDesignJson = designJson;

            // Auto-switch device based on screen platform
            this.autoSwitchDeviceForScreen(designJson, screenName);

            // Convert to render JSON
            const renderJson = await this.convertToRenderJson(designJson);
            this.currentRenderJson = renderJson;

            // Render to canvas
            await this.renderToCanvas(renderJson);

            // Update UI
            this.updateJsonViewers(designJson, renderJson);
            this.updateScreenInfo(screenName, designJson);
            this.updateComponentTree(renderJson);

            // Update pipeline status
            this.updatePipelineStatus('Ready', 'success');

            // Update performance metrics
            this.updateMetrics();

        } catch (error) {
            console.error('Error loading screen:', error);
            this.updatePipelineStatus('Error', 'error');
            this.addErrorLogEntry(error.message);
        }
    }

    async loadDesignJson(screenName) {
        try {
            const response = await fetch('login-screen-example.json');
            const designJson = await response.json();

            // Check if the requested screen exists in the design JSON
            if (!designJson.screens || !designJson.screens[screenName]) {
                throw new Error(`Screen "${screenName}" not found in design data. Available screens: ${Object.keys(designJson.screens || {}).join(', ')}`);
            }

            // Update screen availability in UI
            this.updateScreenAvailability(designJson.screens || {});

            return designJson;
        } catch (error) {
            console.error('Error loading design JSON:', error);
            throw error;
        }
    }

    autoSwitchDeviceForScreen(designJson, screenName) {
        // Get the screen definition
        const screen = designJson.screens[screenName];
        if (!screen || !screen.platform) {
            // No platform specified, keep current device
            return;
        }

        // Map platform to device
        let targetDevice;
        switch (screen.platform) {
            case 'desktop':
                targetDevice = 'desktop';
                break;
            case 'tablet':
                targetDevice = 'tablet';
                break;
            case 'mobile':
            default:
                targetDevice = 'mobile';
                break;
        }

        // Only switch if different from current device
        if (targetDevice !== this.state.currentDevice) {
            console.log(`Auto-switching to ${targetDevice} for ${screenName} screen (platform: ${screen.platform})`);
            this.setDevice(targetDevice);
        }
    }

    updateScreenAvailability(availableScreens) {
        // Get all screen items in the sidebar
        const screenItems = document.querySelectorAll('.tree-item[data-screen]');

        screenItems.forEach(item => {
            const screenName = item.dataset.screen;

            if (availableScreens[screenName]) {
                // Screen is available - remove unavailable class
                item.classList.remove('unavailable');
            } else {
                // Screen is not available - add unavailable class
                item.classList.add('unavailable');
            }
        });
    }

    async convertToRenderJson(designJson) {
        const viewport = this.getViewportForCurrentDevice();
        const screenName = this.state.currentScreen;

        // Add the current screen to the designJson for the converter
        const designJsonWithScreen = {
            ...designJson,
            currentScreenName: screenName
        };

        return this.layoutConverter.convert(designJsonWithScreen, viewport, this.state.theme);
    }

    async renderToCanvas(renderJson) {
        // Prevent concurrent renders
        if (this.isRendering) {
            this.pendingRender = renderJson;
            return;
        }

        this.isRendering = true;
        const startTime = performance.now();

        try {
            // Clear canvas completely (resets all context state)
            this.canvasRenderer.clear();

            // Get canvas and container dimensions
            const canvas = document.getElementById('renderCanvas');
            const containerRect = canvas.parentElement.getBoundingClientRect();

            // Validate dimensions
            if (containerRect.width <= 0 || containerRect.height <= 0) {
                console.warn('Invalid container dimensions:', containerRect);
                return 0;
            }

            // Update canvas size to match container
            const dpr = window.devicePixelRatio || 1;
            canvas.width = containerRect.width * dpr;
            canvas.height = containerRect.height * dpr;

            // Set canvas CSS size
            canvas.style.width = containerRect.width + 'px';
            canvas.style.height = containerRect.height + 'px';

            // Get context and apply high DPI scaling
            const ctx = canvas.getContext('2d');
            ctx.scale(dpr, dpr);

            // Calculate scaling factor from design size to actual canvas size
            const designWidth = renderJson.viewport.width;
            const designHeight = renderJson.viewport.height;
            const scaleX = containerRect.width / designWidth;
            const scaleY = containerRect.height / designHeight;
            const scale = Math.min(scaleX, scaleY); // Use uniform scaling to maintain aspect ratio

            // Calculate centered position
            const offsetX = (containerRect.width - designWidth * scale) / 2;
            const offsetY = (containerRect.height - designHeight * scale) / 2;

            // Apply scaling transform to canvas
            ctx.save();
            ctx.translate(offsetX, offsetY);
            ctx.scale(scale, scale);

            // Render elements
            if (renderJson.elements && Array.isArray(renderJson.elements)) {
                for (const element of renderJson.elements) {
                    this.canvasRenderer.renderElement(element);
                }
            }

            // Restore context state
            ctx.restore();

            const endTime = performance.now();
            return endTime - startTime;

        } catch (error) {
            console.error('Error rendering to canvas:', error);
            return 0;
        } finally {
            this.isRendering = false;

            // Process pending render if any
            if (this.pendingRender) {
                const pending = this.pendingRender;
                this.pendingRender = null;

                // Use setTimeout to prevent stack overflow and allow UI updates
                this.renderTimeout = setTimeout(() => {
                    this.renderToCanvas(pending);
                }, 16); // ~60fps
            }
        }
    }

    getViewportForCurrentDevice() {
        const { currentDevice, currentOrientation } = this.state;

        if (currentDevice === 'mobile') {
            return currentOrientation === 'portrait'
                ? { x: 0, y: 0, width: 390, height: 844 }
                : { x: 0, y: 0, width: 844, height: 390 };
        } else if (currentDevice === 'tablet') {
            return currentOrientation === 'portrait'
                ? { x: 0, y: 0, width: 768, height: 1024 }
                : { x: 0, y: 0, width: 1024, height: 768 };
        } else { // desktop
            return { x: 0, y: 0, width: 1440, height: 900 };
        }
    }

    // =========================
    // UI STATE MANAGEMENT
    // =========================

    selectScreen(screenName) {
        // Update active state in sidebar
        document.querySelectorAll('.tree-item').forEach(item => {
            item.classList.toggle('active', item.dataset.screen === screenName);
        });

        // Update screen and reload
        this.state.update({ currentScreen: screenName });
        this.loadScreen(screenName);
    }

    setDevice(device) {
        // Clear any pending renders
        this.clearPendingRenders();

        // Update active device button
        document.querySelectorAll('.device-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.device === device);
        });

        // Update device frame
        const deviceFrame = this.components.deviceFrame;
        deviceFrame.className = `device-frame ${device} ${this.state.currentOrientation}`;

        // Update state and reload
        this.state.update({ currentDevice: device });

        // Delay render slightly to allow CSS transitions
        setTimeout(() => {
            this.loadScreen(this.state.currentScreen);
        }, 50);
    }

    setOrientation(orientation) {
        // Clear any pending renders
        this.clearPendingRenders();

        // Update active orientation button
        document.querySelectorAll('.orientation-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.orientation === orientation);
        });

        // Update device frame
        const deviceFrame = this.components.deviceFrame;
        deviceFrame.className = `device-frame ${this.state.currentDevice} ${orientation}`;

        // Update state and reload
        this.state.update({ currentOrientation: orientation });

        // Delay render slightly to allow CSS transitions
        setTimeout(() => {
            this.loadScreen(this.state.currentScreen);
        }, 50);
    }

  clearPendingRenders() {
        // Clear any pending renders
        if (this.renderTimeout) {
            clearTimeout(this.renderTimeout);
            this.renderTimeout = null;
        }
        this.pendingRender = null;
        this.isRendering = false;
    }

    setScale(scale) {
        this.state.update({ currentScale: scale });
        this.components.canvasWrapper.style.transform = `scale(${scale})`;
        document.getElementById('zoomLevel').textContent = `${Math.round(scale * 100)}%`;
        document.getElementById('scaleSelect').value = scale;
    }

    zoom(delta) {
        const newScale = Math.max(0.25, Math.min(2, this.state.currentScale + delta));
        this.setScale(newScale);
    }

    zoomToFit() {
        // Calculate scale to fit the device frame in the viewport
        const container = this.components.canvasWrapper.parentElement;
        const deviceFrame = this.components.deviceFrame;

        const containerRect = container.getBoundingClientRect();
        const frameRect = deviceFrame.getBoundingClientRect();

        const scaleX = (containerRect.width - 64) / frameRect.width; // 64px for padding
        const scaleY = (containerRect.height - 64) / frameRect.height;
        const scale = Math.min(scaleX, scaleY, 1); // Don't scale up beyond 100%

        this.setScale(scale);
    }

    toggleSidebar() {
        const isExpanded = !this.state.sidebarExpanded;
        this.state.update({ sidebarExpanded: isExpanded });

        const container = document.querySelector('.app-container');
        container.setAttribute('data-sidebar-collapsed', !isExpanded);
    }

    toggleTheme() {
        const newTheme = this.state.theme === 'light' ? 'dark' : 'light';
        this.state.update({ theme: newTheme });

        const container = document.querySelector('.app-container');
        container.setAttribute('data-theme', newTheme);

        // Update theme icon
        const themeToggle = document.getElementById('themeToggle');
        const icon = newTheme === 'light'
            ? '<svg class="icon-sun" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>'
            : '<svg class="icon-moon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>';
        themeToggle.innerHTML = icon;
    }

    setActiveTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            const isActive = btn.dataset.tab === tabName;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-selected', isActive);
        });

        // Update active tab pane
        document.querySelectorAll('.tab-pane').forEach(pane => {
            const isActive = pane.dataset.tab === tabName;
            pane.classList.toggle('active', isActive);
        });

        this.state.update({ activeTab: tabName });
    }

    toggleGrid() {
        this.state.gridVisible = !this.state.gridVisible;
        const gridToggle = document.getElementById('gridToggle');
        const gridOverlay = document.getElementById('gridOverlay');

        // Update button color
        gridToggle.style.color = this.state.gridVisible ? 'var(--accent-color)' : 'var(--text-secondary)';

        // Show/hide grid overlay
        if (this.state.gridVisible) {
            gridOverlay.classList.remove('hidden');
            gridOverlay.classList.add('visible');
        } else {
            gridOverlay.classList.remove('visible');
            gridOverlay.classList.add('hidden');
        }
    }

    toggleRulers() {
        this.state.rulersVisible = !this.state.rulersVisible;
        const rulersToggle = document.getElementById('rulersToggle');
        const rulersContainer = document.getElementById('rulersContainer');

        // Update button color
        rulersToggle.style.color = this.state.rulersVisible ? 'var(--accent-color)' : 'var(--text-secondary)';

        // Show/hide rulers
        if (this.state.rulersVisible) {
            rulersContainer.classList.remove('hidden');
            rulersContainer.classList.add('visible');
            this.generateRulerLabels();
        } else {
            rulersContainer.classList.remove('visible');
            rulersContainer.classList.add('hidden');
        }
    }

    generateRulerLabels() {
        const rulerHorizontal = document.getElementById('rulerHorizontal');
        const rulerVertical = document.getElementById('rulerVertical');

        // Clear existing labels
        rulerHorizontal.querySelectorAll('.ruler-label').forEach(label => label.remove());
        rulerVertical.querySelectorAll('.ruler-label').forEach(label => label.remove());

        // Get canvas dimensions
        const canvas = document.getElementById('renderCanvas');
        if (!canvas) return;

        const canvasRect = canvas.getBoundingClientRect();
        const containerRect = canvas.parentElement.getBoundingClientRect();

        // Generate horizontal ruler labels (every 64px)
        for (let x = 0; x <= canvasRect.width; x += 64) {
            const label = document.createElement('div');
            label.className = 'ruler-label';
            label.textContent = x.toString();
            label.style.left = `${x + 20}px`; // Offset for ruler width
            rulerHorizontal.appendChild(label);
        }

        // Generate vertical ruler labels (every 64px)
        for (let y = 0; y <= canvasRect.height; y += 64) {
            const label = document.createElement('div');
            label.className = 'ruler-label';
            label.textContent = y.toString();
            label.style.top = `${y + 20}px`; // Offset for ruler height
            rulerVertical.appendChild(label);
        }
    }

    // =========================
    // UTILITY METHODS
    // =========================

    refreshCurrentScreen() {
        this.loadScreen(this.state.currentScreen);
    }

    downloadCanvas() {
        const canvas = document.getElementById('renderCanvas');
        const link = document.createElement('a');
        link.download = `${this.state.currentScreen}-rendered.png`;
        link.href = canvas.toDataURL();
        link.click();
    }

    copyJsonToClipboard(elementId) {
        const content = document.getElementById(elementId).textContent;
        navigator.clipboard.writeText(content).then(() => {
            this.showTemporaryMessage('Copied to clipboard!');
        });
    }

    downloadJson(type, jsonData) {
        const dataStr = JSON.stringify(jsonData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.download = `${this.state.currentScreen}-${type}.json`;
        link.href = url;
        link.click();

        URL.revokeObjectURL(url);
    }

    filterScreens(searchTerm) {
        const term = searchTerm.toLowerCase();
        document.querySelectorAll('.tree-item').forEach(item => {
            const label = item.querySelector('.tree-item-label');
            const shouldShow = !term || label.textContent.toLowerCase().includes(term);
            item.style.display = shouldShow ? 'block' : 'none';
        });

        // Update clear button visibility
        document.getElementById('searchClear').style.display =
            searchTerm ? 'block' : 'none';
    }

    updatePipelineStatus(message, type) {
        const statusElement = document.getElementById('pipelineStatus');
        const statusText = statusElement.querySelector('.status-text');
        const statusDot = statusElement.querySelector('.status-dot');

        statusText.textContent = message;
        statusElement.className = `status-indicator ${type}`;
    }

    updateScreenInfo(screenName, designJson) {
        document.getElementById('screenName').textContent = screenName;
        document.getElementById('screenPlatform').textContent =
            designJson.screenType.charAt(0).toUpperCase() + designJson.screenType.slice(1);

        document.getElementById('infoScreenName').textContent = screenName;
        document.getElementById('infoPlatform').textContent = designJson.screenType;

        const viewport = this.getViewportForCurrentDevice();
        document.getElementById('infoResolution').textContent =
            `${viewport.width} × ${viewport.height}`;
    }

    updateJsonViewers(designJson, renderJson) {
        // Update JSON content with proper formatting
        document.getElementById('designJsonContent').textContent =
            JSON.stringify(designJson, null, 2);
        document.getElementById('renderJsonContent').textContent =
            JSON.stringify(renderJson, null, 2);
    }

    updateComponentTree(renderJson) {
        // Build component tree from render JSON
        const componentTree = document.getElementById('componentTree');
        componentTree.innerHTML = ''; // Clear existing tree

        // Build hierarchical tree structure
        const treeData = this.buildTreeData(renderJson.elements);
        const treeElement = this.createTreeElement(treeData);
        componentTree.appendChild(treeElement);

        // Update component count
        const componentCount = renderJson.elements.length;
        document.getElementById('infoComponents').textContent = componentCount;
        document.getElementById('elementCount').textContent = componentCount;
    }

    buildTreeData(elements) {
        const tree = [];

        elements.forEach(element => {
            const node = {
                id: element.id,
                type: element.type,
                name: this.getElementDisplayName(element),
                bounds: element.bounds,
                styles: element.styles,
                hasChildren: element.nestedElements && element.nestedElements.length > 0,
                children: []
            };

            // Add nested elements as children
            if (element.nestedElements && element.nestedElements.length > 0) {
                node.children = this.buildTreeData(element.nestedElements);
            }

            tree.push(node);
        });

        return tree;
    }

    createTreeElement(treeData) {
        const fragment = document.createDocumentFragment();

        treeData.forEach(node => {
            const treeNode = document.createElement('div');
            treeNode.className = 'tree-node';
            treeNode.dataset.elementId = node.id;

            // Create node content
            const nodeContent = document.createElement('div');
            nodeContent.className = 'tree-node-content';

            // Add expand/collapse toggle if has children
            if (node.hasChildren) {
                const toggle = document.createElement('button');
                toggle.className = 'tree-node-toggle';
                toggle.setAttribute('aria-expanded', 'true');
                toggle.innerHTML = `
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                `;

                toggle.addEventListener('click', () => {
                    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
                    toggle.setAttribute('aria-expanded', !isExpanded);
                    const children = treeNode.querySelector('.tree-node-children');
                    if (children) {
                        children.hidden = isExpanded;
                    }
                });

                nodeContent.appendChild(toggle);
            } else {
                const spacer = document.createElement('div');
                spacer.style.width = '20px';
                nodeContent.appendChild(spacer);
            }

            // Add element icon
            const icon = document.createElement('div');
            icon.className = 'tree-node-icon';
            icon.innerHTML = this.getElementIcon(node.type);
            nodeContent.appendChild(icon);

            // Add element name
            const name = document.createElement('div');
            name.className = 'tree-node-name';
            name.textContent = node.name;
            nodeContent.appendChild(name);

            // Add element info
            const info = document.createElement('div');
            info.className = 'tree-node-info';
            info.textContent = `${node.type} (${Math.round(node.bounds.width)}×${Math.round(node.bounds.height)})`;
            nodeContent.appendChild(info);

            treeNode.appendChild(nodeContent);

            // Add children if any
            if (node.hasChildren && node.children.length > 0) {
                const childrenContainer = document.createElement('div');
                childrenContainer.className = 'tree-node-children';
                const childrenElement = this.createTreeElement(node.children);
                childrenContainer.appendChild(childrenElement);
                treeNode.appendChild(childrenContainer);
            }

            fragment.appendChild(treeNode);
        });

        return fragment;
    }

    getElementDisplayName(element) {
        // Generate a readable name for the element
        if (element.type === 'rectangle' && element.styles?.backgroundColor) {
            return 'Background';
        } else if (element.type === 'rounded-rectangle') {
            return 'Container';
        } else if (element.type === 'text') {
            const text = element.content?.properties?.text || 'Text';
            return text.length > 15 ? text.substring(0, 15) + '...' : text;
        } else if (element.type === 'input-field') {
            return 'Input Field';
        } else if (element.type === 'button') {
            const text = element.content?.properties?.text || 'Button';
            return text.length > 15 ? text.substring(0, 15) + '...' : text;
        }

        // Fallback: capitalize and format type name
        return element.type.split('-').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    getElementIcon(type) {
        const icons = {
            'rectangle': '<rect x="4" y="4" width="16" height="16" rx="1" stroke="currentColor" fill="none" stroke-width="2"/>',
            'rounded-rectangle': '<rect x="4" y="4" width="16" height="16" rx="4" stroke="currentColor" fill="none" stroke-width="2"/>',
            'text': '<text x="12" y="14" text-anchor="middle" font-size="10" fill="currentColor">T</text>',
            'input-field': '<path d="M4 8h16M4 12h16M4 16h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
            'button': '<rect x="4" y="6" width="16" height="12" rx="2" stroke="currentColor" fill="none" stroke-width="2"/>'
        };

        return icons[type] || '<circle cx="12" cy="12" r="8" stroke="currentColor" fill="none" stroke-width="2"/>';
    }

    updateMetrics() {
        // Update performance metrics
        const renderTime = Math.random() * 20 + 5; // Mock render time
        const memoryUsage = (Math.random() * 2 + 1).toFixed(1);

        document.getElementById('renderTime').textContent = `${renderTime.toFixed(1)}ms`;
        document.getElementById('memoryUsage').textContent = `${memoryUsage}MB`;
        document.getElementById('tokensResolved').textContent = '24';
    }

    addErrorLogEntry(message) {
        const errorLog = document.getElementById('errorLog');
        const entry = document.createElement('div');
        entry.className = 'log-entry error';
        entry.innerHTML = `<span class="log-message">${message}</span>`;
        errorLog.appendChild(entry);
    }

    showTemporaryMessage(message) {
        // Create a temporary toast notification
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            box-shadow: var(--shadow-md);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    handleKeyboardShortcut(e) {
        // Keyboard shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'r':
                    e.preventDefault();
                    this.refreshCurrentScreen();
                    break;
                case 's':
                    e.preventDefault();
                    this.downloadCanvas();
                    break;
                case '=':
                case '+':
                    e.preventDefault();
                    this.zoom(0.1);
                    break;
                case '-':
                    e.preventDefault();
                    this.zoom(-0.1);
                    break;
                case '0':
                    e.preventDefault();
                    this.zoomToFit();
                    break;
            }
        }

        switch (e.key) {
            case 'Escape':
                this.zoomToFit();
                break;
            case 'ArrowLeft':
            case 'ArrowRight':
                if (!e.target.matches('input, select, textarea')) {
                    e.preventDefault();
                    this.navigateScreen(e.key === 'ArrowRight' ? 1 : -1);
                }
                break;
        }
    }

    navigateScreen(direction) {
        const allScreens = Array.from(document.querySelectorAll('.tree-item[data-screen]'));
        const currentIndex = allScreens.findIndex(item =>
            item.dataset.screen === this.state.currentScreen);

        const newIndex = Math.max(0, Math.min(allScreens.length - 1, currentIndex + direction));
        const newScreen = allScreens[newIndex].dataset.screen;

        if (newScreen !== this.state.currentScreen) {
            this.selectScreen(newScreen);
        }
    }

    render(state) {
        // React to state changes
        // This is called whenever the state is updated
    }
}

// =========================
// INITIALIZATION
// =========================
document.addEventListener('DOMContentLoaded', () => {
    const app = new CanvasRendererApp();

    // Make app globally available for debugging
    window.canvasApp = app;

    console.log('SimFlo Canvas Renderer initialized');
});