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
        .then((tags: Tag[]) => all.value = tags.sort((a: Tag, b: Tag) => a.name > b.name ? 1 : -1))
        .catch((err: unknown) => console.error(err))
        .finally(() => loading.value = false);
  }
  
  async function fetchSingle(ingredientId: number) {
    loading.value = true
    recipesApi
        .get<Tag>(ingredientId)
        .then((newTag: Tag) => all.value.map(tag => tag.id === newTag.id ? newTag : tag))
        .catch((err: unknown) => console.error(err))
        .finally(() => loading.value = false);
  }


  return { all, loading, fetch, fetchSingle }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTagStore, import.meta.hot))
}
