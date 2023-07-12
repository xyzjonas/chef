<template>
  <div class="px-3">
  <h1 class="title is-3">Add</h1>
  <h2 class="subtitle is-5">a new recipe</h2>

    <RecipeForm
      :data="blankRecipe"
      @posted="routeToNewRecipe"
      @cancel="$router.push({ name: 'home' })"
    />
    
  </div>
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
}
const router = useRouter();
const routeToNewRecipe = (recipe: Recipe) => {
  router.push({ name: 'recipe', params: { id: recipe.id } })
}
</script>
