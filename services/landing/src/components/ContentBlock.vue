<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="content-block">
    <h1>{{ props.title }}</h1>
    <slot></slot>
  </div>
</template>

<style>
.content-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  max-width: 912px;
  margin: 0 auto;

  font-size: 16px;
  line-height: 28px;
  font-weight: 400;

  padding-bottom: 48px;
  border-bottom: 1px solid var(--divider-color);
}

.content-block:not(:first-child) {
  margin-top: 24px;
}

.content-block h1 {
  line-height: 40px;
  font-size: 32px;
  font-weight: 600;
  margin: 0;
}

.content-block p {
  margin-top: 16px;
  margin-bottom: 0;
}

.content-block p:not(:last-child) {
  margin-bottom: 16px;
}

.content-block a {
  color: var(--highlight-color-lighter);
  text-decoration: underline;
  text-underline-offset: 2px;
  transition:
    color 0.25s,
    opacity 0.25s;
}

.content-block a:hover {
  color: var(--highlight-color-lightest);
}

.content-block a:active {
  color: var(--highlight-color-lightest);
}

.content-block :not(pre) > code {
  border-radius: 4px;
  padding: 3px 6px;
  background-color: var(--code-bg);
  transition:
    color 0.25s,
    background-color 0.5s;
}

.content-block :not(pre, h1, h2, h3, h4, h5, h6) > code {
  color: var(--code-color);
}

.content-block .custom {
  width: 100%;
  margin: 16px 0;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 16px 16px 8px;
  line-height: 24px;
  font-size: 14px;
}

.content-block .custom p {
  margin: 8px 0;
}

.content-block .custom p:first-child {
  margin: 0;
}

.content-block .custom .title {
  font-weight: 600;
}

.content-block .note {
  background-color: var(--code-note-bg);
}

.content-block .note code {
  color: var(--code-note-color);
  background-color: var(--code-note-bg);
  white-space: nowrap;
}

.content-block ul {
  list-style: disc;
  margin: 0;
  padding-left: 1.25rem;
}

.content-block ul li p {
  margin-top: 0 !important;
}

.content-block ul li + li {
  margin-top: 8px;
}
</style>
