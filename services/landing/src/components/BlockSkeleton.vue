<script setup lang="ts"></script>

<template>
	<div class="wrapper">
		<div class="block" v-for="_ in 5">
			<div class="title skeleton"></div>
			<div class="lines">
				<div class="line skeleton" v-for="_ in 4"></div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.wrapper {
	display: flex;
	flex-direction: column;
	justify-content: start;

	width: 400px;
}
.block {
	display: flex;
	flex-direction: column;
	justify-content: start;

	gap: 16px;
	padding-bottom: 48px;
	border-bottom: 1px solid var(--divider-color);
}
.block:not(:first-child) {
	margin-top: 24px;
}
.title {
	height: 32px;
	width: 100%;
	margin: 4px 0;
}
.lines {
	display: flex;
	flex-direction: column;
	justify-content: start;
}
.line {
	height: 16px;
	width: 100%;
	margin: 4px 0;
}

.skeleton {
	animation: skeleton-loading 1s linear infinite alternate;
}

@keyframes skeleton-loading {
	0% {
		background-color: var(--skeleton-color-1);
	}
	100% {
		background-color: var(--skeleton-color-2);
	}
}
</style>
