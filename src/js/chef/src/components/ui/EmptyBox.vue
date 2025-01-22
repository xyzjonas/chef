<template>
  <section
    class="flex flex-col items-center text-center justify-center min-h-xl"
  >
    <component
      v-if="icon"
      :is="icon"
      width="5rem"
      class="dark:text-white light:text-dark mb-5"
    />
    <h1 class="text-[3rem] line-height-[3rem]">
      {{ title ?? "No assets created yet" }}
    </h1>
    <h2 class="text-2xl">{{ subtitle ?? "This is really really empty" }}</h2>
    <router-link v-if="routeName" :to="{ name: routeName }" class="link">{{
      linkText
    }}</router-link>
  </section>
</template>
<script lang="ts" setup>
import type { Component } from "vue";
defineProps<{
  title?: string;
  subtitle?: string;
  linkText?: string;
  routeName?: string;
  icon?: Component;
}>();
</script>
<style lang="css" scoped>
.link {  
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.body--dark .link {
  color: white;
}

.body--light .link {
  color: var(--q-dark);
}
</style>
