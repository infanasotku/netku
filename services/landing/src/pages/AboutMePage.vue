<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
	<main>
		<ContentBlock :title="t('content.aboutme.header')">
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

<style scoped></style>
