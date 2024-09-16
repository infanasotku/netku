<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { Navigation } from "@/lang/type";
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

const { tm } = useI18n();

const nav = ref(tm("nav") as Array<Navigation>);

const currentHref = ref("");

const groups = computed(() => {
  return nav.value.map((val) => {
    return {
      header: val.header,
      list: val.list.map((listVal) => {
        return {
          content: listVal.content,
          href: listVal.href,
          active: listVal.href === currentHref.value,
        };
      }),
    };
  });
});

onMounted(() => {
  currentHref.value = groups.value[0].list[0].href;
});
</script>

<template>
  <aside class="sidebar">
    <div class="header">
      <a href="/">
        <img style="width: 25px" src="/img/netku.svg" />
        <span>Netku</span>
      </a>
    </div>
    <NavBar class="navbar" :nav-groups="groups"></NavBar>
  </aside>
</template>

<style scoped>
.sidebar {
  background-color: var(--bg-alt);

  padding-left: 32px;
  padding-right: 32px;

  display: flex;
  flex-direction: column;
}

.navbar {
  padding: 0;
}

/*#region Header */
.header {
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
.header a {
  display: flex;
  gap: 10px;
}
.header span {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color-1);
}
/*#endregion */
</style>
