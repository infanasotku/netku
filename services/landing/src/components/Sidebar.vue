<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { ref } from "vue";

const groups = ref([
  {
    header: "Author",
    list: [
      {
        content: "Briefly about me",
        href: "/about",
        active: true,
      },
      {
        content: "Skills | Technologies",
        href: "/skills",
        active: false,
      },
      {
        content: "Work experience",
        href: "/experience",
        active: false,
      },
    ],
  },
  {
    header: "Second",
    list: [
      {
        content: "First",
        href: "/First",
        active: false,
      },
      {
        content: "Second",
        href: "/Second",
        active: false,
      },
      {
        content: "Third",
        href: "/Third",
        active: false,
      },
    ],
  },
]);
</script>

<template>
  <aside class="sidebar">
    <div class="sb-header">
      <a href="/">
        <img style="width: 25px" src="/img/netku.svg" />
        <span>Netku</span>
      </a>
    </div>
    <NavBar class="sb-navbar" :nav-groups="groups"></NavBar>
  </aside>
</template>

<style scoped>
.sidebar {
  background-color: var(--bg-alt);
  transition: 0.5s;

  padding-left: 32px;
  padding-right: 32px;

  display: flex;
  flex-direction: column;
}

.sb-navbar {
  padding: 0;
}

/*#region Header */
.sb-header {
  width: 100%;
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
  border-bottom: 1px solid var(--divider-color);
}
.sb-header a {
  display: flex;
  gap: 10px;
}
.sb-header span {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-1);
}
/*#endregion */
</style>
