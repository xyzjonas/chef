<template>
  <div class="view">
    <div class="category-tiles" v-if="categories.all.length > 0">
        <category-tile
            v-for="category in categories.all" :category="category"
            :key="category.id"
            @clicked="$router.push({ name: 'category', params: { id: category.id } })"
            class="h-[12rem]"
          />
      </div>
      <div v-else id="empty">
        <empty-box title="No categories created yet" subtitle="Start by adding a new category." linkText="Add a new category" routeName="newcategory" :icon="Rocket" />
      </div>

  </div>
</template>

<script setup lang="ts">
import CategoryTile from "@/components/CategoryTile.vue";
import EmptyBox from "@/components/ui/EmptyBox.vue";
import { useCategoryStore } from "@/stores/categories";
import { useRecipeStore } from "@/stores/recipe";
import Rocket from "@/components/icons/Rocket.vue";


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

#empty {
  min-height: 80dvh;
  display: flex;
  flex-direction: column;
}

</style>
