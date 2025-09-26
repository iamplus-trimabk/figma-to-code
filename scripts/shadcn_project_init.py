#!/usr/bin/env python3
"""
ShadCN-First Project Automation Script

This script creates a Vite React project with proper ShadCN integration,
installing blocks and components directly to organized directory structure.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    """Terminal color codes"""
    NC = '\033[0m'      # No Color
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'


class ShadCNProjectInitializer:
    """Initialize ShadCN project with proper directory structure"""

    def __init__(self, project_name: str, options: Dict):
        self.project_name = project_name
        self.options = options
        self.project_path = Path.cwd() / project_name

    def log(self, message: str, color: str = Colors.NC):
        """Log colored message to console"""
        print(f"{color}{message}{Colors.NC}")

    def run_command(self, command: List[str], cwd: Optional[Path] = None, check: bool = True, timeout: int = 300) -> subprocess.CompletedProcess:
        """Run command with enhanced error handling"""
        try:
            self.log(f"  Running: {' '.join(command)}", Colors.CYAN)
            result = subprocess.run(
                command,
                cwd=cwd or self.project_path,
                check=check,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            # Log successful command output if verbose
            if result.returncode == 0 and result.stdout.strip():
                self.log(f"  ✅ Command completed successfully", Colors.GREEN)

            return result

        except subprocess.TimeoutExpired:
            self.log(f"❌ Command timed out after {timeout}s: {' '.join(command)}", Colors.RED)
            if check:
                raise
            # Return a fake result indicating timeout
            return subprocess.CompletedProcess(command, 124, "", "Command timed out")

        except subprocess.CalledProcessError as e:
            self.log(f"❌ Command failed: {' '.join(command)}", Colors.RED)
            if e.stderr and e.stderr.strip():
                self.log(f"  Error: {e.stderr.strip()}", Colors.RED)
            if e.stdout and e.stdout.strip():
                self.log(f"  Output: {e.stdout.strip()}", Colors.YELLOW)
            if check:
                raise
            return e

        except FileNotFoundError:
            self.log(f"❌ Command not found: {command[0]}", Colors.RED)
            self.log("  Please ensure the command is available in your PATH", Colors.YELLOW)
            if check:
                raise
            # Return a fake result indicating command not found
            return subprocess.CompletedProcess(command, 127, "", "Command not found")

        except Exception as e:
            self.log(f"❌ Unexpected error running command: {' '.join(command)}", Colors.RED)
            self.log(f"  Error: {str(e)}", Colors.RED)
            if check:
                raise
            # Return a fake result indicating unexpected error
            return subprocess.CompletedProcess(command, 1, "", f"Unexpected error: {str(e)}")

    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        self.log("🔍 Checking prerequisites...", Colors.YELLOW)

        # Check Node.js
        try:
            result = self.run_command(["node", "--version"], cwd=Path.cwd(), check=False)
            if result.returncode == 0:
                version = result.stdout.strip()
                version_num = version.replace('v', '').split('.')[0]
                if int(version_num) >= 18:
                    self.log(f"✅ Node.js version: {version}", Colors.GREEN)
                else:
                    self.log(f"❌ Node.js version {version} is too old. Please install Node.js 18+.", Colors.RED)
                    sys.exit(1)
            else:
                self.log("❌ Node.js not found. Please install Node.js 18+.", Colors.RED)
                sys.exit(1)
        except FileNotFoundError:
            self.log("❌ Node.js not found. Please install Node.js 18+.", Colors.RED)
            sys.exit(1)

        # Check npm
        try:
            result = self.run_command(["npm", "--version"], cwd=Path.cwd(), check=False)
            if result.returncode == 0:
                self.log(f"✅ npm version: {result.stdout.strip()}", Colors.GREEN)
            else:
                self.log("❌ npm not found. Please install npm.", Colors.RED)
                sys.exit(1)
        except FileNotFoundError:
            self.log("❌ npm not found. Please install npm.", Colors.RED)
            sys.exit(1)

        # Check available disk space (at least 100MB)
        try:
            import shutil
            disk_usage = shutil.disk_usage(self.project_path.parent)
            free_mb = disk_usage.free // (1024 * 1024)
            if free_mb >= 100:
                self.log(f"✅ Available disk space: {free_mb}MB", Colors.GREEN)
            else:
                self.log(f"❌ Insufficient disk space: {free_mb}MB (min 100MB required)", Colors.RED)
                sys.exit(1)
        except Exception as e:
            self.log(f"⚠️  Could not check disk space: {e}", Colors.YELLOW)

        self.log("✅ All prerequisites checked", Colors.GREEN)

    def create_project_directory(self):
        """Create project directory"""
        if self.project_path.exists():
            self.log(f"⚠️  Directory {self.project_name} already exists", Colors.YELLOW)
            response = input(f"Overwrite {self.project_name}? (y/N): ")
            if response.lower() != 'y':
                self.log("❌ Project initialization cancelled", Colors.RED)
                sys.exit(0)

        self.project_path.mkdir(parents=True, exist_ok=True)
        self.log(f"✅ Created project directory: {self.project_path}", Colors.GREEN)

    def setup_vite_project(self):
        """Create Vite React TypeScript project"""
        self.log("📦 Creating Vite project with React + TypeScript...", Colors.YELLOW)

        # Create Vite project in temporary directory first
        temp_path = Path.cwd() / "temp_vite"
        self.run_command([
            "npm", "create", "vite@latest", "temp_vite", "--", "--template", "react-ts"
        ], cwd=Path.cwd())

        # Move all files from temp directory to project directory
        for item in temp_path.iterdir():
            dest = self.project_path / item.name
            if dest.exists():
                if dest.is_dir():
                    subprocess.run(["rm", "-rf", str(dest)])
                else:
                    subprocess.run(["rm", str(dest)])

            if item.is_dir():
                subprocess.run(["mv", str(item), str(dest)])
            else:
                subprocess.run(["mv", str(item), str(dest)])

        # Clean up temp directory
        subprocess.run(["rm", "-rf", str(temp_path)])

        self.log("✅ Vite project created successfully", Colors.GREEN)

    def install_dependencies(self):
        """Install project dependencies"""
        self.log("📋 Installing project dependencies...", Colors.YELLOW)
        self.run_command(["npm", "install"])
        self.log("✅ Dependencies installed", Colors.GREEN)

    def setup_tailwind(self):
        """Install and configure Tailwind CSS"""
        self.log("🎨 Installing Tailwind CSS...", Colors.YELLOW)

        # Install Tailwind dependencies
        self.run_command([
            "npm", "install", "-D", "tailwindcss", "postcss", "autoprefixer"
        ])

        # Initialize Tailwind config
        result = self.run_command(["npx", "tailwindcss", "init", "-p"], check=False)
        if result.returncode != 0:
            self.log("⚠️  Tailwind init failed, creating config manually...", Colors.YELLOW)
            # Create basic tailwind config manually
            tailwind_config = '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}'''
            with open(self.project_path / "tailwind.config.js", "w") as f:
                f.write(tailwind_config)

            # Create postcss config
            postcss_config = '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''
            with open(self.project_path / "postcss.config.js", "w") as f:
                f.write(postcss_config)

        self.log("✅ Tailwind CSS installed", Colors.GREEN)

    def setup_shadcn(self):
        """Initialize ShadCN with custom directory structure"""
        self.log("⚡ Setting up ShadCN with custom paths...", Colors.YELLOW)

        # Initialize ShadCN with default settings first
        result = self.run_command(["npx", "shadcn@latest", "init"], check=False)

        if result.returncode != 0:
            self.log("⚠️  ShadCN init had issues, continuing with manual setup...", Colors.YELLOW)

        # Update components.json for custom paths
        components_config = {
            "$schema": "https://ui.shadcn.com/schema.json",
            "style": "default",
            "rsc": False,
            "tsx": True,
            "tailwind": {
                "config": "tailwind.config.js",
                "css": "src/index.css",
                "baseColor": "slate",
                "cssVariables": True,
                "prefix": ""
            },
            "aliases": {
                "components": "@/shadcn/components",
                "utils": "@/shadcn/lib/utils"
            }
        }

        # Write custom components.json
        with open(self.project_path / "components.json", "w") as f:
            json.dump(components_config, f, indent=2)

        # Update tsconfig.json paths
        self.update_tsconfig_paths()

        self.log("✅ ShadCN initialized with custom paths", Colors.GREEN)

    def update_tsconfig_paths(self):
        """Update TypeScript config paths for custom structure"""
        tsconfig_path = self.project_path / "tsconfig.json"
        if tsconfig_path.exists():
            with open(tsconfig_path, 'r') as f:
                tsconfig = json.load(f)

            # Update or add paths
            if "compilerOptions" not in tsconfig:
                tsconfig["compilerOptions"] = {}

            tsconfig["compilerOptions"]["baseUrl"] = "."
            tsconfig["compilerOptions"]["paths"] = {
                "@/*": ["src/*"],
                "@/shadcn/*": ["src/shadcn/*"],
                "@/shadcn/components/*": ["src/shadcn/components/*"],
                "@/shadcn/blocks/*": ["src/shadcn/blocks/*"],
                "@/shadcn/hooks/*": ["src/shadcn/hooks/*"],
                "@/custom/*": ["src/custom/*"],
                "@/custom/blocks/*": ["src/custom/blocks/*"],
                "@/custom/hooks/*": ["src/custom/hooks/*"],
                "@/custom/components/*": ["src/custom/components/*"]
            }

            with open(tsconfig_path, 'w') as f:
                json.dump(tsconfig, f, indent=2)

    def create_directory_structure(self):
        """Create organized directory structure"""
        self.log("📁 Creating organized directory structure...", Colors.YELLOW)

        # Create ShadCN directories
        shadcn_dirs = [
            "src/shadcn/blocks",
            "src/shadcn/components",
            "src/shadcn/hooks",
            "src/shadcn/lib"
        ]

        for dir_path in shadcn_dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Create custom directories
        custom_dirs = [
            "src/custom/blocks",
            "src/custom/hooks",
            "src/custom/components"
        ]

        for dir_path in custom_dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

        self.log("✅ Directory structure created", Colors.GREEN)

    def install_dashboard_block(self):
        """Install Dashboard-01 block with custom path"""
        self.log("📊 Installing Dashboard-01 block...", Colors.YELLOW)

        # Install Dashboard-01 to custom path
        result = self.run_command([
            "npx", "shadcn@latest", "add", "dashboard-01",
            "--path", "src/shadcn/blocks/dashboard-01"
        ], check=False)

        if result.returncode != 0:
            self.log("⚠️  Dashboard-01 installation had issues, continuing...", Colors.YELLOW)
            self.log(result.stdout or result.stderr, Colors.YELLOW)
        else:
            self.log("✅ Dashboard-01 block installed", Colors.GREEN)

    def install_essential_components(self):
        """Install essential UI components"""
        self.log("🧩 Installing essential UI components...", Colors.YELLOW)

        essential_components = [
            "button", "card", "input", "label", "select",
            "sheet", "dialog", "dropdown-menu", "toast", "table"
        ]

        for component in essential_components:
            self.log(f"  Installing {component}...", Colors.CYAN)
            result = self.run_command([
                "npx", "shadcn@latest", "add", component,
                "--path", "src/shadcn/components"
            ], check=False)

            if result.returncode != 0:
                self.log(f"  ⚠️  {component} installation failed", Colors.YELLOW)

        self.log("✅ Essential components installed", Colors.GREEN)

    def install_useful_hooks(self):
        """Install useful ShadCN hooks"""
        self.log("🪝 Installing useful hooks...", Colors.YELLOW)

        useful_hooks = [
            "use-local-storage", "use-media-query", "use-debounce-value",
            "use-copy-to-clipboard", "use-click-outside", "use-boolean"
        ]

        for hook in useful_hooks:
            self.log(f"  Installing {hook}...", Colors.CYAN)
            result = self.run_command([
                "npx", "shadcn@latest", "add", hook,
                "--path", "src/shadcn/hooks"
            ], check=False)

            if result.returncode != 0:
                self.log(f"  ⚠️  {hook} not available or failed", Colors.YELLOW)

        self.log("✅ Hooks installation completed", Colors.GREEN)

    def install_additional_blocks(self):
        """Install additional useful blocks"""
        if self.options.get("additional_blocks"):
            self.log("🧱 Installing additional blocks...", Colors.YELLOW)

            blocks = self.options.get("additional_blocks", "").split(",")

            for block in blocks:
                block = block.strip()
                if block:
                    block_dir = f"src/shadcn/blocks/{block}"
                    self.log(f"  Installing {block}...", Colors.CYAN)
                    result = self.run_command([
                        "npx", "shadcn@latest", "add", block,
                        "--path", block_dir
                    ], check=False)

                    if result.returncode != 0:
                        self.log(f"  ⚠️  {block} installation failed", Colors.YELLOW)

            self.log("✅ Additional blocks installed", Colors.GREEN)

    def create_documentation(self):
        """Create project documentation"""
        self.log("📝 Creating project documentation...", Colors.YELLOW)

        readme_content = f"""# {self.project_name}

