<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
	<main class="main">
		<ContentBlock class="block" :title="t('content.aboutme.header')">
			<i18n-t keypath="content.aboutme.description" tag="p">
				<template v-slot:email>
					<a target="_blank" href="https://t.me/infanasotku">{{
						t("content.aboutme.email")
					}}</a>
				</template>
			</i18n-t>
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
