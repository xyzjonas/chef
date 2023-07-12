<template>
  <div>
    <!-- title -->
    <h1 class="title is-4 mt-5">{{ ingredients.length }} Ingredients</h1>

    <!-- search -->
    <p class="control has-icons-left">
      <input 
        v-model="search"
        class="input is-rounded"
        type="text"
        placeholder="search">
      <span class="icon is-small is-left">
        <i class="fas fa-search"></i>
      </span>
    </p>

    <div class="section px-3 pt-4">
      <IngredientListItem
        v-for="(ingredient, index) in ingredients" :key="`${ingredient},${index},list`"
        :ingredient="ingredient"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import IngredientListItem from "@/components/IngredientListItem.vue";
import { useIngredientStore } from "@/stores/ingredient";
import { computed, ref } from "vue";
import { replaceUnicode } from "@/utils";

const ingredientsStore = useIngredientStore();

const search = ref<string>();

const ingredients = computed(() => {
  if (!search.value || search.value === ""){
    return ingredientsStore.all;
  }
  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return ingredientsStore.all.filter(ing => {
    const match = re.exec(replaceUnicode(ing.name.toLowerCase()))
    if (match) {
      return true;
    }
    return false;
  })
})
</script>

<style>

</style>