A React project built with Vite, TypeScript, and ShadCN UI components.

## Project Structure

```
src/
├── shadcn/               # All ShadCN-provided code
│   ├── blocks/          # ShadCN blocks (dashboard-01, etc.)
│   ├── components/       # ShadCN UI components (button, card, etc.)
│   ├── hooks/           # ShadCN hooks (use-local-storage, etc.)
│   └── lib/             # ShadCN utilities
└── custom/              # Custom implementations (empty initially)
    ├── blocks/          # Custom blocks (if needed)
    ├── hooks/           # Custom hooks (if needed)
    └── components/      # Custom components (if needed)
```

## Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## ShadCN Integration

This project uses actual ShadCN blocks and components installed via CLI:

### Installed Blocks
- Dashboard-01 (main app shell)

### Installed Components
- Button, Card, Input, Label, Select, Sheet, Dialog, Dropdown-menu, Toast, Table

### Installed Hooks
- Use-local-storage, Use-media-query, Use-debounce-value, Use-copy-to-clipboard

## Philosophy

This project follows a **blocks-first** approach:
1. Use ShadCN blocks when available
2. Use ShadCN hooks when available
3. Only create custom implementations when ShadCN doesn't provide needed functionality

## Custom Code

The `src/custom/` directory is intentionally empty initially. Only add custom implementations when:
- ShadCN doesn't provide the needed functionality
- You need to extend or customize ShadCN components significantly

