/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0A0A0F',
        surface: '#12121A',
        panel: '#1A1A26',
        border: '#2A2A3E',
        accent: '#6C63FF',
        'accent-dim': '#4B44CC',
        'accent-glow': 'rgba(108,99,255,0.15)',
        muted: '#6B7280',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
      },
      fontFamily: {
        display: ['"DM Serif Display"', 'serif'],
        body: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease forwards',
        'slide-up': 'slideUp 0.4s ease forwards',
        'pulse-ring': 'pulseRing 2s ease infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: { from: { opacity: 0, transform: 'translateY(16px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        pulseRing: { '0%, 100%': { boxShadow: '0 0 0 0 rgba(108,99,255,0.4)' }, '50%': { boxShadow: '0 0 0 12px rgba(108,99,255,0)' } },
      }
    },
  },
  plugins: [],
}
