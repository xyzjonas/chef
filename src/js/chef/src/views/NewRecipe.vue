<template>
  <q-page padding class="flex flex-col">
    <h1 class="text-4xl mb-3">Add a new recipe</h1>

    <RecipeForm
      :data="blankRecipe"
      id="blank"
      @posted="routeToNewRecipe"
      @cancel="$router.push({ name: 'recipes' })"
      class="flex-1"
    />
  </q-page>
</template>

<script setup lang="ts">
import RecipeForm from "@/components/RecipeForm.vue";
import type { CreateRecipe, Recipe } from "@/types";
import { useRouter } from "vue-router";



const blankRecipe: CreateRecipe = {
  title: "",
  portions: 4,
  ingredients: [],
  tags: [],
  body: "",
};
const router = useRouter();
const routeToNewRecipe = (recipe: Recipe) => {
  router.push({ name: "recipe", params: { id: recipe.id } });
};
</script>