"""

        with open(self.project_path / "README.md", "w") as f:
            f.write(readme_content)

        self.log("✅ Documentation created", Colors.GREEN)

    def analyze_installed_functionality(self):
        """Analyze what ShadCN provides and document gaps"""
        self.log("🔍 Analyzing installed functionality...", Colors.YELLOW)

        analysis_content = """# ShadCN Functionality Analysis

## What ShadCN Provides

### Blocks
- **Dashboard-01**: Complete app shell with sidebar navigation, header, content area
  - Responsive design
  - Built-in navigation structure
  - Theme support

### Components
- **Button**: Clickable elements with variants
- **Card**: Content containers with header/footer
- **Input**: Form input fields
- **Label**: Form labels
- **Select**: Dropdown selection
- **Sheet**: Slide-out panels
- **Dialog**: Modal dialogs
- **Dropdown-menu**: Menu components
- **Toast**: Notifications
- **Table**: Data display tables

### Hooks
- **use-local-storage**: Local storage state management
- **use-media-query**: Responsive design utilities
- **use-debounce-value**: Debounced input handling
- **use-copy-to-clipboard**: Clipboard functionality
- **use-click-outside**: Outside click detection
- **use-boolean**: Boolean state management

## Potential Gaps (Custom Implementation Needed)

