<script setup lang="ts">
import ThemeSwitch from "@/components/ThemeSwitch.vue";
</script>

<template>
  <header class="headbar">
    <ThemeSwitch></ThemeSwitch>
  </header>
</template>

<style scoped>
.headbar {
  background-color: var(--bg-block);

  height: 64px;
  width: 100%;

  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;

  border-bottom: 1px solid var(--divider-color);
}
</style>
