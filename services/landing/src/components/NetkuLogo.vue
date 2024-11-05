<script></script>

<template>
  <div class="logo">
    <a href="/">
      <img style="width: 25px" src="/img/netku.svg" />
      <span>Netku</span>
    </a>
  </div>
</template>

<style scoped>
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
}
.logo a {
  display: flex;
  gap: 10px;
}
.logo span {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-1);
}
</style>
