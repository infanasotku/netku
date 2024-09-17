import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		name: "about",
		path: "/",
		component: async () => await import("@/pages/AboutMe.vue"),
	},
];

const router = createRouter({
	routes: routes,
	history: createWebHistory(),
});

export default router;
