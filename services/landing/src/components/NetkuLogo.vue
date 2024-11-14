<script setup lang="ts">
const props = defineProps({
  withLabel: {
    type: Boolean,
    default: true,
  },
});
</script>

<template>
  <div class="logo">
    <a href="/">
      <span class="icon"></span>
      <span class="title" v-if="props.withLabel">Netku</span>
    </a>
  </div>
</template>

<style scoped lang="scss">
.logo {
  width: fit-content;
  height: 64px;
  position: sticky;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: start;
  flex-grow: 0;
  flex-shrink: 0;

  z-index: 1;
  background-color: inherit;

  a {
    display: flex;
    gap: 10px;

    .title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-color-1);
    }

    .icon {
      display: flex;

      background-color: currentColor;
      width: 25px;
      height: 25px;
      fill: currentColor;
      mask: url("/img/netku.svg") no-repeat;

      color: var(--text-color-1);
      transition: color 0.25s;
    }
  }
}
</style>
