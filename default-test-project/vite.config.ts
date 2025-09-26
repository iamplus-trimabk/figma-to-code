import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/shadcn': path.resolve(__dirname, './src/shadcn'),
      '@/shadcn/components': path.resolve(__dirname, './src/shadcn/components'),
      '@/shadcn/blocks': path.resolve(__dirname, './src/shadcn/blocks'),
      '@/shadcn/hooks': path.resolve(__dirname, './src/shadcn/hooks'),
      '@/custom': path.resolve(__dirname, './src/custom'),
      '@/custom/blocks': path.resolve(__dirname, './src/custom/blocks'),
      '@/custom/hooks': path.resolve(__dirname, './src/custom/hooks'),
      '@/custom/components': path.resolve(__dirname, './src/custom/components'),
    },
  },
})
