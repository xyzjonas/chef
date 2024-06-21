<template>
  <ui-card :background-image="image" @click="navigateTo(`/recipes/${recipe.id}`)">
    <p class="title">{{ recipe.title?.toUpperCase() }}</p>
    <p class="subtitle">{{ recipe.subtitle }}</p>
    <div class="flex flex-wrap gap-1 mt-2">
      <ui-pin v-for="tag in recipe.tags" :text="tag.name" size="small" color="#a8f2cd"/>
    </div>
  </ui-card>
</template>

<script setup lang="ts">
import type { RecipeListItem } from "@/types";

interface Props {
  recipe: RecipeListItem;
}
const props = defineProps<Props>();

const image = computed(() => props.recipe.thumbnail_image ?? '/notfound.jpg')
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
  transition: .2s ease-in-out;
}

.card:hover {
  border-color: var(--primary-100);
  cursor: pointer;
}

.card:hover p {
  text-decoration: underline;
}
</style>
