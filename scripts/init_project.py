#!/usr/bin/env python3
"""
Vite React Project Initialization Script
Creates a new project with TypeScript, React, ShadCN, Tailwind, Vitest, and Playwright
Supports enhanced automation with dashboard blocks, branding, and enterprise features.
"""

import argparse
import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import tempfile
import platform


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class ProjectInitializer:
    """Main class for project initialization with enhanced automation capabilities"""

    def __init__(self, project_name: str, options: Dict[str, Any]):
        self.project_name = project_name
        self.options = options
        self.project_path = Path.cwd() / project_name
        self.templates_dir = Path(__file__).parent / "templates"
        self.config_dir = Path(__file__).parent / "config"

    def log(self, message: str, color: str = Colors.NC):
        """Log colored message to console"""
        print(f"{color}{message}{Colors.NC}")

    def run_command(self, command: List[str], cwd: Optional[Path] = None,
                   capture_output: bool = False) -> subprocess.CompletedProcess:
        """Run shell command with proper error handling"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                capture_output=capture_output,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {' '.join(command)}", Colors.RED)
            self.log(f"Error: {e.stderr if e.stderr else str(e)}", Colors.RED)
            raise

    def check_node_version(self) -> bool:
        """Check if Node.js version is compatible"""
        try:
            result = self.run_command(["node", "--version"], capture_output=True)
            version_str = result.stdout.strip()
            major_version = int(version_str[1:].split('.')[0])
            minor_version = int(version_str[1:].split('.')[1])

            # Check for Node 20.18.0+ compatibility
            if major_version > 20 or (major_version == 20 and minor_version >= 18):
                return True
            else:
                self.log(f"Warning: Node.js version {version_str} may have compatibility issues", Colors.YELLOW)
                self.log("Consider upgrading to Node.js 20.18.0+", Colors.YELLOW)
                return False
        except (subprocess.CalledProcessError, ValueError):
            self.log("Could not determine Node.js version", Colors.YELLOW)
            return False

    def create_project_directory(self):
        """Create project directory if it doesn't exist"""
        if self.project_path.exists():
            self.log(f"Error: Directory '{self.project_name}' already exists", Colors.RED)
            sys.exit(1)

        self.project_path.mkdir(parents=True, exist_ok=True)
        os.chdir(self.project_path)
        self.log(f"Created project directory: {self.project_path}", Colors.GREEN)

    def setup_vite_project(self):
        """Initialize Vite project with React + TypeScript"""
        self.log("📦 Creating Vite project with React + TypeScript...", Colors.YELLOW)

        # Use specific version to avoid Node.js compatibility issues (Node 20.18.0 support)
        self.run_command(["npm", "create", "vite@6.5.0", ".", "--", "--template", "react-ts"])

    def install_dependencies(self):
        """Install core dependencies"""
        self.log("📋 Installing project dependencies...", Colors.YELLOW)
        self.run_command(["npm", "install"])

    def setup_tailwind(self):
        """Setup Tailwind CSS with ShadCN-compatible configuration"""
        self.log("🎨 Installing Tailwind CSS...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "tailwindcss", "postcss", "autoprefixer", "tailwindcss-animate"])

        # Create tailwind.config.js
        tailwind_config = self.generate_tailwind_config()
        with open("tailwind.config.js", "w") as f:
            f.write(tailwind_config)

    def setup_shadcn(self):
        """Setup ShadCN UI with dashboard configuration"""
        if self.options.get("dashboard"):
            self.log("⚡ Setting up ShadCN with dashboard configuration...", Colors.YELLOW)

            # Install ShadCN CLI
            self.run_command(["npm", "install", "-D", "@shadcn/ui"])

            # Initialize ShadCN with dashboard config
            shadcn_config = self.generate_shadcn_config()
            with open("components.json", "w") as f:
                json.dump(shadcn_config, f, indent=2)

            # Install dashboard blocks
            if self.options.get("dashboard"):
                self.install_dashboard_blocks()

    def install_dashboard_blocks(self):
        """Install ShadCN dashboard blocks"""
        blocks = ["dashboard-01", "sidebar-07", "login-03", "data-tables"]

        for block in blocks:
            try:
                self.log(f"Installing {block} block...", Colors.YELLOW)
                self.run_command(["npx", "shadcn@latest", "add", block])
            except subprocess.CalledProcessError:
                self.log(f"Warning: Could not install {block} block", Colors.YELLOW)
                continue

    def setup_testing(self):
        """Setup Vitest and Playwright for testing"""
        self.log("🧪 Installing Vitest for testing...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "vitest", "@vitest/ui", "jsdom",
                         "@testing-library/react", "@testing-library/jest-dom",
                         "@testing-library/user-event"])

        self.log("🎭 Installing Playwright for E2E testing...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "@playwright/test"])

        # Create test configurations
        self.create_test_configs()

    def setup_code_quality(self):
        """Setup ESLint, Prettier, and Husky"""
        self.log("🔧 Setting up ESLint and Prettier...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "eslint", "@typescript-eslint/eslint-plugin",
                         "@typescript-eslint/parser", "eslint-plugin-react", "eslint-plugin-react-hooks",
                         "eslint-config-prettier", "eslint-plugin-prettier", "prettier"])

        self.log("📊 Installing Husky for git hooks...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "husky", "lint-staged"])

    def setup_additional_dependencies(self):
        """Install additional useful dependencies"""
        self.log("🔧 Installing additional development dependencies...", Colors.YELLOW)
        self.run_command(["npm", "install", "-D", "@types/node", "vite-tsconfig-paths", "vite-plugin-pwa"])

        self.log("📱 Installing React Router and other useful libraries...", Colors.YELLOW)
        self.run_command(["npm", "install", "react-router-dom", "@types/react-router-dom"])
        self.run_command(["npm", "install", "zustand"])  # For state management
        self.run_command(["npm", "install", "axios"])  # For API calls
        self.run_command(["npm", "install", "@tanstack/react-query"])  # For data fetching
        self.run_command(["npm", "install", "clsx", "tailwind-merge", "class-variance-authority"])  # For utility classes
        self.run_command(["npm", "install", "lucide-react"])  # For icons

    def create_project_structure(self):
        """Create basic project structure"""
        self.log("📝 Creating project structure...", Colors.YELLOW)

        # Create directories
        directories = [
            "src/components",
            "src/components/ui",
            "src/components/__tests__",
            "src/lib",
            "src/hooks",
            "src/types",
            "src/config",
            "src/test",
            "e2e"
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def create_configuration_files(self):
        """Create configuration files"""
        self.log("📝 Creating configuration files...", Colors.YELLOW)

        # Create global CSS
        with open("src/index.css", "w") as f:
            f.write(self.generate_global_css())

        # Create utils
        with open("src/lib/utils.ts", "w") as f:
            f.write(self.generate_utils())

        # Create sample Button component
        with open("src/components/Button.tsx", "w") as f:
            f.write(self.generate_button_component())

        # Create configuration files
        self.create_vitest_config()
        self.create_eslint_config()
        self.create_prettier_config()
        self.create_playwright_config()
        self.create_gitignore()

    def update_package_json(self):
        """Update package.json with additional scripts"""
        self.log("📝 Updating package.json scripts...", Colors.YELLOW)

        scripts = {
            "test": "vitest",
            "test:ui": "vitest --ui",
            "test:run": "vitest run",
            "e2e": "playwright test",
            "e2e:ui": "playwright test --ui",
            "e2e:install": "playwright install",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "format": "prettier --write .",
            "format:check": "prettier --check ."
        }

        # Update package.json using npm pkg command
        for script_name, script_command in scripts.items():
            self.run_command(["npm", "pkg", "set", f"scripts.{script_name}={script_command}"])

    def setup_husky(self):
        """Setup Husky git hooks"""
        self.log("📝 Setting up husky hooks...", Colors.YELLOW)

        # Create husky directory and pre-commit hook
        Path(".husky").mkdir(exist_ok=True)
        with open(".husky/pre-commit", "w") as f:
            f.write("npx lint-staged\n")

        # Make pre-commit hook executable
        if platform.system() != "Windows":
            os.chmod(".husky/pre-commit", 0o755)

        # Configure lint-staged
        lint_staged_config = {
            "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
            "*.{json,md,yml,yaml}": ["prettier --write"]
        }

        with open("package.json", "r+") as f:
            package_data = json.load(f)
            package_data["lint-staged"] = lint_staged_config
            f.seek(0)
            json.dump(package_data, f, indent=2)
            f.truncate()

    def setup_branding(self):
        """Setup branding and design tokens if requested"""
        if self.options.get("brand"):
            self.log("🎨 Setting up branding and design tokens...", Colors.YELLOW)
            self.create_design_tokens()

    def setup_themes(self):
        """Setup multi-theme support if requested"""
        if self.options.get("themes"):
            self.log("🌈 Setting up multi-theme support...", Colors.YELLOW)
            self.create_theme_system()

    def create_design_tokens(self):
        """Create design tokens based on brand configuration"""
        brand_name = self.options.get("brand", "MyCompany")
        colors = self.options.get("colors", ["#3B82F6", "#10B981", "#F59E0B"])

        # Create tokens directory
        tokens_dir = Path("src/tokens")
        tokens_dir.mkdir(exist_ok=True)

        # Create color tokens
        colors_content = self.generate_color_tokens(colors)
        with open(tokens_dir / "colors.ts", "w") as f:
            f.write(colors_content)

        # Create other token files
        with open(tokens_dir / "typography.ts", "w") as f:
            f.write(self.generate_typography_tokens())

        with open(tokens_dir / "spacing.ts", "w") as f:
            f.write(self.generate_spacing_tokens())

    def create_theme_system(self):
        """Create theme provider and system"""
        themes = self.options.get("themes", ["light", "dark"]).split(",")
        default_theme = self.options.get("default_theme", "light")

        # Create theme provider
        with open("src/components/ui/theme-provider.tsx", "w") as f:
            f.write(self.generate_theme_provider(themes, default_theme))

    def initialize(self):
        """Main initialization method"""
        self.log(f"🚀 Initializing Vite React project: {self.project_name}", Colors.BLUE)

        # Check Node.js version
        self.check_node_version()

        # Create project directory
        self.create_project_directory()

        # Setup basic project
        self.setup_vite_project()
        self.install_dependencies()
        self.setup_tailwind()
        self.setup_shadcn()
        self.setup_testing()
        self.setup_code_quality()
        self.setup_additional_dependencies()

        # Create project structure and configuration
        self.create_project_structure()
        self.create_configuration_files()
        self.create_sample_tests()
        self.update_package_json()
        self.setup_husky()

        # Setup enhanced features
        self.setup_branding()
        self.setup_themes()

        # Create dashboard structure if requested
        if self.options.get("dashboard"):
            self.create_dashboard_structure()

        # Generate templates
        self.generate_templates()

        self.log_completion_message()

    def create_dashboard_structure(self):
        """Create dashboard-specific project structure"""
        self.log("📊 Creating dashboard project structure...", Colors.YELLOW)

        # Create dashboard directories
        dashboard_dirs = [
            "src/blocks/dashboard",
            "src/blocks/sidebar",
            "src/blocks/login",
            "src/blocks/data-tables",
            "src/hooks/auth",
            "src/hooks/navigation",
            "src/config/navigation"
        ]

        for directory in dashboard_dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)

        # Create basic dashboard files
        self.create_dashboard_configs()

    def create_dashboard_configs(self):
        """Create dashboard configuration files"""
        # Navigation config
        nav_config = {
            "main": [
                {"name": "Dashboard", "href": "/dashboard", "icon": "LayoutDashboard"},
                {"name": "Analytics", "href": "/analytics", "icon": "BarChart3"},
                {"name": "Settings", "href": "/settings", "icon": "Settings"}
            ],
            "admin": [
                {"name": "Users", "href": "/admin/users", "icon": "Users"},
                {"name": "System", "href": "/admin/system", "icon": "Server"}
            ]
        }

        with open("src/config/navigation.ts", "w") as f:
            f.write(f"export const navigationConfig = {json.dumps(nav_config, indent=2)}\n")

    def log_completion_message(self):
        """Log completion message with next steps"""
        self.log("✅ Project initialization complete!", Colors.GREEN)
        self.log("", Colors.NC)
        self.log("📋 Next steps:", Colors.BLUE)
        self.log(f"1. cd {self.project_name}", Colors.YELLOW)
        self.log("2. npx playwright install", Colors.YELLOW)
        self.log("3. npm run dev", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("🚀 Available commands:", Colors.BLUE)
        self.log("• npm run dev          - Start development server", Colors.YELLOW)
        self.log("• npm run build        - Build for production", Colors.YELLOW)
        self.log("• npm run test          - Run unit tests", Colors.YELLOW)
        self.log("• npm run test:ui      - Run unit tests with UI", Colors.YELLOW)
        self.log("• npm run e2e          - Run e2e tests", Colors.YELLOW)
        self.log("• npm run e2e:ui       - Run e2e tests with UI", Colors.YELLOW)
        self.log("• npm run lint          - Run ESLint", Colors.YELLOW)
        self.log("• npm run format        - Format code with Prettier", Colors.YELLOW)
        self.log("", Colors.NC)
        self.log("🎉 Happy coding!", Colors.GREEN)

    # Generator methods for configuration files
    def generate_tailwind_config(self) -> str:
        """Generate Tailwind CSS configuration"""
        return '''/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}'''

    def generate_shadcn_config(self) -> Dict[str, Any]:
        """Generate ShadCN configuration"""
        return {
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
                "components": "src/components",
                "utils": "src/lib/utils"
            }
        }

    def generate_global_css(self) -> str:
        """Generate global CSS with theme variables"""
        return '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 84% 4.9%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 94.1%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}'''

    def generate_utils(self) -> str:
        """Generate utility functions"""
        return '''import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}'''

    def generate_button_component(self) -> str:
        """Generate sample Button component"""
        return '''import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }'''

    def create_vitest_config(self):
        """Create Vitest configuration"""
        vitest_config = '''import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})'''

        with open("vitest.config.ts", "w") as f:
            f.write(vitest_config)

        # Create test setup file
        test_setup = '''import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))'''

        with open("src/test/setup.ts", "w") as f:
            f.write(test_setup)

    def create_eslint_config(self):
        """Create ESLint configuration"""
        eslint_config = '''module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
}'''

        with open(".eslintrc.js", "w") as f:
            f.write(eslint_config)

    def create_prettier_config(self):
        """Create Prettier configuration"""
        prettier_config = '''{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}'''

        with open(".prettierrc", "w") as f:
            f.write(prettier_config)

    def create_playwright_config(self):
        """Create Playwright configuration"""
        playwright_config = '''import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
})'''

        with open("playwright.config.ts", "w") as f:
            f.write(playwright_config)

    def create_sample_tests(self):
        """Create sample test files"""
        # Component test
        component_test = '''import { render, screen } from '@testing-library/react'
import { Button } from '../Button'

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('applies variant classes', () => {
    render(<Button variant="destructive">Delete</Button>)
    const button = screen.getByText('Delete')
    expect(button).toHaveClass('bg-destructive')
  })
})'''

        with open("src/components/__tests__/Button.test.tsx", "w") as f:
            f.write(component_test)

        # E2E test
        e2e_test = '''import { test, expect } from '@playwright/test'

test('homepage has correct title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/Vite [+][+] React/)
})

test('counter works correctly', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('button')).toHaveText('count is 0')
  await page.locator('button').click()
  await expect(page.locator('button')).toHaveText('count is 1')
})'''

        with open("e2e/example.spec.ts", "w") as f:
            f.write(e2e_test)

    def create_gitignore(self):
        """Create .gitignore file"""
        gitignore_content = '''# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Playwright
test-results/
playwright-report/
playwright/.cache/

# Coverage
coverage/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local'''

        with open(".gitignore", "w") as f:
            f.write(gitignore_content)

    def generate_color_tokens(self, colors: List[str]) -> str:
        """Generate color tokens from brand colors"""
        return f'''// Color tokens generated from brand colors: {colors}
export const colors = {{
  primary: {{
    50: '{colors[0]}08',
    100: '{colors[0]}15',
    500: '{colors[0]}',
    600: '{colors[0]}dd',
    700: '{colors[0]}bb',
  }},
  secondary: {{
    50: '{colors[1] if len(colors) > 1 else '#10B981'}08',
    100: '{colors[1] if len(colors) > 1 else '#10B981'}15',
    500: '{colors[1] if len(colors) > 1 else '#10B981'}',
    600: '{colors[1] if len(colors) > 1 else '#10B981'}dd',
    700: '{colors[1] if len(colors) > 1 else '#10B981'}bb',
  }},
  accent: {{
    50: '{colors[2] if len(colors) > 2 else '#F59E0B'}08',
    100: '{colors[2] if len(colors) > 2 else '#F59E0B'}15',
    500: '{colors[2] if len(colors) > 2 else '#F59E0B'}',
    600: '{colors[2] if len(colors) > 2 else '#F59E0B'}dd',
    700: '{colors[2] if len(colors) > 2 else '#F59E0B'}bb',
  }},
}}'''

    def generate_typography_tokens(self) -> str:
        """Generate typography tokens"""
        return '''// Typography tokens
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'Consolas', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem',
  },
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  lineHeight: {
    tight: '1.25',
    snug: '1.375',
    normal: '1.5',
    relaxed: '1.625',
    loose: '2',
  },
}'''

    def generate_spacing_tokens(self) -> str:
        """Generate spacing tokens"""
        return '''// Spacing tokens
export const spacing = {
  px: '1px',
  0: '0',
  1: '0.25rem',
  2: '0.5rem',
  3: '0.75rem',
  4: '1rem',
  5: '1.25rem',
  6: '1.5rem',
  8: '2rem',
  10: '2.5rem',
  12: '3rem',
  16: '4rem',
  20: '5rem',
  24: '6rem',
}'''

    def generate_theme_provider(self, themes: List[str], default_theme: str) -> str:
        """Generate theme provider component"""
        return '''import React, { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

type ThemeProviderProps = {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

type ThemeProviderState = {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const initialState: ThemeProviderState = {
  theme: 'system',
  setTheme: () => null,
}

const ThemeProviderContext = createContext<ThemeProviderState>(initialState)

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'vite-ui-theme',
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  )

  useEffect(() => {
    const root = window.document.documentElement

    root.classList.remove('light', 'dark')

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)')
        .matches
        ? 'dark'
        : 'light'

      root.classList.add(systemTheme)
      return
    }

    root.classList.add(theme)
  }, [theme])

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext)

  if (context === undefined)
    throw new Error('useTheme must be used within a ThemeProvider')

  return context
}'''

    def generate_templates(self):
        """Generate templates from template directory"""
        if self.options.get("dashboard"):
            self.log("📝 Generating dashboard templates...", Colors.YELLOW)

            # Look for templates in multiple locations
            template_locations = [
                self.templates_dir,  # Default location
                Path(__file__).parent.parent / "templates",  # Parent directory
                Path.cwd().parent / "templates",  # Current working directory parent
            ]

            templates_found = False
            for templates_dir in template_locations:
                if templates_dir.exists():
                    self.log(f"📁 Found templates in: {templates_dir}", Colors.YELLOW)
                    self.copy_templates(templates_dir)
                    templates_found = True
                    break

            if not templates_found:
                self.log("⚠️  Templates directory not found, skipping template generation", Colors.YELLOW)
                self.log("💡 Create templates directory to enable template generation", Colors.YELLOW)

    def copy_templates(self, templates_dir: Path):
        """Copy templates to project directory"""
        import shutil

        # Copy component templates
        components_src = templates_dir / "components"
        components_dest = Path("src/components")
        if components_src.exists():
            for template_file in components_src.rglob("*.tsx"):
                relative_path = template_file.relative_to(components_src)
                dest_path = components_dest / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Process template with variable substitution
                template_content = template_file.read_text()
                processed_content = self.process_template(template_content)
                dest_path.write_text(processed_content)

        # Copy hook templates
        hooks_src = templates_dir / "hooks"
        hooks_dest = Path("src/hooks")
        if hooks_src.exists():
            for template_file in hooks_src.rglob("*.ts"):
                relative_path = template_file.relative_to(hooks_src)
                dest_path = hooks_dest / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                template_content = template_file.read_text()
                processed_content = self.process_template(template_content)
                dest_path.write_text(processed_content)

        # Copy config templates
        config_src = templates_dir / "config"
        config_dest = Path("src/config")
        if config_src.exists():
            for template_file in config_src.rglob("*.ts"):
                relative_path = template_file.relative_to(config_src)
                dest_path = config_dest / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                template_content = template_file.read_text()
                processed_content = self.process_template(template_content)
                dest_path.write_text(processed_content)

        # Copy type templates
        types_src = templates_dir / "types"
        types_dest = Path("src/types")
        if types_src.exists():
            for template_file in types_src.rglob("*.ts"):
                relative_path = template_file.relative_to(types_src)
                dest_path = types_dest / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                template_content = template_file.read_text()
                processed_content = self.process_template(template_content)
                dest_path.write_text(processed_content)

    def process_template(self, content: str) -> str:
        """Process template content with variable substitution"""
        # Replace project-specific variables
        replacements = {
            "{{PROJECT_NAME}}": self.project_name,
            "{{BRAND_NAME}}": self.options.get("brand", "MyCompany"),
            "{{CURRENT_YEAR}}": "2025",
        }

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        return content

    def create_test_configs(self):
        """Create test configuration files (already handled in separate methods)"""
        pass


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Initialize Vite React project with enhanced automation"
    )
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("--dashboard", action="store_true", help="Setup dashboard with ShadCN blocks")
    parser.add_argument("--brand", help="Company name for branding")
    parser.add_argument("--colors", help="Brand colors (comma-separated hex values)")
    parser.add_argument("--themes", help="Theme options (comma-separated)")
    parser.add_argument("--default-theme", help="Default theme", default="system")

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Convert namespace to dict for options
    options = {
        "dashboard": args.dashboard,
        "brand": args.brand,
        "colors": args.colors.split(",") if args.colors else None,
        "themes": args.themes,
        "default_theme": args.default_theme
    }

    # Initialize project
    initializer = ProjectInitializer(args.project_name, options)
    initializer.initialize()


if __name__ == "__main__":
    main()