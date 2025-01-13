<script setup lang="ts">
import LoadingLogo from "@/components/LoadingLogo.vue";
</script>

<template>
  <main>
    <LoadingLogo class="logo"></LoadingLogo>
  </main>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

main {
  justify-content: center;
  display: flex;

  height: fit-content;

  .logo {
    width: 100px;
    height: 100px;
  }
}

@include media-breakpoint-down(sm) {
  main {
    .logo {
      width: 60px;
      height: 60px;
    }
  }
}
</style>
