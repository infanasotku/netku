<script setup lang="ts">
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import LinkIcon from "@/components/LinkIcon.vue";
import LanguageSelect from "@/components/LanguageSelect.vue";
</script>

<template>
	<header class="headbar">
		<div class="divider"></div>
		<LanguageSelect></LanguageSelect>
		<div class="divider"></div>
		<ThemeSwitch class="swicth"></ThemeSwitch>
		<div class="divider"></div>
		<div class="social-icons">
			<LinkIcon
				imgSource="/img/github.svg"
				link="https://github.com/infanasotku"
			></LinkIcon>
			<LinkIcon
				imgSource="/img/telegram.svg"
				link="https://t.me/infanasotku"
			></LinkIcon>
		</div>
	</header>
</template>

<style scoped>
.headbar {
	background-color: var(--bg-block);

	height: 64px;
	width: 100%;

	display: flex;
	flex-direction: row;
	justify-content: end;
	align-items: center;

	border-bottom: 1px solid var(--divider-color);
}

.dark .headbar {
	border-bottom: 1px solid #000000;
}

.social-icons {
	display: flex;
	flex-direction: row;
}

.divider {
	width: 1px;
	height: 24px;
	background-color: var(--divider-color);
	margin: 0 8px;
}

.switch {
	margin-left: 8px;
	margin-right: 8px;
}
</style>
