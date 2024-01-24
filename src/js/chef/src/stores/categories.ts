import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { API_URL } from '@/constants';

import type { Category, CreateCategory, Recipe } from '@/types';
import { mande } from 'mande';
import { useRecipeStore } from './recipe';


const api = mande(API_URL + "/categories")


export const useCategoryStore = defineStore('category', () => {
  
    const loading = ref<boolean>(false);
    const all = ref<Category[]>([]);
    
    const currentId = ref<number>(); // to be updated from the view
    const current = computed(() => all.value.find(cat => cat.id === currentId.value));

    const imageCache = ref<number[]>([]);

    const recipesStore = useRecipeStore();
    const recipes = computed<Recipe[]>(() => {
        return recipesStore.all.value.filter(rec => {
            if (!current.value) {
                return false;
            }
            const recipeTagsIds = new Set(rec.tags.map(t => t.id));
            if (current.value.tags.length === 0) {
                return true;
            }
            return current.value.tags
                .map(tag => recipeTagsIds.has(tag.id))
                .reduce((prev: boolean, next: boolean) => prev && next)
        })
    });

    async function fetch() {
    loading.value = true
    try {
        const response = await api.get<Category[]>();
        all.value = response.sort((a: Category, b: Category) => a.name > b.name ? 1 : -1);
    } catch(err) {
        console.error(err);
    }
    loading.value = false;
    }

    async function fetchSingle(categoryId: number) {
    loading.value = true
    try {
        const response = await api.get<Category>(categoryId);
        all.value.map(cat => cat.id === response.id ? response : cat);
    } catch(err) {
        console.error(err);
    }
    loading.value = false;
    }

    async function create(categoryData: CreateCategory) {
    loading.value = true
    try {
        const result = await api.post<Category>(categoryData)
        all.value.push(result);
        all.value.sort((a: Category, b: Category) => a.name > b.name ? 1 : -1)
    } catch(err) {
        console.error(err);
    }
    loading.value = false;
    }

    async function update(categoryData: Category) {
    loading.value = true
    try {
        const result = await api.put<Category>(categoryData.id, categoryData)
        all.value = all.value.filter(r => r.id !== categoryData.id);
        all.value.push(result);
        all.value.sort((a: Category, b: Category) => a.name > b.name ? 1 : -1);
    } catch(err) {
        console.error(err);
    }
    loading.value = false;
    }

    async function deleteById(categoryId: number) {
        loading.value = true
        console.debug(`Deleting category id=${categoryId}.`)
        try {
            await api.delete(categoryId);
            all.value = all.value.filter(cat => cat.id !== categoryId);
        } catch(err) {
            console.error(err);
        } finally {
            loading.value = false;
        }
    }


    return { all, loading, imageCache, currentId, current, recipes, fetch, fetchSingle, create, update, deleteById }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useCategoryStore, import.meta.hot))
}
