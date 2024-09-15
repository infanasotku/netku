<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import HeadBar from "@/components/HeadBar.vue";
</script>

<template>
  <div class="layout">
    <HeadBar class="headbar"></HeadBar>
    <Sidebar class="sidebar"></Sidebar>
    <router-view> </router-view>
  </div>
</template>

<style scoped>
.layout {
  background-color: var(--bg-block);
  width: 100%;
  height: 100%;
  display: flex;
}
.sidebar {
  left: 0;
  position: fixed;
  height: 100%;
  width: var(--sidebar-width);

  overflow-x: hidden;
  overflow-y: auto;
}
.headbar {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 64px;
  padding-left: var(--sidebar-width);
  padding-right: 30px;
}
</style>
