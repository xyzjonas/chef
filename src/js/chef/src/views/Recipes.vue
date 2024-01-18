<template>
  <div>
    <Transition name="loading" mode="out-in">
      <Suspense>
        
        <template #default>
          <recipe-list :allRecipes="recipes"/>
        </template>

        <template #fallback>
          <loading-section :loading="true" />
        </template>
      </Suspense>
    </Transition>
  </div>
</template>

<script lang="ts" setup>
import RecipeList from "@/components/RecipeList.vue";
import LoadingSection from "@/components/LoadingSection.vue"


import { useRecipeStore } from "@/stores/recipe";
import { storeToRefs } from "pinia";

const store = useRecipeStore();
await store.fetch(false);

const { recipes } = storeToRefs(store)
</script>
