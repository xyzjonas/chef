<template>
  <q-card
    flat
    bordered
    class="hover:cursor-pointer hover:border-primary transition"
    @click="router.push({ name: 'recipe', params: { id: recipe.id } })"
  >
    <q-img
      :src="recipe.thumbnail_image ?? 'none'"
      error-src="@/assets/notfound.jpg"
      :ratio="1.6"
    />

    <q-card-section class="flex flex-col">
      <div class="text-lg uppercase line-height-snug">{{ recipe.title }}</div>
      <div class="text-xs uppercase text-gray-7 dark:text-gray-4">
        {{ recipe.subtitle }}
      </div>
      <div class="flex gap-1 mt-3">
        <q-badge rounded v-for="tag in recipe.tags">{{ tag.name }}</q-badge>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";

import router from "@/router";

defineProps<{ recipe: Recipe }>();
</script>

<style lang="css" scoped>
.title {
  font-size: medium;
  font-weight: 500;
  letter-spacing: -1px;
}

.subtitle {
  font-size: small;
}

.card {
  transition: 0.2s ease-in-out;
}

.card:hover {
  border-color: var(--primary-100);
  cursor: pointer;
}

.card:hover p {
  text-decoration: underline;
}
</style>
