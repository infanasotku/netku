<script setup lang="ts">
import SelectMenu from "@/components/SelectMenu.vue";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

const { locale } = useI18n();

const menuVisible = ref(false);

const languageCode: any = {
	English: "en",
	Русский: "ru",
};
const menu = ref(["English", "Русский"]);
const current = ref(0);

watch(current, () => {
	menuVisible.value = false;
	locale.value = languageCode[menu.value[current.value]];
});
</script>

<template>
	<div
		class="wrapper"
		@mouseenter="menuVisible = true"
		@mouseleave="menuVisible = false"
	>
		<button class="select">
			<span class="icon">
				<span class="language select-icon"></span>
				<span class="arrow select-icon"></span>
			</span>
		</button>
		<Transition name="menu">
			<div class="menu" v-if="menuVisible">
				<SelectMenu :list="menu" v-model:current="current"></SelectMenu>
			</div>
		</Transition>
	</div>
</template>

<style scoped>
.wrapper {
	position: relative;
	display: flex;
	flex-direction: column;

	height: 100%;
}
/*#region Button */
.select {
	display: flex;
	align-items: center;
	height: 100%;
	padding: 0 12px;

	color: var(--text-color-1);
	border: none;
	background-color: transparent;
	background-image: none;
	transition: color 0.5s;
}
.wrapper:hover > .select {
	color: var(--text-color-2);
	transition: color 0.25s;
}
.icon {
	width: 34px;
	display: flex;
	align-items: center;
	gap: 4px;
}
.select-icon {
	background-color: currentColor;
	color: inherit;
}
.language {
	mask: url("/img/language.svg") no-repeat;
	width: 16px;
	height: 16px;
}
.arrow {
	mask: url("/img/arrow.svg") no-repeat;
	width: 14px;
	height: 14px;
	transform: rotate(90deg);
}
/*#endregion */
/*#region Menu */
.menu {
	position: absolute;
	right: -12px;
	top: calc(100% / 2 + 20px);
}
.menu-enter-active,
.menu-leave-active {
	transition: opacity 0.25s ease;
}

.menu-enter-from,
.menu-leave-to {
	opacity: 0;
}
/*#endregion */
</style>
