import axios from 'axios';
import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { API_URL } from '@/constants';

import type { Ingredient } from '@/types';
import { mande } from 'mande';


const api = mande(API_URL + "/ingredients")


export const useIngredientStore = defineStore('ingredient', () => {
  
  const loading = ref<boolean>(false);
  
  const all = ref<Ingredient[]>([]);

  const getById = computed(() => {
    return (ingredientId: number) => { all.value.find(r => r.id === ingredientId) };
  })


  async function fetch() {
    loading.value = true
    api.get<Ingredient[]>()
       .then(ingredient => all.value = ingredient.sort((a: Ingredient, b: Ingredient) => a.name > b.name ? 1 : -1))
       .catch(err => console.error(err))
       .finally(() => loading.value = false);
  }
  
  async function fetchSingle(ingredientId: number) {
    loading.value = true
    api.get<Ingredient>(ingredientId)
       .then(newIng => all.value.map(r => r.id === newIng.id ? newIng : r))
       .catch(err => console.error(err))
       .finally(() => loading.value = false);
  }

//   async function create(recipeData: CreateRecipe) {
//     loading.value = true
//     recipesApi
//         .post<Recipe>(recipeData)
//         .then(r => {
//           recipes.value.push(r);
//           recipes.value.sort((a: Recipe, b: Recipe) => a.title > b.title ? 1 : -1);
//         })
//         .catch(err => console.error(err))
//         .finally(() => loading.value = false);
//   }

  async function update(ingredientData: Ingredient): Promise<Ingredient> {
    loading.value = true
    try {
      const result = await api.put<Ingredient>(ingredientData.id, ingredientData);
      all.value = all.value.filter(ing => ing.id !== ingredientData.id);
      all.value.push(result);
      all.value.sort((a: Ingredient, b: Ingredient) => a.name > b.name ? 1 : -1);
      return result
    } catch(err) {
      console.error(err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteById(ingredientId: number) {
    loading.value = true
    console.debug(`Deleting ingredient id=${ingredientId}.`)
    try {
      const result = api.delete(ingredientId);
      all.value = all.value.filter(ing => ing.id !== ingredientId);
    } catch(err) {
      console.error(err);
    }
    loading.value = false;
  }

  return { all, loading, fetch, update, fetchSingle, deleteById }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useIngredientStore, import.meta.hot))
}
