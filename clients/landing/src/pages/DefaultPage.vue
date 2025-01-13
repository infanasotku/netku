<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
  <main>
    <ContentBlock :title="t('content.default.header')">
      <p>
        {{ t("content.default.description") }}
      </p>
    </ContentBlock>
    <slot></slot>
  </main>
</template>

<style scoped></style>
