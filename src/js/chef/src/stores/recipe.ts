// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { mande } from 'mande';

import { API_URL } from '@/constants';

import type { CreateRecipe, Recipe } from '@/types';
import { useTagStore } from './tags';
import { useUnitsStore } from './units';


const recipesApi = mande(API_URL + "/recipes")


export const useRecipeStore = defineStore('recipe', () => {

  const tagsStore = useTagStore();
  const unitsStore = useUnitsStore();
  
  const loading = ref(false);

  const recipes = ref<Recipe[]>([]);

  const all = computed(() => recipes);
  const favorites = computed(() => recipes.value.filter(rec => rec.favorite));

  async function fetch(force: boolean = true) {
    if (recipes.value.length > 0 && !force) {
      return
    }

    loading.value = true
    const result = await recipesApi.get<Recipe[]>()
    recipes.value = result.sort((a: Recipe, b: Recipe) => a.title > b.title ? 1 : -1);
    setTimeout(() => { loading.value = false }, 300);
  }
  
  async function fetchSingle(recipeId: number): Promise<Recipe> {
    loading.value = true
    try {
      const recipe = await recipesApi.get<Recipe>(recipeId);
      recipes.value.map(r => r.id === recipe.id ? recipe : r);
      loading.value = false;
      return recipe;
    } catch(err) {
      loading.value = false;
      console.error(err)
    }
  }

  async function create(recipeData: CreateRecipe): Promise<Recipe> {
    loading.value = true;
    console.debug("Creating recipe.");
    const recipe = await recipesApi.post<Recipe>(recipeData);
    recipes.value.push(recipe);
    recipes.value.sort((a: Recipe, b: Recipe) => a.title > b.title ? 1 : -1);
    loading.value = false;
    
    // Let's update other stores in case new items were added.
    tagsStore.fetch();
    unitsStore.fetch();
    return recipe;
  }

  async function update(recipeData: Recipe): Promise<Recipe> {
    loading.value = true
    console.debug(`Updating recipe id=${recipeData.id}.`)
    const result = await recipesApi.put<Recipe>(recipeData.id, recipeData)
    recipes.value = recipes.value.filter(r => r.id !== recipeData.id);
    recipes.value.push(result);
    recipes.value.sort((a: Recipe, b: Recipe) => a.title > b.title ? 1 : -1);
    loading.value = false;

    // Let's update other stores in case new items were added.
    tagsStore.fetch();
    unitsStore.fetch();
    return result;
  }

  async function deleteById(recipeId: number) {
    loading.value = true
    console.debug(`Deleting recipe id=${recipeId}.`)
    try {
      await recipesApi.delete(recipeId);
      recipes.value = recipes.value.filter(rec => rec.id !== recipeId);
    } catch(err) {
      console.error(err);
    }
    loading.value = false;

    // Let's update other stores in case new items were removed.
    tagsStore.fetch();
    unitsStore.fetch();
  }


  return { recipes, all, favorites, loading, fetch, fetchSingle, create, update, deleteById }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useRecipeStore, import.meta.hot))
}
