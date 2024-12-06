<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import HeadBar from "@/components/HeadBar.vue";
import LoadingPage from "./pages/LoadingPage.vue";
import PageLink from "@/components/PageLink.vue";
import { Ref, ref, useTemplateRef } from "vue";
import { NavLink } from "@/types";

const nextLink: Ref<NavLink | undefined> = ref(undefined);
const prevLink: Ref<NavLink | undefined> = ref(undefined);

const onPageChanged = () => {
  const html = document.getElementsByTagName("html")[0];
  html.scrollTo(0, 0);
  if (sidebarVisible.value) {
    switchMenuVisibility();
  }
};

const backdropVisible = ref(false);
const backdropClicked = () => {
  switchMenuVisibility();
};

const sidebar = useTemplateRef("sidebar");
const sidebarVisible = ref(false);
const switchMenuVisibility = () => {
  if (sidebar.value === null) {
    return;
  }
  backdropVisible.value = !backdropVisible.value;
  sidebarVisible.value = !sidebarVisible.value;

  const html = document.getElementsByTagName("html")[0];
  if (!sidebarVisible.value) {
    sidebar.value.$el.classList.remove("expand");
    html.classList.remove("disable-scroll");
  } else {
    sidebar.value.$el.classList.add("expand");
    html.classList.add("disable-scroll");
  }
};
</script>

<template>
  <div class="layout">
    <HeadBar @menu-click="switchMenuVisibility" class="headbar"></HeadBar>
    <div @click="backdropClicked" v-if="backdropVisible" class="backdrop"></div>
    <Sidebar
      @change="onPageChanged"
      class="sidebar"
      ref="sidebar"
      v-model:next-link="nextLink"
      v-model:prev-link="prevLink"
    ></Sidebar>
    <div class="content">
      <RouterView v-slot="{ Component }">
        <template v-if="Component">
          <Transition mode="out-in" name="fade">
            <Suspense timeout="0">
              <!-- main content -->
              <component class="page" :is="Component">
                <PageLink
                  @change="onPageChanged"
                  class="page-link"
                  :next-link="nextLink"
                  :prev-link="prevLink"
                ></PageLink>
              </component>

              <!-- loading state -->
              <template #fallback>
                <LoadingPage></LoadingPage>
              </template>
            </Suspense>
          </Transition>
        </template>
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

  .sidebar {
    left: 0;
    position: fixed;
    height: 100%;
    width: var(--sidebar-width);

    overflow-x: hidden;
    overflow-y: auto;
    z-index: var(--z-index-sidebar);

    transition:
      opacity 0.25s,
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

    .page {
      display: flex;
      flex-direction: column;
      flex-shrink: 0;

      max-width: 912px;
      margin: 0 auto;

      transition: opacity 0.5s;
    }
  }

  .backdrop {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;

    background-color: var(--backdrop-bg-color);
    z-index: var(--z-index-backdrop);
    transition: opacity 0.5s;
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
    .headbar {
      padding-left: 32px;
      padding-right: 32px;
    }
    .expand {
      opacity: 1;
      transform: translate(0);
    }
  }
}
</style>
