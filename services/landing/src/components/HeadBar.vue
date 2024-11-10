<script setup lang="ts">
import { ref } from "vue";
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import LinkIcon from "@/components/LinkIcon.vue";
import LanguageSelect from "@/components/LanguageSelect.vue";
import NetkuLogo from "@/components/NetkuLogo.vue";

const emits = defineEmits(["menu-click"]);

const popUpTools = ref(false);
</script>

<template>
  <header class="headbar">
    <div class="menu">
      <span @click.prevent="emits('menu-click')" class="menu-icon"></span>
      <NetkuLogo :withLabel="false" class="logo"></NetkuLogo>
    </div>
    <div class="tool-switch">
      <span class="icon"></span>
    </div>
    <div class="tools">
      <div class="divider"></div>
      <LanguageSelect></LanguageSelect>
      <div class="divider"></div>
      <ThemeSwitch class="switch"></ThemeSwitch>
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
    </div>
    <Transition name="tools">
      <div v-if="popUpTools" class="pop-up-tools pop-up"></div>
    </Transition>
  </header>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

.headbar {
  background-color: var(--bg-block);

  height: 65px;

  display: flex;
  flex-grow: 1;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;

  border-bottom: 1px solid var(--divider-color);

  .menu {
    display: flex;
    flex-direction: row;
    align-items: center;

    gap: 10px;
    opacity: 0;

    .menu-icon {
      background-color: currentColor;
      color: inherit;
      width: 20px;
      height: 20px;
      fill: currentColor;
      mask: url("/img/menu.svg") no-repeat;

      color: var(--text-color-2);
      transition: color 0.25s;

      &:hover {
        color: var(--text-color-1);
        cursor: pointer;
      }
    }

    .logo {
      height: 63px;
    }
  }

  .tool-switch {
    align-items: center;
    position: relative;
    padding: 0 12px;
    margin-right: -12px;
    height: 100%;

    &:hover {
      cursor: pointer;
    }

    .icon {
      color: var(--text-color-1);
      background-color: currentColor;
      mask: url("/img/ellipsis.svg") no-repeat;

      height: 20px;
      width: 20px;
    }

    display: none;
  }

  .tools {
    display: flex;
    flex-direction: row;
    align-items: center;

    height: 100%;

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
  }

  .tools-enter-active,
  .tools-leave-active {
    transition: opacity 0.25s ease;
  }

  .tools-enter-from,
  .tools-leave-to {
    opacity: 0;
  }

  @include media-breakpoint-down(lg) {
    .menu {
      opacity: 1;
    }
    .tool-switch {
      display: flex;
    }
    .tools {
      display: none;
    }
  }
  @include media-breakpoint-up(lg) {
    .pop-up-tools {
      display: none;
    }
  }
}

.dark .headbar {
  border-bottom: 1px solid #000000;
}
</style>
