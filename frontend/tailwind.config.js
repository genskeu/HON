/** @type {import('tailwindcss').Config} */
// https://stackoverflow.com/questions/62688037/can-use-both-tailwind-css-and-bootstrap-4-at-the-same-time#:~:text=Yes%2C%20you%20can%20use%20Tailwind,make%20the%20important%20as%20true.
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  prefix: 'tw-',
  important: true,
  theme: {
    extend: {}
  },
  plugins: [],
  corePlugins: {
    preflight: false
  }
}
