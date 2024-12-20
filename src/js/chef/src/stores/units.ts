import { defineStore, acceptHMRUpdate } from 'pinia'
import { ref } from 'vue';

import { API_URL } from '@/constants';

import type { Unit } from '@/types';
import { mande } from 'mande';
import { useLocalStorage } from '@vueuse/core';


const recipesApi = mande(API_URL + "/units")

const all = useLocalStorage<Unit[]>("units", [])

export const useUnitsStore = defineStore('unit', () => {
  
  const loading = ref<boolean>(false);

  async function fetch() {
    loading.value = true
    recipesApi
        .get<Unit[]>()
        .then((units: Unit[]) => all.value = units.sort((a: Unit, b: Unit) => a.name > b.name ? 1 : -1))
        .catch((err: unknown) => console.error(err))
        .finally(() => loading.value = false);
  }
  
  return { all, loading, fetch }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUnitsStore, import.meta.hot))
}
