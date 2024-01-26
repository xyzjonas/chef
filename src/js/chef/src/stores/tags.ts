// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { API_URL } from '@/constants';

import type { Tag } from '@/types';
import { mande } from 'mande';


const recipesApi = mande(API_URL + "/tags")


export const useTagStore = defineStore('tag', () => {
  
  const loading = ref<boolean>(false);
  
  const all = ref<Tag[]>([]);

  const getById = computed(() => {
    return (ingredientId: number) => { all.value.find(r => r.id === ingredientId) };
  })


  async function fetch() {
    loading.value = true
    recipesApi
        .get<Tag[]>()
        .then(tag => all.value = tag.sort((a: Tag, b: Tag) => a.name > b.name ? 1 : -1))
        .catch(err => console.error(err))
        .finally(() => loading.value = false);
  }
  
  async function fetchSingle(ingredientId: number) {
    loading.value = true
    recipesApi
        .get<Tag>(ingredientId)
        .then(newTag => all.value.map(tag => tag.id === newTag.id ? newTag : tag))
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

//   async function update(recipeData: Recipe) {
//     loading.value = true
//     recipesApi
//         .put<Recipe>(recipeData.id, recipeData)
//         .then(r => {
//           recipes.value = recipes.value.filter(r => r.id !== recipeData.id);
//           recipes.value.push(r);
//           recipes.value.sort((a: Recipe, b: Recipe) => a.title > b.title ? 1 : -1);
//         })
//         .catch(err => console.error(err))
//         .finally(() => loading.value = false);
//   }

//   async function deleteById(recipeId: number) {
//     loading.value = true
//     console.debug(`Deleting recipe id=${recipeId}.`)
//     return recipesApi
//         .delete(recipeId)
//         .then(() => recipes.value = recipes.value.filter(r => r.id !== recipeId))
//         .catch(err => console.error(err))
//         .finally(() => loading.value = false);
//   }


  return { all, loading, fetch, fetchSingle }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTagStore, import.meta.hot))
}
