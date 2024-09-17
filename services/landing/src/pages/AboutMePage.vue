<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
	<main class="main">
		<h1>{{ t("content.aboutme.header") }}</h1>
	</main>
</template>

<style scoped>
.main {
	display: flex;
	justify-content: center;
}
</style>
