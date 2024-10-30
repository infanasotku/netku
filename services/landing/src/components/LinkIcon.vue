<script setup lang="ts">
const props = defineProps({
  imgSource: {
    type: String,
    required: true,
  },
  link: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <a target="_blank" class="link" :href="props.link">
    <span
      class="icon"
      :style="{ mask: `url(${props.imgSource}) no-repeat` }"
    ></span>
  </a>
</template>

<style scoped>
.link {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 36px;
  height: 36px;

  cursor: pointer;
  color: var(--text-color-2);
  transition: color 0.5s;
}
.link:hover {
  color: var(--text-color-1);
  transition: color 0.25s;
}
.icon {
  background-color: currentColor;
  color: inherit;
  width: 20px;
  height: 20px;
  fill: currentColor;
}
</style>
