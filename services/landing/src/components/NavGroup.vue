<script setup lang="ts">
const props = defineProps({
  header: {
    type: String,
    required: true,
  },
  list: {
    type: Array<{ active: boolean; content: string; href: string }>,
    required: true,
  },
});
</script>
<template>
  <ul class="group">
    <li class="group-header">{{ props.header }}</li>
    <li v-for="link in props.list">
      <a :class="{ highlighted: link.active }" :href="link.href">
        {{ link.content }}</a
      >
    </li>
  </ul>
</template>
<style scoped>
.group {
  list-style: none;
  padding-left: 0;
  padding-top: 12px;
  padding-bottom: 12px;
  margin: 0;
  width: 100%;

  display: flex;
  flex-direction: column;
}
.group-header {
  color: var(--text-color-1) !important;
  font-size: 14px;
  font-weight: 600;
}
.group li {
  padding-top: 5px;
  padding-bottom: 5px;
}
.group li a {
  color: var(--text-color-2);
  font-size: 14px;
  font-weight: 600;
  transition: 0.5s;
}
.group li:not(:first-child):hover a,
.group li:not(:first-child):hover {
  cursor: pointer;
  color: var(--highlight-color-1);
}
.highlighted {
  color: var(--highlight-color-1) !important;
}
</style>
