import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import router from "@/router";
import VueCookies from "vue-cookies";

import App from "@/App.vue";
import * as config from "@/config";
import en from "@/lang/en.json";
import ru from "@/lang/ru.json";
import "@/assets/scss/main.scss";

console.log(__BUILD_VERSION__);

const app = createApp(App);

const i18n = createI18n({
  locale: localStorage.Lang,
  fallbackLocale: "en",
  messages: { ru, en },
  legacy: false,
});

app
  .use(VueCookies, { expires: config.cookiesExpires })
  .use(i18n)
  .use(router)
  .mount("#app");
