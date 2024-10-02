<script setup lang="ts">
const props = defineProps({
	title: {
		type: String,
		required: true,
	},
});
</script>

<template>
	<div class="content-block">
		<h1>{{ props.title }}</h1>
		<slot></slot>
	</div>
</template>

<style>
.content-block {
	display: flex;
	flex-direction: column;
	justify-content: start;

	font-size: 16px;
	line-height: 24px;
	font-weight: 400;
	max-width: 80%;
}

.content-block h1 {
	line-height: 40px;
	font-size: 32px;
	font-weight: 600;
	margin: 0;
}

.content-block p {
	margin: 16px 0;
}

.content-block a {
	color: var(--highlight-color-lighter);
	text-decoration: underline;
	text-underline-offset: 2px;
	transition: color 0.25s, opacity 0.25s;
}

.content-block a:hover {
	color: var(--highlight-color-lightest);
}

.content-block a:active {
	color: var(--highlight-color-lightest);
}
</style>
