<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
	<main class="main">
		<ContentBlock :title="t('content.default.header')">
			<p>
				{{ t("content.default.description") }}
			</p>
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
</style>
