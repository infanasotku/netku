<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const localt = (key: string) => t("content.aboutme." + key);
</script>

<template>
	<main>
		<ContentBlock :title="localt('title')">
			<i18n-t keypath="content.aboutme.description" tag="p">
				<code>{{ localt("fullstack") }}</code>
				<a href="https://fastapi.tiangolo.com/" target="_blank">{{
					localt("fastapi")
				}}</a>
				<a href="https://www.python.org/" target="_blank">{{
					localt("python")
				}}</a>
				<a href="https://go.dev/" target="_blank">{{ localt("go") }}</a>
				<a href="https://vuejs.org/" target="_blank">{{ localt("vue") }}</a>
				<code>{{ localt("spa") }}</code>
				<a href="https://docs.docker.com/compose/" target="_blank">{{
					localt("docker")
				}}</a>
				<a href="https://www.postgresql.org/" target="_blank">{{
					localt("postgres")
				}}</a>
				<code>{{ localt("tcp") }}</code>
				<a href="https://nginx.org/en/" target="_blank">{{
					localt("nginx")
				}}</a>
				<code>{{ localt("ci") }}</code>
				<code>{{ localt("code") }}</code>
			</i18n-t>
			<div class="custom note">
				<p class="title">
					<code>{{ localt("note.title") }}</code>
				</p>
				<i18n-t keypath="content.aboutme.note.body" tag="p">
					<code>{{ localt("note.observation") }}</code>
					<code>{{ localt("note.presentation") }}</code>
					<code>{{ localt("note.development") }}</code>
					<code>{{ localt("note.test") }}</code>
					<code>{{ localt("note.bug") }}</code>
					<a target="_blank" href="https://t.me/infanasotku">{{
						localt("note.email")
					}}</a>
				</i18n-t>
			</div>
		</ContentBlock>
	</main>
</template>

<style scoped></style>
