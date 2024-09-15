<script setup lang="ts">
import { VueCookies } from "vue-cookies";
import { inject, onMounted } from "vue";

const $cookies = inject<VueCookies>("$cookies")!;

const setTheme = (dark: boolean) => {
  const layout = document.getElementsByClassName("layout")[0];

  if (dark) {
    layout.classList.add("dark");
  } else {
    layout.classList.remove("dark");
  }

  $cookies.set("theme", dark ? "dark" : "light");
};

const onClick = () => {
  const layout = document.getElementsByClassName("layout")[0];

  setTheme(!layout.classList.contains("dark"));
};

onMounted(() => {
  const theme = $cookies.get("theme");

  setTheme(theme && theme === "dark");
});
</script>

<template>
  <button class="switch" @click="onClick">
    <span class="check">
      <span class="icon">
        <span class="sun switch-icon"></span>
        <span class="moon switch-icon"></span>
      </span>
    </span>
  </button>
</template>

<style scoped>
.switch {
  position: relative;
  display: flex;
  flex-shrink: 0;
  width: 40px;
  height: 22px;
  height: 22px;

  transition: 0.3s;
  border-radius: 11px;
  border: 1px solid var(--input-border-color);
  background-color: var(--input-switch-bg-color);
}

.check {
  position: absolute;
  top: 1px;
  left: 1px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  transition: transform 0.25s !important;

  background-color: var(--neutral-inverse-color);
}

.dark .check {
  transform: translate(18px);
}

.icon {
  position: relative;
  display: block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  overflow: hidden;
}

.switch-icon {
  transition: opacity 0.25s !important;
  color: var(--text-color-1);
  mask-size: 100% 100%;
  background-color: currentColor;

  position: absolute;
  top: 3px;
  left: 3px;
  width: 12px;
  height: 12px;
}

.sun {
  mask: url("/img/sun.svg") no-repeat;
}

.moon {
  opacity: 0;
  mask: url("/img/moon.svg") no-repeat;
}

.dark .sun {
  opacity: 0;
}

.dark .moon {
  opacity: 1;
}
</style>
