<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
</script>

<template>
  <aside class="sidebar">
    <div class="sb-header">
      <a href="/">
        <img style="width: 25px" src="/img/netku.svg" />
        <span>Netku</span>
      </a>
    </div>
    <NavBar class="sb-navbar"></NavBar>
  </aside>
</template>

<style scoped>
.sidebar {
  background-color: var(--bg-alt);
  opacity: 1;

  padding-left: 32px;
  padding-right: 32px;
}

.sb-navbar {
  border-top: 1px solid var(--divider-color);
  height: 100%;
}

/*#region Header */
.sb-header {
  width: 100%;
  height: 64px;

  display: flex;
  align-items: center;
  justify-content: start;
}
.sb-header a {
  display: flex;
  gap: 10px;
}
.sb-header span {
  font-size: 16px;
  font-weight: 600;
}
/*#endregion */
</style>
