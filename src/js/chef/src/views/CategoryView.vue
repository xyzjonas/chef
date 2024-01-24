<template>
  <div>
    <CategoryTile
      :category="categories.current"
      editable
      @categoryDeleted="$router.push({ name: 'home' })"
      @categoryEdited="$router.push(route.fullPath)"
    />

    <RecipeList :allRecipes="categories.recipes" />
  </div>
</template>

<script setup lang="ts">
import RecipeList from "@/components/RecipeList.vue";
import CategoryTile from "@/components/CategoryTile.vue";
import { useCategoryStore } from "@/stores/categories";
import { useRoute } from "vue-router";

const categories = useCategoryStore();

const route = useRoute();
const categoryId = parseInt(route.params.id as string);

categories.currentId = categoryId;
if (!categories.all.find(cat => cat.id === categoryId)) {
  await categories.fetchSingle(categoryId);
}
</script>
