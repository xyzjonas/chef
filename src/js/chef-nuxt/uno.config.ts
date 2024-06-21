// uno.config.ts
import { defineConfig, presetUno, presetIcons, presetWebFonts } from 'unocss'


export default defineConfig({
  rules: [],
  presets: [
    // https://icones.js.org/collection/hugeicons
    presetIcons({
      extraProperties: {
        'vertical-align': 'middle',
      }
    }),
    presetUno(),
    presetWebFonts({
      provider: 'bunny',
      fonts: {
        sans: 'Poppins:200,300,400,500,600'
      }
    }),
  ]
})