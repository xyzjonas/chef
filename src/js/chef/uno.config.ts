// uno.config.ts
import { defineConfig, presetUno, presetIcons } from "unocss";
import presetWebFonts from '@unocss/preset-web-fonts'
import { createLocalFontProcessor } from "@unocss/preset-web-fonts/local";

export default defineConfig({
  rules: [],
  shortcuts: {
    "title": "uppercase m-0 font-bold text-[3rem] md:text-[4rem] line-height-[2.5rem] md:line-height-[3.5rem] mb-1",
    "title-sm": "uppercase m-0 font-500 text-4xl mb-1",
  },
  presets: [
    // https://icones.js.org/collection/hugeicons
    presetIcons({
      extraProperties: {
        "vertical-align": "middle",
      },
    }),
    presetUno({
      // Align tailwind darkmode to Quasar's classes,
      // so that darkmode selectors (e.g. 'dark:color-red') can be used as well.
      dark: {
        light: '.body--light',
        dark: '.body--dark'
      }
    }),
    presetWebFonts({
      provider: "bunny",
      fonts: {
        sans: "Poppins:200,300,400,500,600",
        // title: 'Bungee Inline',
        title: "Monoton",
      },
      // processors: createLocalFontProcessor({
      //   // Directory to cache the fonts
      //   cacheDir: "node_modules/.cache/unocss/fonts",

      //   // Directory to save the fonts assets
      //   fontAssetsDir: "public/assets/fonts",

      //   // Base URL to serve the fonts from the client
      //   fontServeBaseUrl: "/assets/fonts",
      // }),
    }),
  ],
  theme: {
    colors: {
      primary: '#d35459',
      secondary: '#343a40',
      accent: '#FE7C3F'
    }
  }
});
