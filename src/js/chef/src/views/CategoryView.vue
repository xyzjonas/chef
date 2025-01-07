<template>
  <div v-if="categories.current">
    <CategoryTile
      :category="categories.current"
      editable
      @categoryDeleted="$router.push({ name: 'home' })"
      @categoryEdited="$router.push(route.fullPath)"
      class="h-[12rem] mb-3"
    />

    <RecipeList :storage-id="`${categories.current.id}`" :allRecipes="categories.recipes"/>
  </div>
  <NotFound v-else />
</template>

<script setup lang="ts">
import RecipeList from "@/components/RecipeList.vue";
import CategoryTile from "@/components/CategoryTile.vue";
import { useCategoryStore } from "@/stores/categories";
import { useRoute } from "vue-router";
import NotFound from "@/components/NotFound.vue";

const categories = useCategoryStore();

const route = useRoute();
const categoryId = parseInt(route.params.id as string);

categories.currentId = categoryId;
if (!categories.all.find(cat => cat.id === categoryId)) {
  await categories.fetchSingle(categoryId);
}
</script>
