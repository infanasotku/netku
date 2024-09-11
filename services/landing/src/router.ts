import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    name: "aboutme",
    path: "/aboutme",
    component: async () => await import("@/pages/AboutMe.vue"),
  },
];

const router = createRouter({
  routes: routes,
  history: createWebHistory(),
});

export default router;
