<script setup lang="ts">
import { NavLink } from "@/types";
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps({
  header: {
    type: String,
    required: true,
  },
  list: {
    type: Array<NavLink>,
    required: true,
  },
});
const emits = defineEmits(["change"]);
</script>

<template>
  <ul class="group">
    <li class="header">{{ props.header }}</li>
    <li v-for="link in props.list">
      <a
        :class="{ highlighted: link.active }"
        :href="link.href"
        @click.prevent="
          router.push(link.href);
          emits('change');
        "
      >
        <span>{{ link.content }}</span>
      </a>
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
.header {
  color: var(--text-color-1) !important;
  font-size: 14px;
  font-weight: 600;
  padding-top: 5px;
  padding-bottom: 5px;
}
.group a {
  display: flex;
  padding-top: 5px;
  padding-bottom: 5px;
}
.group a {
  color: var(--text-color-2);
  font-size: 14px;
  font-weight: 600;
  transition: color 0.25s;
}
.group a:hover {
  cursor: pointer;
  color: var(--highlight-color);
  transition: color 0.25s;
}
.highlighted {
  color: var(--highlight-color) !important;
}
</style>
