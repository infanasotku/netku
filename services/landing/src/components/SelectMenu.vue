<script setup lang="ts"></script>

<template>
  <div class="wrapper">
    <ul class="menu">
      <li>English</li>
      <li>Русский</li>
    </ul>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  align-items: start;
  justify-content: center;

  padding: 12px;
  min-width: 128px;
  max-height: 200px;

  border: 1px solid var(--divider-color);
  border-radius: 12px;
  background-color: var(--menu-bg);
  box-shadow: var(--vp-shadow-3);
  transition: background-color 0.5s;
}
.menu {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;

  list-style: none;

  padding: 0;
  margin: 0;
}
.menu li {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color-1);

  padding: 0 24px 0 12px;
  line-height: 32px;
  white-space: nowrap;
}
.menu li:first-child {
  font-weight: 700;
}
</style>
