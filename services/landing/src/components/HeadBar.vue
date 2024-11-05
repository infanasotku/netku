<script setup lang="ts">
import ThemeSwitch from "@/components/ThemeSwitch.vue";
import LinkIcon from "@/components/LinkIcon.vue";
import LanguageSelect from "@/components/LanguageSelect.vue";
import NetkuLogo from "@/components/NetkuLogo.vue";
</script>

<template>
  <header class="headbar">
    <NetkuLogo class="logo"></NetkuLogo>
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

/*#region logo */
.logo {
  opacity: 0;
  height: 63px;
}

@include media-breakpoint-down(lg) {
  .logo {
    opacity: 1;
  }
}
/*#endregion */

/*#region tools */
.tools {
  display: flex;
  flex-direction: row;
  align-items: center;
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
</style>
