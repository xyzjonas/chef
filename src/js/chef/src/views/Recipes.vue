<template>
  <div class="recipes px-3">
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="recipes.loading" :loading="recipes.loading" />
    <RecipeList v-else :allRecipes="recipes.recipes"/>
    </transition>
  </div>  
</template>

<script setup lang="ts">
import RecipeList from "@/components/RecipeList.vue";
import LoadingSection from "@/components/LoadingSection.vue"


import { useRecipeStore } from "@/stores/recipe";

const recipes = useRecipeStore();
</script>
