<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  list: {
    type: Array<string>,
    required: true,
  },
});
const current = defineModel("current", {
  type: Number,
  required: true,
});
const list = computed(() => {
  return props.list
    .map((val, index) => ({ text: val, index: index }))
    .filter((el) => el.index !== current.value);
});
</script>

<template>
  <ul class="menu-list">
    <li class="current">{{ props.list[current] }}</li>
    <li v-for="record in list" @click="current = record.index">
      <span class="text">{{ record.text }}</span>
    </li>
  </ul>
</template>

<style scoped lang="scss">
.menu-list {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;

  list-style: none;

  padding: 0;
  margin: 0;

  li {
    font-size: 14px;
    color: var(--text-color-1);

    border-radius: 6px;
    padding: 0 24px 0 12px;
    line-height: 32px;
    white-space: nowrap;
    user-select: none;

    &:not(.current) {
      font-weight: 500;
      cursor: pointer;
      transition:
        background-color 0.25s,
        color 0.25s;

      &:hover {
        color: var(--highlight-color-lighter);
        background-color: var(--input-switch-bg-color);
        transition:
          background-color 0.25s,
          color 0.25s;

        .text::after {
          transition: transform 0.25s;
          transform: translateX(6px);
        }
      }

      .text::after {
        content: "";

        width: 16px;
        height: 16px;

        transition: transform 0.25s;
        color: var(--text-color-3);
        background-color: currentColor;
        mask: url("/img/arrow.svg") no-repeat;
      }
    }

    &.current {
      font-weight: 700;
    }

    .text {
      display: flex;
      align-items: center;

      gap: 6px;
    }
  }
}
</style>
