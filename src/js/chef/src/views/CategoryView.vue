<template>
  <div>
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="categories.loading" :loading="categories.loading"/>
    <CategoryTile
      v-else
      :category="categories.current"
      :editable="true"
      @categoryDeleted="$router.push({ name: 'home' })"
      @categoryEdited="$router.push(route.fullPath)"
    />
    </transition>

    <transition name="loading" mode="out-in">
    <LoadingSection v-if="recipes.loading" :loading="recipes.loading"/>
    <div v-else class="px-2 pt-3 recipe-list">
      <RecipeList :allRecipes="categories.recipes" />
    </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import RecipeList from "@/components/RecipeList.vue";
import CategoryTile from "@/components/CategoryTile.vue";
import LoadingSection from "@/components/LoadingSection.vue"
import { useCategoryStore } from "@/stores/categories";
import { useRecipeStore } from "@/stores/recipe";
import { useRoute } from "vue-router";


const categories = useCategoryStore();
const recipes = useRecipeStore();

const route = useRoute();
const categoryId = parseInt(route.params.id);
categories.currentId = categoryId;
if (!categories.all.find(cat => cat.id === categoryId)) {
  categories.fetchSingle(categoryId);
}
</script>

<style lang="scss" scoped>
.recipe-list {
  min-height: 1800px;
}
</style>