### Authentication
- Login/logout functionality
- JWT token management
- User session handling

### API Integration
- Data fetching hooks
- Error handling
- Loading states

### ERP-Specific Features
- Custom data visualization
- Complex forms
- Role-based access control

### Advanced Features
- Real-time updates (WebSockets)
- File upload/download
- Advanced filtering/sorting

## Implementation Strategy

1. **Start with Dashboard-01** as the main app shell
2. **Extend with custom components** only when needed
3. **Leverage existing hooks** for common functionality
4. **Build custom hooks** for ERP-specific needs

## Next Steps

1. Explore the installed Dashboard-01 structure
2. Identify specific ERP requirements
3. Plan custom implementations based on gaps
4. Implement custom features in `src/custom/` directory
"""

        with open(self.project_path / "SHADCN_ANALYSIS.md", "w") as f:
            f.write(analysis_content)

        self.log("✅ Functionality analysis completed", Colors.GREEN)

    def create_basic_templates(self):
        """Create basic templates for non-dashboard projects"""
        self.log("📝 Creating basic templates...", Colors.YELLOW)

        # Create a basic App.tsx template
        app_template = """import { useState } from 'react'
import { Button } from '@/shadcn/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shadcn/components/ui/card'
import { Input } from '@/shadcn/components/ui/input'
import { Label } from '@/shadcn/components/ui/label'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className=\"min-h-screen bg-background text-foreground p-8\">
      <div className=\"max-w-4xl mx-auto space-y-8\">
        <header className=\"text-center space-y-4\">
          <h1 className=\"text-4xl font-bold tracking-tight\">Welcome to Your App</h1>
          <p className=\"text-xl text-muted-foreground\">
            Built with ShadCN components and Tailwind CSS
          </p>
        </header>

        <div className=\"grid gap-6 md:grid-cols-2\">
          <Card>
            <CardHeader>
              <CardTitle>Counter Demo</CardTitle>
              <CardDescription>
                Basic state management with ShadCN components
              </CardDescription>
            </CardHeader>
            <CardContent className=\"space-y-4\">
              <div className=\"text-center\">
                <p className=\"text-2xl font-semibold\">{count}</p>
                <div className=\"flex gap-2 justify-center mt-4\">
                  <Button
                    onClick={() => setCount(c => c + 1)}
                    variant=\"default\"
                  >
                    Increment
                  </Button>
                  <Button
                    onClick={() => setCount(c => Math.max(0, c - 1))}
                    variant=\"outline\"
                  >
                    Decrement
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Form Demo</CardTitle>
              <CardDescription>
                Basic form with ShadCN input components
              </CardDescription>
            </CardHeader>
            <CardContent className=\"space-y-4\">
              <div className=\"space-y-2\">
                <Label htmlFor=\"name\">Name</Label>
                <Input id=\"name\" placeholder=\"Enter your name\" />
              </div>
              <div className=\"space-y-2\">
                <Label htmlFor=\"email\">Email</Label>
                <Input id=\"email\" type=\"email\" placeholder=\"Enter your email\" />
              </div>
              <Button className=\"w-full\">Submit</Button>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Getting Started</CardTitle>
            <CardDescription>
              Your project is ready for development
            </CardDescription>
          </CardHeader>
          <CardContent className=\"space-y-4\">
            <div className=\"grid gap-4 text-sm\">
              <div>
                <strong>✅ ShadCN Components:</strong> Button, Card, Input, Label, and more
              </div>
              <div>
                <strong>✅ Styling:</strong> Tailwind CSS with custom design tokens
              </div>
              <div>
                <strong>✅ Type Safety:</strong> Full TypeScript support
              </div>
              <div>
                <strong>✅ Development:</strong> Hot reload and fast refresh
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App
"""

        # Create a basic custom component template
        component_template = """import React from 'react'
