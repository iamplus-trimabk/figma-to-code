# test-shadcn-project

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

