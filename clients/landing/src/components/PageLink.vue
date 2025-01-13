<script setup lang="ts">
import { PropType } from "vue";
import { type NavLink } from "@/types";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const router = useRouter();

const { t } = useI18n();

const emits = defineEmits(["change"]);
const props = defineProps({
  nextLink: {
    type: Object as PropType<NavLink>,
  },
  prevLink: {
    type: Object as PropType<NavLink>,
  },
});
</script>

<template>
  <nav>
    <div class="wrapper">
      <a
        v-if="props.prevLink !== undefined"
        class="link prev"
        :href="props.prevLink.href"
        @click.prevent="
          router.push(props.prevLink.href);
          emits('change');
        "
      >
        <span class="desc">{{ t("common.desc.prev") }}</span>
        <span class="title">{{ props.prevLink.content }}</span>
      </a>
    </div>
    <div class="wrapper">
      <a
        v-if="props.nextLink !== undefined"
        class="link next"
        :href="props.nextLink.href"
        @click.prevent="
          router.push(props.nextLink.href);
          emits('change');
        "
      >
        <span class="desc">{{ t("common.desc.next") }}</span>
        <span class="title">{{ props.nextLink.content }}</span>
      </a>
    </div>
  </nav>
</template>

<style scoped>
nav {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 16px;

  padding-top: 24px;
}

.wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 0.5;
  width: 100%;
}

.link {
  display: flex;
  flex-direction: column;

  width: 100%;
  height: 100%;

  border: 1px solid var(--divider-color);
  transition: border-color 0.25s;
  border-radius: 8px;
  padding: 11px 16px 13px;
}

.link:hover {
  border-color: var(--highlight-color);
}

.next {
  align-items: flex-end;
}

.prev {
  align-items: flex-start;
}

.desc {
  line-height: 20px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-color-2);
}

.title {
  line-height: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.25s;
  color: var(--highlight-color-lighter);
}
</style>
