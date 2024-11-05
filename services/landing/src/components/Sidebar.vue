<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import NetkuLogo from "@/components/NetkuLogo.vue";
import { Navigation } from "@/lang/type";
import { computed, PropType, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import { NavData, NavLink } from "@/types";

const emits = defineEmits(["change"]);

const { tm, locale } = useI18n();
const route = useRoute();

const nav = computed(() => {
  locale;
  return tm("nav") as Array<Navigation>;
});

const currentHref = ref("");

const groups = computed((): Array<NavData> => {
  const result = nav.value.map((val) => ({
    header: val.header,
    list: val.list.map((listVal) => ({
      content: listVal.content,
      href: listVal.href,
      active: listVal.href === currentHref.value,
    })),
  }));

  const links: Array<NavLink> = [];
  result.forEach((val) => {
    links.push(...val.list);
  });
  const currentIndex = links.findIndex((val) => val.active);

  prevLink.value = currentIndex - 1 >= 0 ? links[currentIndex - 1] : undefined;
  nextLink.value =
    currentIndex + 1 < links.length ? links[currentIndex + 1] : undefined;

  emits("change");

  return result;
});

const nextLink = defineModel("nextLink", {
  type: Object as PropType<NavLink>,
});
const prevLink = defineModel("prevLink", {
  type: Object as PropType<NavLink>,
});

watch(route, () => {
  currentHref.value = route.path;
});
</script>

<template>
  <aside class="sidebar">
    <NetkuLogo class="logo"></NetkuLogo>
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

.logo {
  border-bottom: 1px solid var(--divider-color);
  width: 100%;
}
</style>
