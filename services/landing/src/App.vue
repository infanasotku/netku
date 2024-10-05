<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import HeadBar from "@/components/HeadBar.vue";
import LoadingPage from "./pages/LoadingPage.vue";
</script>

<template>
	<div class="layout">
		<HeadBar class="headbar"></HeadBar>
		<Sidebar class="sidebar"></Sidebar>
		<div class="content">
			<RouterView v-slot="{ Component }">
				<Suspense timeout="0">
					<template #default>
						<component :is="Component" v-if="Component" />
					</template>
					<template #fallback>
						<LoadingPage></LoadingPage>
					</template>
				</Suspense>
			</RouterView>
		</div>
	</div>
</template>

<style scoped>
.layout {
	background-color: var(--bg-block);
	width: 100%;
	height: 100%;
	display: flex;

	overflow-y: auto;
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
	flex-grow: 0;
	flex-shrink: 0;

	height: fit-content;
	width: 100%;

	padding: calc(48px + var(--headbar-height)) 64px 128px
		calc(64px + var(--sidebar-width));
	color: var(--text-color-1);
}
main {
	display: flex;
	align-items: center;
	flex-direction: column;
	flex-shrink: 0;

	height: fit-content;
	width: 100%;
}
</style>
