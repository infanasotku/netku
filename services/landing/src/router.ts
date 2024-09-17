import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		name: "about",
		path: "/",
		component: async () => await import("@/pages/AboutMePage.vue"),
	},
	{
		name: "not-found",
		path: "/:pathMatch(.*)*",
		component: async () => await import("@/pages/DefaultPage.vue"),
	},
];

const router = createRouter({
	routes: routes,
	history: createWebHistory(),
});

router.resolve({
	name: "not-found",
	params: { pathMatch: ["*"] },
});

export default router;
