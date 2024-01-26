<template>
  <div class="view">
      <recipe-list
        class="mb-4 mt-5"
        v-if="recipes.favorites.length > 0"
        :allRecipes="recipes.favorites"
        :hideSearch="true"
        :hideFilters="true"
        :hideTitle="true"
      />
      <div class="category-tiles" v-if="categories.all.length > 0">
        <category-tile
            v-for="category in categories.all" :category="category"
            :key="category.id"
            @clicked="$router.push({ name: 'category', params: { id: category.id } })"
          />
      </div>
      <empty-box v-else
        linkText="add a new category"
        routeName="newcategory"
      />

  </div>
</template>

<script setup lang="ts">
import CategoryTile from "@/components/CategoryTile.vue";
import RecipeList from "@/components/RecipeList.vue"
import EmptyBox from "@/components/ui/EmptyBox.vue";
import { useCategoryStore } from "@/stores/categories";
import { useRecipeStore } from "@/stores/recipe";
import { computed } from "vue";


const categories = useCategoryStore();
const recipes = useRecipeStore();

await recipes.fetch(false)

</script>

<style lang="scss" scoped>

.view {
  height: 80dvh;
}

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
