<script setup lang="ts"></script>

<template>
  <div class="logo">
    <span class="icon"></span>
  </div>
</template>

<style scoped>
.logo {
  display: flex;
  position: relative;
}

.icon {
  width: 100%;
  height: 100%;

  color: transparent;
  mask: url("/img/netku.svg") no-repeat;
}

.icon:before {
  content: "";

  animation-name: shine;
  animation-duration: 1s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in;

  background: var(--shine-gradient);

  width: 300%;
  height: 100%;
  position: absolute;
}

@keyframes shine {
  100% {
    transform: translateX(-66%);
  }
}
</style>
