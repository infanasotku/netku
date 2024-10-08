<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import HeadBar from "@/components/HeadBar.vue";
import LoadingPage from "./pages/LoadingPage.vue";
import PageLink from "@/components/PageLink.vue";
</script>

<template>
	<div class="layout">
		<HeadBar class="headbar"></HeadBar>
		<Sidebar class="sidebar"></Sidebar>
		<div class="content">
			<RouterView v-slot="{ Component }">
				<Transition name="fade">
					<Suspense timeout="0">
						<template #default>
							<component class="page" :is="Component" v-if="Component">
								<PageLink
									class="page-link"
									:next-link="{
										href: '/skills',
										content: 'Skills',
										active: true,
									}"
								></PageLink>
							</component>
						</template>
						<template #fallback>
							<LoadingPage></LoadingPage>
						</template>
					</Suspense>
				</Transition>
			</RouterView>
		</div>
	</div>
</template>

<style scoped>
.layout {
	background-color: var(--bg-block);
	width: 100%;
	min-height: 100vh;
	display: flex;
}
.sidebar {
	left: 0;
	position: fixed;
	height: 100%;
	width: var(--sidebar-width);

	overflow-x: hidden;
	overflow-y: auto;
	z-index: 2;
}
.headbar {
	position: fixed;
	right: 0;
	top: 0;
	width: 100%;
	height: var(--headbar-height);
	padding-left: var(--sidebar-width);
	padding-right: 30px;
	z-index: 1;
}
.content {
	display: flex;

	width: 100%;

	padding: calc(48px + var(--headbar-height)) 64px 128px
		calc(64px + var(--sidebar-width));
	color: var(--text-color-1);
}
.page-link {
	width: 80%;
}
</style>
