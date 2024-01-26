// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { API_URL } from '@/constants';

import type { Unit } from '@/types';
import { mande } from 'mande';


const recipesApi = mande(API_URL + "/units")


export const useUnitsStore = defineStore('unit', () => {
  
  const loading = ref<boolean>(false);
  
  const all = ref<Unit[]>([]);

  async function fetch() {
    loading.value = true
    recipesApi
        .get<Unit[]>()
        .then(unit => all.value = unit.sort((a: Unit, b: Unit) => a.name > b.name ? 1 : -1))
        .catch(err => console.error(err))
        .finally(() => loading.value = false);
  }
  
  return { all, loading, fetch }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUnitsStore, import.meta.hot))
}
