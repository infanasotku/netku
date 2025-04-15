<script setup lang="ts">
import ContentBlock from "@/components/ContentBlock.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const localt = (key: string) => t("content.aboutme." + key);
</script>

<template>
  <main>
    <ContentBlock :title="localt('title')">
      <i18n-t scope="global" keypath="content.aboutme.description" tag="p">
        <a href="https://www.python.org/" target="_blank">{{
          localt("backend")
        }}</a>
        <code>{{ localt("experience") }}</code>
        <code>{{ localt("microservice") }}</code>
        <a href="https://fastapi.tiangolo.com/" target="_blank">{{
          localt("fastapi")
        }}</a>
        <code>{{ localt("async") }}</code>
        <a href="https://docs.docker.com/compose/" target="_blank">{{
          localt("docker")
        }}</a>
        <a href="https://docs.celeryq.dev/en/stable/" target="_blank">{{
          localt("celery")
        }}</a>
        <a href="https://www.rabbitmq.com/" target="_blank">{{
          localt("rabbit")
        }}</a>
        <code>{{ localt("eda") }}</code>
        <code>{{ localt("unit") }}</code>
        <code>{{ localt("integration") }}</code>
        <a href="https://docs.pytest.org/en/stable/" target="_blank">{{
          localt("pytest")
        }}</a>
        <a href="https://playwright.dev/" target="_blank">{{
          localt("playwright")
        }}</a>

        <a href="https://go.dev/" target="_blank">{{ localt("go") }}</a>
        <a href="https://vuejs.org/" target="_blank">{{ localt("vue") }}</a>
        <code>{{ localt("spa") }}</code>

        <a href="https://www.postgresql.org/" target="_blank">{{
          localt("postgres")
        }}</a>
        <code>{{ localt("tcp") }}</code>
        <a href="https://nginx.org/en/" target="_blank">{{
          localt("nginx")
        }}</a>
        <code>{{ localt("ci") }}</code>
        <code>{{ localt("code") }}</code>
      </i18n-t>

      <i18n-t scope="global" keypath="content.aboutme.description2" tag="p">
        <code>{{ localt("five") }}</code>
        <a href="https://vuejs.org/" target="_blank">{{ localt("vue") }}</a>
        <a href="https://www.typescriptlang.org/" target="_blank">{{
          localt("ts")
        }}</a>
        <code>{{ localt("py_backend") }}</code>
        <code>{{ localt("reliable") }}</code>
        <code>{{ localt("scalable") }}</code>

        <a href="https://www.python.org/" target="_blank">{{
          localt("backend")
        }}</a>
        <code>{{ localt("experience") }}</code>
        <code>{{ localt("microservice") }}</code>
        <a href="https://fastapi.tiangolo.com/" target="_blank">{{
          localt("fastapi")
        }}</a>
        <code>{{ localt("async") }}</code>
        <a href="https://docs.docker.com/compose/" target="_blank">{{
          localt("docker")
        }}</a>
        <a href="https://docs.celeryq.dev/en/stable/" target="_blank">{{
          localt("celery")
        }}</a>
        <a href="https://www.rabbitmq.com/" target="_blank">{{
          localt("rabbit")
        }}</a>
        <code>{{ localt("eda") }}</code>
        <code>{{ localt("unit") }}</code>
        <code>{{ localt("integration") }}</code>
        <a href="https://docs.pytest.org/en/stable/" target="_blank">{{
          localt("pytest")
        }}</a>
        <a href="https://playwright.dev/" target="_blank">{{
          localt("playwright")
        }}</a>

        <a href="https://go.dev/" target="_blank">{{ localt("go") }}</a>
        <a href="https://vuejs.org/" target="_blank">{{ localt("vue") }}</a>
        <code>{{ localt("spa") }}</code>

        <a href="https://www.postgresql.org/" target="_blank">{{
          localt("postgres")
        }}</a>
        <code>{{ localt("tcp") }}</code>
        <a href="https://nginx.org/en/" target="_blank">{{
          localt("nginx")
        }}</a>
        <code>{{ localt("ci") }}</code>
        <code>{{ localt("code") }}</code>
      </i18n-t>

      <div class="custom note">
        <p class="title">
          <code>{{ localt("note.title") }}</code>
        </p>
        <i18n-t scope="global" keypath="content.aboutme.note.body" tag="p">
          <code>{{ localt("note.observation") }}</code>
          <code>{{ localt("note.presentation") }}</code>
          <code>{{ localt("note.development") }}</code>
          <code>{{ localt("note.test") }}</code>
          <code>{{ localt("note.bug") }}</code>
          <a target="_blank" href="https://t.me/infanasotku">{{
            localt("note.email")
          }}</a>
        </i18n-t>
      </div>
    </ContentBlock>
    <slot></slot>
  </main>
</template>

<style scoped></style>
