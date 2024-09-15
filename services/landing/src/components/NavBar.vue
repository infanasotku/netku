<script setup lang="ts">
import NavGroup from "@/components/NavGroup.vue";

const props = defineProps({
  navGroups: {
    type: Array<{
      header: string;
      list: Array<{ active: boolean; content: string; href: string }>;
    }>,
    required: true,
  },
});
</script>

<template>
  <nav class="navbar">
    <NavGroup
      class="group"
      v-for="group in props.navGroups"
      :header="group.header"
      :list="group.list"
    ></NavGroup>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;
  gap: 15px;
}
.group:not(:first-child) {
  border-top: 1px solid var(--divider-color);
}
</style>
