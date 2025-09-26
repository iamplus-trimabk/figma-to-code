#!/bin/bash

# Vite React Project Initialization Script
# Creates a new project with TypeScript, React, ShadCN, Tailwind, Vitest, and Playwright

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME=${1:-vite-react-app}

echo -e "${BLUE}🚀 Initializing Vite React project: ${PROJECT_NAME}${NC}"

# Check if project directory already exists
if [ -d "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: Directory '$PROJECT_NAME' already exists${NC}"
    exit 1
fi

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

echo -e "${YELLOW}📦 Creating Vite project with React + TypeScript...${NC}"
# Use specific version to avoid Node.js compatibility issues
npm create vite@5.4.8 . -- --template react-ts

echo -e "${YELLOW}📋 Installing project dependencies...${NC}"
npm install

echo -e "${YELLOW}🎨 Installing Tailwind CSS...${NC}"
npm install -D tailwindcss postcss autoprefixer tailwindcss-animate

echo -e "${YELLOW}⚡ Setting up ShadCN...${NC}"
# Skip ShadCN for now due to compatibility issues - can be added manually later
echo -e "${YELLOW}⚠️  Skipping ShadCN setup due to compatibility issues${NC}"
echo -e "${YELLOW}💡 You can add ShadCN later with: npm install -D @shadcn/ui && npx shadcn@latest init${NC}"

echo -e "${YELLOW}🧪 Installing Vitest for testing...${NC}"
npm install -D vitest @vitest/ui jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event

echo -e "${YELLOW}🎭 Installing Playwright for E2E testing...${NC}"
npm install -D @playwright/test

echo -e "${YELLOW}🔧 Setting up ESLint and Prettier...${NC}"
npm install -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-react eslint-plugin-react-hooks eslint-config-prettier eslint-plugin-prettier prettier

echo -e "${YELLOW}📊 Installing Husky for git hooks...${NC}"
npm install -D husky lint-staged

echo -e "${YELLOW}🔧 Installing additional development dependencies...${NC}"
npm install -D @types/node vite-tsconfig-paths vite-plugin-pwa

echo -e "${YELLOW}📱 Installing React Router and other useful libraries...${NC}"
npm install react-router-dom @types/react-router-dom
npm install zustand # For state management
npm install axios # For API calls
npm install @tanstack/react-query # For data fetching
npm install clsx tailwind-merge class-variance-authority # For utility classes
npm install lucide-react # For icons

echo -e "${YELLOW}📝 Configuring Tailwind...${NC}"
# Update tailwind.config.js
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
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
}
EOF

echo -e "${YELLOW}📝 Creating global CSS file...${NC}"
# Create src/index.css
cat > src/index.css << 'EOF'
@tailwind base;
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
}
EOF

echo -e "${YELLOW}📝 Setting up Vitest configuration...${NC}"
# Create vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'
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
})
EOF

# Create test setup file
mkdir -p src/test
cat > src/test/setup.ts << 'EOF'
import '@testing-library/jest-dom'
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
}))
EOF

echo -e "${YELLOW}📝 Setting up ESLint configuration...${NC}"
# Create .eslintrc.js
cat > .eslintrc.js << 'EOF'
module.exports = {
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
}
EOF

echo -e "${YELLOW}📝 Setting up Prettier configuration...${NC}"
# Create .prettierrc
cat > .prettierrc << 'EOF'
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
EOF

echo -e "${YELLOW}📝 Setting up Playwright configuration...${NC}"
# Create playwright.config.ts
cat > playwright.config.ts << 'EOF'
import { defineConfig, devices } from '@playwright/test'

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

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    // },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
})
EOF

echo -e "${YELLOW}📝 Creating sample test files...${NC}"
# Create sample component test
mkdir -p src/components/__tests__
cat > src/components/__tests__/Button.test.tsx << 'EOF'
import { render, screen } from '@testing-library/react'
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
})
EOF

# Create sample e2e test
mkdir -p e2e
cat > e2e/example.spec.ts << 'EOF'
import { test, expect } from '@playwright/test'

test('homepage has correct title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/Vite \+ React/)
})

test('counter works correctly', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('button')).toHaveText('count is 0')
  await page.locator('button').click()
  await expect(page.locator('button')).toHaveText('count is 1')
})
EOF

echo -e "${YELLOW}📝 Updating package.json scripts...${NC}"
# Update package.json with additional scripts
npm pkg set scripts.test="vitest"
npm pkg set scripts.test:ui="vitest --ui"
npm pkg set scripts.test:run="vitest run"
npm pkg set scripts.e2e="playwright test"
npm pkg set scripts.e2e:ui="playwright test --ui"
npm pkg set scripts.e2e:install="playwright install"
npm pkg set scripts.lint="eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
npm pkg set scripts.format="prettier --write ."
npm pkg set scripts.format:check="prettier --check ."

echo -e "${YELLOW}📝 Creating .gitignore...${NC}"
# Update .gitignore
cat > .gitignore << 'EOF'
# Logs
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
.env.production.local
EOF

echo -e "${YELLOW}📝 Creating utility functions...${NC}"
# Create utils
mkdir -p src/lib
cat > src/lib/utils.ts << 'EOF'
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

echo -e "${YELLOW}📝 Creating sample Button component...${NC}"
# Create sample Button component
cat > src/components/Button.tsx << 'EOF'
import * as React from "react"
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

export { Button, buttonVariants }
EOF

echo -e "${YELLOW}📝 Setting up husky hooks...${NC}"
# Configure husky (skip npx due to compatibility issues)
mkdir -p .husky
echo 'npx lint-staged' > .husky/pre-commit
chmod +x .husky/pre-commit
npm pkg set lint-staged '{"*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"], "*.{json,md,yml,yaml}": ["prettier --write"]}'

echo -e "${GREEN}✅ Project initialization complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo -e "${YELLOW}1. cd $PROJECT_NAME${NC}"
echo -e "${YELLOW}2. npx playwright install${NC}"
echo -e "${YELLOW}3. npm run dev${NC}"
echo ""
echo -e "${BLUE}🚀 Available commands:${NC}"
echo -e "${YELLOW}• npm run dev          - Start development server${NC}"
echo -e "${YELLOW}• npm run build        - Build for production${NC}"
echo -e "${YELLOW}• npm run test          - Run unit tests${NC}"
echo -e "${YELLOW}• npm run test:ui      - Run unit tests with UI${NC}"
echo -e "${YELLOW}• npm run e2e          - Run e2e tests${NC}"
echo -e "${YELLOW}• npm run e2e:ui       - Run e2e tests with UI${NC}"
echo -e "${YELLOW}• npm run lint          - Run ESLint${NC}"
echo -e "${YELLOW}• npm run format        - Format code with Prettier${NC}"
echo ""
echo -e "${GREEN}🎉 Happy coding!${NC}"