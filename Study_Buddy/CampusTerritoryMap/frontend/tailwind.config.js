/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'hex': "url('/src/assets/background.png')",
        'hex_svg': "url('/src/assets/background_2.svg')",
        'hex_test': "url('/src/assets/background_test.svg')",
      }
    },
  },
  plugins: [],
}

