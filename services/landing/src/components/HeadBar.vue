<script setup lang="ts">
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import LinkIcon from "@/components/LinkIcon.vue";
import LanguageSelect from "@/components/LanguageSelect.vue";
import NetkuLogo from "@/components/NetkuLogo.vue";

const emits = defineEmits(["menu-click"]);
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
}

/*#region menu */
.menu {
  display: flex;
  flex-direction: row;
  align-items: center;

  gap: 10px;
  opacity: 0;
}

.menu-icon {
  background-color: currentColor;
  color: inherit;
  width: 20px;
  height: 20px;
  fill: currentColor;
  mask: url("/img/menu.svg") no-repeat;

  color: var(--text-color-2);
  transition: color 0.25s;
}

.menu-icon:hover {
  color: var(--text-color-1);
  cursor: pointer;
}

.logo {
  height: 63px;
}

/*#endregion */

/*#region tools */
.tools {
  display: flex;
  flex-direction: row;
  align-items: center;

  height: 100%;
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
/*#endregion */

@include media-breakpoint-down(lg) {
  .menu {
    opacity: 1;
  }
}
</style>
