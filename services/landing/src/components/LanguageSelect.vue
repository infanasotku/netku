<script setup lang="ts"></script>

<template>
  <button class="select">
    <span class="icon">
      <span class="language select-icon"></span>
      <span class="arrow select-icon"></span>
    </span>
  </button>
</template>

<style scoped>
.select {
  display: flex;
  align-items: center;
  height: 100%;

  color: var(--text-color-1);
  border: none;
  background-color: transparent;
  background-image: none;
  transition: color 0.5s;
}
.select:hover {
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
</style>
