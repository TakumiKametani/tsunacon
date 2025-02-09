module.exports = {
  darkMode: 'class',
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: false,
    content: ['./templates/*.html', './templates/**/*.html'],
  },
  theme: {
    screens: {
      xs: '320px',
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    extend: {
      keyframes: {
        roll: {
          '0%': { transform: 'rotateX(45deg) rotateY(-45deg)'},
          '25%': { transform: 'rotateX(-45deg) rotateY(-45deg)'},
          '50%': { transform: 'rotateX(45deg) rotateY(45deg)'},
          '75%': { transform: 'rotateX(-45deg) rotateY(45deg)'},
          '100%': { transform: 'rotateX(45deg) rotateY(-45deg)'}
        }
      },
      animation: {
        roll: 'roll 5s infinite',
      }
    }
  },
  variants: {},
  plugins: [],
}