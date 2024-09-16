<script setup lang="ts">
const props = defineProps({
	list: {
		type: Array<string>,
		required: true,
	},
});
const current = defineModel("current", {
	type: Number,
	required: true,
});
</script>

<template>
	<div class="wrapper">
		<ul class="menu">
			<li
				:class="{ current: current === index }"
				v-for="(record, index) in props.list"
			>
				{{ record }}
			</li>
		</ul>
	</div>
</template>

<style scoped>
.wrapper {
	display: flex;
	align-items: start;
	justify-content: center;

	padding: 12px;
	min-width: 128px;
	max-height: 200px;

	border: 1px solid var(--divider-color);
	border-radius: 12px;
	background-color: var(--menu-bg);
	box-shadow: var(--vp-shadow-3);
	transition: background-color 0.5s;
}
.menu {
	display: flex;
	flex-direction: column;
	align-items: start;
	justify-content: start;

	list-style: none;

	padding: 0;
	margin: 0;
}
.menu li {
	font-size: 14px;
	color: var(--text-color-1);

	border-radius: 6px;
	padding: 0 24px 0 12px;
	line-height: 32px;
	white-space: nowrap;
}
.menu li:not(.current) {
	font-weight: 500;
	cursor: pointer;
	transition: background-color 0.25s, color 0.25s;
}
.menu li:not(.current):hover {
	color: var(--highlight-color-1);
	background-color: var(--input-switch-bg-color);
	transition: background-color 0.25s, color 0.25s;
}
.current {
	font-weight: 700;
}
</style>
