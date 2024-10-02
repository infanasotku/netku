<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
</script>

<template>
	<main class="main">
		<ContentBlock class="block" title="Loading">
			<p>Loading...</p>
		</ContentBlock>
	</main>
</template>

<style scoped>
.main {
	display: flex;
	align-items: center;
	flex-direction: column;
	flex-shrink: 0;
}
.block {
	max-width: 80%;
}
</style>
