/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f7f6fd',
          100: '#efeefb',
          200: '#dfddf7',
          300: '#cfccf4',
          400: '#c0bbf0',
          500: '#6257db',
          600: '#584ec5',
          700: '#4e45af',
          800: '#443c99',
          900: '#3a3483',
          950: '#312b6d'
        },
        success: {
          50: '#f4fbf5',
          100: '#e9f7ec',
          200: '#d4f0da',
          300: '#bee8c7',
          400: '#a9e1b5',
          500: '#28b446',
          600: '#24a23f',
          700: '#209038',
          800: '#1c7d31',
          900: '#186c2a',
          950: '#145a23'
        },
        warning: {
          50: '#fefbf2',
          100: '#fef8e5',
          200: '#fef1cc',
          300: '#fdeab2',
          400: '#fde399',
          500: '#fbbb00',
          600: '#e1a800',
          700: '#c89500',
          800: '#af8200',
          900: '#967000',
          950: '#7d5d00'
        },
        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
          950: '#450a0a'
        }
      }
    },
  },
  plugins: [],
}