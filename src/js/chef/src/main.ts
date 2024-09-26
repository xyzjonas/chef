// import "./assets/fontawesome/css/all.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { Quasar, Notify } from "quasar";

import 'virtual:uno.css'

// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";

// Import Quasar css
import "quasar/src/css/index.sass";

import "@/assets/css/styles.css"
import "@/assets/css/editor.css"

import App from "./App.vue";
import router from "./router";

const pinia = createPinia();
const app = createApp(App);

Notify.setDefaults({
  position: 'top',
})

app.use(router);
app.use(pinia);
app.use(Quasar, {
  plugins: {
    Notify
  }, // import Quasar plugins and add here
});

app.mount("#app");
