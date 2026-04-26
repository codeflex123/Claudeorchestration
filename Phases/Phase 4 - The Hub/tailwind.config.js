/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Inter', 'serif'], // Fallback for Claude's serif look
      },
      colors: {
        accent: '#d97757',
        carbon: {
          900: '#0a0a0a',
          800: '#111111',
          700: '#1e1e1e',
        }
      }
    },
  },
  plugins: [],
}