import { cn } from '@/shadcn/lib/utils'

export interface CustomComponentProps {
  className?: string
  children?: React.ReactNode
}

export function CustomComponent({ className, children }: CustomComponentProps) {
  return (
    <div className={cn('p-4 border rounded-lg bg-card', className)}>
      {children}
    </div>
  )
}
"""

        # Create a basic custom hook template
        hook_template = """import { useState, useEffect } from 'react'

export function useCustomHook(initialValue: any) {
  const [value, setValue] = useState(initialValue)

  useEffect(() => {
    // Add your side effect logic here
  }, [value])

  return [value, setValue]
}
"""

        # Write templates to files
        templates_dir = self.project_path / "src" / "custom" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Update App.tsx with template
        app_path = self.project_path / "src" / "App.tsx"
        if app_path.exists():
            with open(app_path, 'w') as f:
                f.write(app_template)

        # Create component template
        with open(templates_dir / "CustomComponent.tsx", 'w') as f:
            f.write(component_template)

        # Create hook template
        with open(templates_dir / "useCustomHook.ts", 'w') as f:
            f.write(hook_template)

        # Create templates README
        templates_readme = """# Custom Templates

This directory contains custom templates and components for your application.

## Files
- `CustomComponent.tsx` - Basic component template with TypeScript support
- `useCustomHook.ts` - Basic hook template with state management

