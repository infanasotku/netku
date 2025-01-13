<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t, tm } = useI18n();
const localt = (key: string) => t("content.skills." + key);
const localtm = (key: string) =>
  tm("content.skills." + key) as Array<{ name: string }>;
</script>

<template>
  <main>
    <ContentBlock :title="localt('backend.title')">
      <i18n-t
        scope="global"
        keypath="content.skills.backend.description"
        tag="p"
      >
        <a href="https://www.python.org/" target="_blank">{{
          localt("backend.python")
        }}</a>
        <a href="https://go.dev/" target="_blank">{{ localt("backend.go") }}</a>
        <code>{{ localt("backend.safety") }}</code>
        <code>{{ localt("backend.load") }}</code>
        <code>{{ localt("backend.layer") }}</code>
        <code>{{ localt("backend.database") }}</code>
      </i18n-t>
      <ul>
        <li v-for="skill in localtm('backend.skills')">
          <p>{{ skill.name }}</p>
        </li>
      </ul>
    </ContentBlock>
    <ContentBlock :title="localt('frontend.title')">
      <i18n-t
        scope="global"
        keypath="content.skills.frontend.description"
        tag="p"
      >
        <code>{{ localt("frontend.spa") }}</code>
        <a href="https://vuejs.org/" target="_blank">{{
          localt("frontend.vue")
        }}</a>
        <a href="https://www.typescriptlang.org/" target="_blank">{{
          localt("frontend.ts")
        }}</a>
        <a href="https://react.dev/" target="_blank">{{
          localt("frontend.react")
        }}</a>
        <a href="https://threejs.org/" target="_blank">{{
          localt("frontend.three")
        }}</a>
      </i18n-t>
      <ul>
        <li v-for="skill in localtm('frontend.skills')">
          <p>{{ skill.name }}</p>
        </li>
      </ul>
    </ContentBlock>
    <ContentBlock :title="localt('devops.title')">
      <i18n-t
        scope="global"
        keypath="content.skills.devops.description"
        tag="p"
      >
        <code>{{ localt("devops.ci") }}</code>
        <code>{{ localt("devops.monitoring") }}</code>
        <code>{{ localt("devops.integration") }}</code>
        <code>{{ localt("devops.any") }}</code>
      </i18n-t>
      <ul>
        <li v-for="skill in localtm('devops.skills')">
          <p>{{ skill.name }}</p>
        </li>
      </ul>
      <div class="custom note">
        <p class="title">
          <code>{{ t("common.todo.title") }}</code>
        </p>
        <p>{{ t("common.todo.description") }}</p>
      </div>
    </ContentBlock>
    <slot></slot>
  </main>
</template>

<style scoped></style>
