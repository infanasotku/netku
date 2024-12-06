<script setup lang="ts">
import SelectMenu from "@/components/SelectMenu.vue";
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";

const { locale } = useI18n();
const props = defineProps({
  listOnly: {
    type: Boolean,
  },
});
const emits = defineEmits(["change"]);

const menuVisible = ref(props.listOnly);

const languageCode = {
  English: "en",
  Русский: "ru",
};

const menu = Object.keys(languageCode);
const current = computed({
  get: () => {
    const index = Object.values(languageCode).indexOf(locale.value);

    return index !== -1 ? index : 0;
  },
  set: (index) => {
    const newLang = Object.values(languageCode)[index];
    locale.value = newLang;
    localStorage.Lang = newLang;
    menuVisible.value = false;
    emits("change");
  },
});
</script>

<template>
  <div
    class="wrapper"
    @mouseenter="menuVisible = true"
    @mouseleave="menuVisible = false"
  >
    <button v-if="!props.listOnly" class="select">
      <span class="icon">
        <span class="language select-icon"></span>
        <span class="arrow select-icon"></span>
      </span>
    </button>
    <Transition name="menu">
      <div class="menu" v-if="menuVisible && !props.listOnly">
        <SelectMenu :list="menu" v-model:current="current"></SelectMenu>
      </div>
    </Transition>
    <SelectMenu
      v-if="props.listOnly"
      :list="menu"
      v-model:current="current"
    ></SelectMenu>
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  position: relative;
  display: flex;
  flex-direction: column;

  height: 100%;

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

    .icon {
      width: 34px;
      display: flex;
      align-items: center;
      gap: 4px;

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
    }
  }

  &:hover {
    .select {
      color: var(--text-color-2);
      transition: color 0.25s;
    }
  }

  .menu {
    @include popUp;

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
}
</style>
