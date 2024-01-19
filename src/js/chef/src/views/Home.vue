<template>
  <div>
      <recipe-list
        class="mb-4 mt-5"
        v-if="recipes.favorites.length > 0"
        :allRecipes="recipes.favorites"
        :hideSearch="true"
        :hideFilters="true"
        :hideTitle="true"
      />
      <div class="category-tiles">
        <category-tile
            v-for="category in categories.all" :category="category"
            @clicked="$router.push({ name: 'category', params: { id: category.id } })"
          />
      </div>

  </div>
</template>

<script setup lang="ts">
import CategoryTile from "@/components/CategoryTile.vue";
import RecipeList from "@/components/RecipeList.vue"
import { useCategoryStore } from "@/stores/categories";
import { useRecipeStore } from "@/stores/recipe";
import { computed } from "vue";


const categories = useCategoryStore();
const recipes = useRecipeStore();

await recipes.fetch(false)

</script>

<style lang="scss" scoped>
.category-tiles {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.3em;
}

@media only screen and (max-width: 900px) {
  .category-tiles {
    grid-template-columns: 1fr 1fr;
  }
}

@media only screen and (max-width: 600px) {
  .category-tiles {
    grid-template-columns: 1fr;
  }
}

</style>
