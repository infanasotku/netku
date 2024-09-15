import { createApp } from "vue";
import router from "@/router";
import VueCookies from "vue-cookies";

import App from "@/App.vue";
import * as config from "@/config";

const app = createApp(App);

app
  .use(VueCookies, { expires: config.cookiesExpires })
  .use(router)
  .mount("#app");
