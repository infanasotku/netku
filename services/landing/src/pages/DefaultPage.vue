<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
	<main class="main">
		<h1>{{ t("content.default.header") }}</h1>
		<p>{{ t("content.default.description") }}</p>
	</main>
</template>

<style scoped>
.main {
	display: flex;
	align-items: center;
	flex-direction: column;
}
</style>
