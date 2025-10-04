/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        success: '{color}',
        color-2: '{color}',
        facebook: '{color}',
        primary: '{color}',
        color-5: '{color}',
        gray-100: '{color}',
        color-7: '{color}',
        danger: '{color}',
        gray-50: '{color}',
        warning: '{color}',
      },
      fontFamily: {
        'poppins': ['Poppins'],
      },
      fontSize: {
        'heading': ['36.0px'],
        'body': ['16.0px'],
        'caption': ['12.0px'],
        'body': ['16.0px'],
        'body': ['16.0px'],
        'heading': ['40.0px'],
        'heading': ['36.0px'],
      }
    }
  },
  plugins: [],
}