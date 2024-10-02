<script setup lang="ts">
const props = defineProps({
	title: {
		type: String,
		required: true,
	},
});
</script>

<template>
	<div class="block">
		<h1>{{ props.title }}</h1>
		<slot></slot>
	</div>
</template>

<style>
.block {
	display: flex;
	flex-direction: column;
	justify-content: start;

	font-size: 16px;
	line-height: 24px;
	font-weight: 400;
}

.block h1 {
	line-height: 40px;
	font-size: 32px;
	font-weight: 600;
	margin: 0;
}

.block p {
	margin: 16px 0;
}

.block a {
	color: var(--highlight-color-lighter);
	text-decoration: underline;
	text-underline-offset: 2px;
	transition: color 0.25s, opacity 0.25s;
}

.block a:hover {
	color: var(--highlight-color-lightest);
}

.block a:active {
	color: var(--highlight-color-lightest);
}
</style>
