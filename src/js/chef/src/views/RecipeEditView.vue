<template>
  <q-page padding class="flex flex-col">
    <h1 class="text-4xl mb-3">Edit recipe</h1>
    <RecipeForm
      v-if="current"
      :id="`${current.id}`"
      :data="current"
      @posted="routeback"
      @cancel="routeback"
      class="flex-1"
    />
    <NotFound v-else />
  </q-page>
</template>

<script setup lang="ts">
import { useRecipeStore } from '@/stores/recipe';
import { storeToRefs } from 'pinia';
import { useRoute, useRouter } from 'vue-router';

import RecipeForm from '@/components/RecipeForm.vue';
import NotFound from '@/components/NotFound.vue';

const recipes = useRecipeStore();
const { current, currentId } = storeToRefs(recipes);

const router = useRouter();
const route = useRoute();
const recipeId = parseInt(route.params.id as string);

currentId.value = recipeId;

if (!current.value) {
  await recipes.fetchSingle(recipeId);
}

if (!current.value) {
  router.push({
    name: "notfound",
    query: { path: router.currentRoute.value.fullPath },
  });
}

const routeback = () => {
    router.push({ name: 'recipe', params: { id: current.value?.id } })
}

</script>

<style lang="scss" scoped></style>
