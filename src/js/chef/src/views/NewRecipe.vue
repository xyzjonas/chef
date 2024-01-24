<template>
  <div>
    <h1>Add a new recipe</h1>

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
};
const router = useRouter();
const routeToNewRecipe = (recipe: Recipe) => {
  router.push({ name: "recipe", params: { id: recipe.id } });
};
</script>
<style lang="css" scoped>
h1 {
  font-weight: 100;
}
</style>
