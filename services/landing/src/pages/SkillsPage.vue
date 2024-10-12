<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t, tm } = useI18n();
const localt = (key: string) => t("content.skills." + key);
</script>

<template>
	<main>
		<ContentBlock :title="localt('python.title')">
			<i18n-t
				scope="global"
				keypath="content.skills.python.description"
				tag="p"
			>
				<a href="https://www.python.org/" target="_blank">{{
					localt("python.python")
				}}</a>
				<code>{{ localt("python.backend") }}</code>
			</i18n-t>
			<ul>
				<li
					v-for="skill in (tm('content.skills.python.skills') as Array<{name: string}>)"
				>
					<p>{{ skill.name }}</p>
				</li>
			</ul>
		</ContentBlock>
		<slot></slot>
	</main>
</template>

<style scoped></style>
