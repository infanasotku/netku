<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
});

const title = props.title.toLowerCase().replace(" ", "-");
const titleId = "#" + title;

const route = useRoute();

const moveToTitle = () => {
  document.getElementById(titleId)?.scrollIntoView();
};

onMounted(() => {
  if (route.fullPath.includes(titleId)) {
    moveToTitle();
  }
});
</script>

<template>
  <div class="content-block">
    <h1 :id="title">
      {{ props.title }}
      <a @click="moveToTitle" :href="titleId">&ZeroWidthSpace;</a>
    </h1>
    <slot></slot>
  </div>
</template>

<style lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

.content-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  font-size: 16px;
  line-height: 28px;
  font-weight: 400;

  padding-bottom: 48px;
  border-bottom: 1px solid var(--divider-color);

  &:not(:first-child) {
    margin-top: 24px;
  }

  p {
    margin-top: 16px;
    margin-bottom: 0;

    &:not(:last-child) {
      margin-bottom: 16px;
    }
  }

  h1 {
    position: relative;

    line-height: 40px;
    font-size: 32px;
    font-weight: 600;
    margin: 0;

    a {
      top: 0;
      left: 0;
      position: absolute;
      margin-left: -0.87em;

      display: flex;
      flex-direction: row;

      opacity: 0;
      user-select: none;
      text-decoration: none;

      &::before {
        content: "#";
        font-size: 32px;
        display: block;
      }
    }

    &:hover {
      a {
        opacity: 1;
      }
    }
  }

  a {
    color: var(--highlight-color-lighter);
    text-decoration: underline;
    text-underline-offset: 2px;
    transition:
      color 0.25s,
      opacity 0.25s;

    &:hover {
      color: var(--highlight-color-lightest);
    }

    &:active {
      color: var(--highlight-color-lightest);
    }
  }

  code:not(pre) {
    border-radius: 4px;
    padding: 3px 6px;
    background-color: var(--code-bg);
    white-space: nowrap;
    transition:
      color 0.25s,
      background-color 0.5s;
  }

  code:not(pre, h1, h2, h3, h4, h5, h6) {
    color: var(--code-color);
  }

  .custom {
    width: 100%;
    margin: 16px 0;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 16px 16px 8px;
    line-height: 24px;
    font-size: 14px;

    p {
      margin: 8px 0;

      &:first-child {
        margin: 0;
      }
    }

    .title {
      font-weight: 600;
    }

    &.note {
      background-color: var(--code-note-bg);

      code {
        color: var(--code-note-color);
        background-color: var(--code-note-bg);
        white-space: nowrap;
      }
    }
  }

  ul {
    list-style: disc;
    margin: 0;
    padding-left: 1.25rem;

    li {
      p {
        margin-top: 0 !important;
      }

      & + li {
        margin-top: 8px;
      }
    }
  }

  @include media-breakpoint-down(md) {
    h1 {
      a {
        right: 0;
        left: unset;
        margin-right: -0.87em;
        margin-left: 0;
      }
    }
  }
}
</style>
