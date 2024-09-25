<template>
  <main>
    <recipe-list :allRecipes="recipes"/>
  </main>
</template>

<script lang="ts" setup>
import RecipeList from "@/components/RecipeList.vue";

import { useRecipeStore } from "@/stores/recipe";
import { storeToRefs } from "pinia";

const store = useRecipeStore();
await store.fetch(false);

const { recipes } = storeToRefs(store)
</script>
