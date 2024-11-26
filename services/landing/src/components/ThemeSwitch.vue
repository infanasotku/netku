<script setup lang="ts">
import { VueCookies } from "vue-cookies";
import { inject, onMounted, onUnmounted } from "vue";

const $cookies = inject<VueCookies>("$cookies")!;
let html: Element;
let darkColorScheme: MediaQueryList;

const setTheme = (dark: boolean) => {
  const notransition = document.createElement("style");
  notransition.appendChild(
    document.createTextNode(
      `* {
       -webkit-transition: none !important;
       -moz-transition: none !important;
       -o-transition: none !important;
       -ms-transition: none !important;
       transition: none !important;
    }`,
    ),
  );
  document.head.appendChild(notransition);

  if (dark) {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }
  window.window.getComputedStyle(notransition).opacity;
  document.head.removeChild(notransition);

  $cookies.set("theme", dark ? "dark" : "light");
};

const setPageIcon = (dark: boolean) => {
  const iconLink: HTMLLinkElement | null =
    document.querySelector("link[rel~='icon']");

  if (!iconLink) {
    return;
  }

  const iconId = dark ? "dark" : "light";
  iconLink.href = `/img/netku-${iconId}.svg`;
};

const onClick = () => {
  setTheme(!html.classList.contains("dark"));
};

const browserThemeChanged = () => {
  const isThemeDark = darkColorScheme.matches;
  setTheme(isThemeDark);
  setPageIcon(isThemeDark);
};

onMounted(() => {
  const savedTheme = $cookies.get("theme");
  html = document.documentElement;
  darkColorScheme = window.matchMedia("(prefers-color-scheme: dark)");

  browserThemeChanged();
  darkColorScheme.addEventListener("change", browserThemeChanged);

  if (savedTheme) {
    setTheme(savedTheme === "dark");
  }
});

onUnmounted(() => {
  darkColorScheme.removeEventListener("change", browserThemeChanged);
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
