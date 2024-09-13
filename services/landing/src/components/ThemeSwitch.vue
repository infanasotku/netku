<script setup lang="ts">
const onClick = () => {
  const layout = document.getElementsByClassName("layout")[0];

  if (layout.classList.contains("dark")) {
    layout.classList.remove("dark");
  } else {
    layout.classList.add("dark");
  }
};
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
  border-radius: 11px;
  position: relative;
  display: block;
  width: 40px;
  height: 22px;
  height: 22px;
  transition: 0.3s;

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
