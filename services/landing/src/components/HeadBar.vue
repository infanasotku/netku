<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import LinkIcon from "@/components/LinkIcon.vue";
import LanguageSelect from "@/components/LanguageSelect.vue";
import NetkuLogo from "@/components/NetkuLogo.vue";

const { t } = useI18n();

const emits = defineEmits(["menu-click"]);

const popUpVisible = ref(false);
</script>

<template>
  <header class="headbar">
    <div class="menu">
      <span @click.prevent="emits('menu-click')" class="menu-icon"></span>
      <NetkuLogo :withLabel="false" class="logo"></NetkuLogo>
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
    <div
      class="pop-up-wrapper"
      @mouseenter="popUpVisible = true"
      @mouseleave="popUpVisible = false"
    >
      <div class="tool-switch">
        <span class="icon"></span>
      </div>
      <Transition name="tools">
        <div v-if="popUpVisible" class="pop-up-tools">
          <div class="group">
            <LanguageSelect
              @change="popUpVisible = false"
              :list-only="true"
            ></LanguageSelect>
          </div>
          <div class="group">
            <div class="appearance">
              <span>{{ t("common.appearance") }}</span>
              <ThemeSwitch></ThemeSwitch>
            </div>
          </div>
          <div class="group">
            <div class="social-wrapper">
              <div class="social-icons">
                <LinkIcon
                  class="link"
                  imgSource="/img/github.svg"
                  link="https://github.com/infanasotku"
                ></LinkIcon>
                <LinkIcon
                  class="link"
                  imgSource="/img/telegram.svg"
                  link="https://t.me/infanasotku"
                ></LinkIcon>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </header>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

.headbar {
  background-color: var(--bg-block);

  height: 64px;

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

  .pop-up-wrapper {
    display: flex;
    position: relative;
    height: 100%;

    .tool-switch {
      align-items: center;
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
    .pop-up-tools {
      @include popUp;

      flex-direction: column;

      position: absolute;
      right: -12px;
      top: calc(100% / 2 + 20px);

      min-width: 200px;
      max-height: calc(100vh - var(--headbar-height));
      padding: 0px;

      overflow-y: auto;

      .group:not(:first-child) {
        border-top: 1px solid var(--divider-color);
      }

      .group {
        width: 100%;
        padding: 12px;
      }

      .appearance {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        padding: 0 12px;

        span {
          color: var(--text-color-2);
          line-height: 28px;
          font-size: 12px;
          font-weight: 500;
        }
      }

      .social-wrapper {
        padding: 0 12px;
        .social-icons {
          display: flex;
          flex-direction: row;

          margin: -4px -8px;
        }
      }
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
    .tools {
      display: none;
    }
    .pop-up-wrapper {
      .tool-switch {
        display: flex;
      }
    }
  }
  @include media-breakpoint-up(lg) {
    .pop-up-wrapper {
      display: none;
    }
  }
}

.dark .headbar {
  border-bottom: 1px solid #000000;
}
</style>
