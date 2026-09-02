<template>
  <q-card
    flat
    bordered
    class="card hover:cursor-pointer transition"
    @click="router.push({ name: 'recipe', params: { id: recipe.id } })"
  >
    <q-img
      :src="recipe.thumbnail_image ?? 'none'"
      error-src="@/assets/notfound.jpg"
      :ratio="1"
    />

    <q-card-section class="flex flex-col">
      <div v-if="recipe.tags.length > 0" class="flex gap-1 mb-3">
        <RecipeTag
          v-for="tag in recipe.tags.slice(0, 3)"
          :key="tag.id"
          :tag="tag"
        />
      </div>
      <h2
        class="my-0 text-xl line-height-tight first-letter:uppercase transition-colors"
      >
        {{ recipe.title }}
      </h2>
      <div class="text-xs first-letter:uppercase text-gray-7 dark:text-gray-4">
        {{ recipe.subtitle }}
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";

import router from "@/router";
import RecipeTag from "./RecipeTag.vue";

defineProps<{ recipe: Recipe }>();
</script>

<style lang="scss" scoped>
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
  // border-color: var(--primary-100);
  cursor: pointer;
}

.card:hover h2 {
  color: var(--primary-100);
}

.card:hover .q-img__image {
  transform: rotate(45deg);
}
</style>
