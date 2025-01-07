<template>
  <q-page>
    <recipe-list storage-id="recipes" :allRecipes="recipes" :loading="loading"/>
  </q-page>
</template>

<script lang="ts" setup>
import RecipeList from "@/components/RecipeList.vue";

import { useRecipeStore } from "@/stores/recipe";
import { storeToRefs } from "pinia";
import { onMounted } from "vue";

const store = useRecipeStore();
const { loading, recipes } = storeToRefs(store)
let loaded = false

if (recipes.value.length === 0) {
  await store.fetch();
  loaded = true
}

onMounted(() => {
  if (!loaded) {
    store.fetch()
  }
})

</script>
