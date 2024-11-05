<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import HeadBar from "@/components/HeadBar.vue";
import LoadingPage from "./pages/LoadingPage.vue";
import PageLink from "@/components/PageLink.vue";
import { Ref, ref } from "vue";
import { NavLink } from "@/types";

const nextLink: Ref<NavLink | undefined> = ref(undefined);
const prevLink: Ref<NavLink | undefined> = ref(undefined);
</script>

<template>
  <div class="layout">
    <HeadBar class="headbar"></HeadBar>
    <Sidebar
      class="sidebar"
      v-model:next-link="nextLink"
      v-model:prev-link="prevLink"
    ></Sidebar>
    <div class="content">
      <RouterView v-slot="{ Component }">
        <Suspense timeout="0">
          <template #default>
            <component class="page" :is="Component" v-if="Component">
              <PageLink
                class="page-link"
                :next-link="nextLink"
                :prev-link="prevLink"
              ></PageLink>
            </component>
          </template>
          <template #fallback>
            <LoadingPage></LoadingPage>
          </template>
        </Suspense>
      </RouterView>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

.layout {
  background-color: var(--bg-block);
  width: 100%;
  min-height: 100vh;
  display: flex;
}
.sidebar {
  left: 0;
  position: fixed;
  height: 100%;
  width: var(--sidebar-width);

  overflow-x: hidden;
  overflow-y: auto;
  z-index: 2;

  transition:
    opacity 0.5s,
    transform 0.25s ease;
}
.headbar {
  position: fixed;
  right: 0;
  top: 0;
  width: 100%;
  height: var(--headbar-height);
  padding-left: var(--sidebar-width);
  padding-right: 30px;
  z-index: 1;
}
.content {
  width: 100%;
  height: fit-content;

  padding: calc(32px + var(--headbar-height)) 24px 96px;
  color: var(--text-color-1);
}

@include media-breakpoint-up(md) {
  .content {
    padding: calc(48px + var(--headbar-height)) 64px 128px 64px;
  }
}

@include media-breakpoint-up(lg) {
  .content {
    padding: calc(48px + var(--headbar-height)) 64px 128px
      calc(64px + var(--sidebar-width));
  }
}

@include media-breakpoint-down(lg) {
  .sidebar {
    opacity: 0;
    transform: translate(-100%);
  }
}
</style>
