<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
</script>
<template>
  <div class="layout dark">
    <Sidebar class="app-sidebar"></Sidebar>
    <router-view> </router-view>
  </div>
</template>
<style scoped>
.layout {
  background-color: var(--bg-main);
  width: 100%;
  height: 100%;
  display: flex;
}
.app-sidebar {
  left: 0;
  position: fixed;
  height: 100%;
  width: 272px;
}
</style>