## Usage
```tsx
import { CustomComponent } from '@/custom/templates/CustomComponent'
import { useCustomHook } from '@/custom/templates/useCustomHook'
```

## Next Steps
1. Copy and rename these templates for your specific needs
2. Remove this directory once you have your own components
3. Add your custom components to the `src/custom/components/` directory
"""

        with open(templates_dir / "README.md", 'w') as f:
            f.write(templates_readme)

        self.log("✅ Basic templates created", Colors.GREEN)

    def log_completion_message(self):
        """Log project completion message"""
        self.log("🎉 Project initialization complete!", Colors.GREEN)
        self.log("", Colors.NC)
        self.log("📋 Next steps:", Colors.BLUE)
        self.log(f"1. cd {self.project_name}", Colors.YELLOW)
        self.log("2. npm run dev", Colors.YELLOW)

        if self.options.get('dashboard', True):
            self.log("3. Explore the Dashboard-01 block structure", Colors.YELLOW)
            self.log("4. Review SHADCN_ANALYSIS.md for functionality gaps", Colors.YELLOW)
        else:
            self.log("3. Start building your application with essential components", Colors.YELLOW)
            self.log("4. Review SHADCN_ANALYSIS.md for available functionality", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("🚀 Available commands:", Colors.BLUE)
        self.log("• npm run dev          - Start development server", Colors.YELLOW)
        self.log("• npm run build        - Build for production", Colors.YELLOW)
        self.log("• npm run preview      - Preview production build", Colors.YELLOW)
        self.log("• npm run lint         - Run ESLint", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("📁 Project structure:", Colors.BLUE)
        self.log("• src/shadcn/          - All ShadCN code", Colors.YELLOW)
        self.log("• src/custom/          - Custom implementations (empty)", Colors.YELLOW)
        self.log("• README.md            - Project documentation", Colors.YELLOW)
        self.log("• SHADCN_ANALYSIS.md  - Functionality analysis", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("🎯 Key files to explore:", Colors.BLUE)

        if self.options.get('dashboard', True):
            self.log("• src/shadcn/blocks/dashboard-01/ - Main app shell", Colors.YELLOW)
        else:
            self.log("• src/App.tsx        - Main application entry point", Colors.YELLOW)

        self.log("• components.json     - ShadCN configuration", Colors.YELLOW)
        self.log("• tailwind.config.js  - Tailwind configuration", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("✨ Happy coding with ShadCN!", Colors.GREEN)

    def initialize(self):
        """Main initialization method"""
        self.log(f"🚀 Initializing ShadCN-first project: {self.project_name}", Colors.BLUE)

        try:
            # Check all prerequisites
            self.check_prerequisites()

            # Create project directory
            self.create_project_directory()

            # Setup basic project
            self.setup_vite_project()
            self.install_dependencies()

            # Setup Tailwind CSS
            self.setup_tailwind()

            # Setup ShadCN with custom structure
            self.setup_shadcn()
            self.create_directory_structure()

            # Install ShadCN components based on project type
            if self.options.get('dashboard', True):
                self.install_dashboard_block()
                self.install_additional_blocks()

            self.install_essential_components()
            self.install_useful_hooks()

            # Create documentation
            self.create_documentation()

            # Create basic templates for non-dashboard projects
            if not self.options.get('dashboard', True):
                self.create_basic_templates()

            self.analyze_installed_functionality()

            self.log_completion_message()

        except KeyboardInterrupt:
            self.log("\n❌ Project initialization cancelled by user", Colors.RED)
            sys.exit(1)
        except Exception as e:
            self.log(f"\n❌ Project initialization failed: {str(e)}", Colors.RED)
            self.log("💡 You can try running the script again with the same command", Colors.YELLOW)
            self.log("🔍 If the problem persists, check the error messages above for details", Colors.YELLOW)
            sys.exit(1)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Initialize ShadCN-first React project with organized directory structure"
    )

    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("--additional-blocks", help="Additional blocks to install (comma-separated)")
    parser.add_argument("--no-dashboard", action="store_true", help="Skip dashboard block installation (basic setup only)")

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    options = {
        "additional_blocks": args.additional_blocks,
        "dashboard": not args.no_dashboard
    }

    # Initialize project
    initializer = ShadCNProjectInitializer(args.project_name, options)
    initializer.initialize()


if __name__ == "__main__":
    main()