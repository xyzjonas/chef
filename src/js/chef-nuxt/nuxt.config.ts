// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    pageTransition: { name: "page", mode: "out-in" },
  },
  devtools: { enabled: false },
  modules: [
    "@unocss/nuxt",
    "nuxt-api-party",
  ],
  apiParty: {
    endpoints: {
      api: {
        url: process.env.API_URL!,
      },
      images: {
        url: process.env.IMAGES_URL!,
      }
    }
  },
  devServer: {
    port: 3001,
  },
});