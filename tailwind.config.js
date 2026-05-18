/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'brand-teal': 'oklch(59% 0.2 210)',
        'brand-orange': 'oklch(70% 0.2 40)',
        'brand-lime': 'oklch(75% 0.2 130)',
      }
    }
  }
}