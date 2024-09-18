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

<style scoped>
.block {
	display: flex;
	flex-direction: column;
	justify-content: start;

	font-size: 16px;
	line-height: 24px;
	font-weight: 400;
}

h1 {
	line-height: 40px;
	font-size: 32px;
	font-weight: 600;
	margin: 0;
}
</style>
