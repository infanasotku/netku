<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const localt = (key: string) => t("content.skills." + key);
</script>

<template>
	<main>
		<ContentBlock :title="localt('title')">
			<i18n-t scope="global" keypath="content.skills.description" tag="p">
			</i18n-t scope="global">
		</ContentBlock>
		<slot></slot>
	</main>
</template>

<style scoped></style>
