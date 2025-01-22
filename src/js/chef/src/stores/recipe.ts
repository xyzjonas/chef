import { acceptHMRUpdate, defineStore } from "pinia";
import { computed, ref } from "vue";

import { mande } from "mande";

import { API_URL } from "@/constants";

import { useChefApi } from "@/composables/api";
import type { ChefNotification, CreateRecipe, Recipe } from "@/types";
import { catchError } from "@/utils";
import { useEventBus, useLocalStorage } from "@vueuse/core";
import { useQuasar } from "quasar";
import { useTagStore } from "./tags";
import { useUnitsStore } from "./units";

const recipesApi = mande(API_URL + "/recipes");
const currentId = ref<number>();

const recipes = useLocalStorage<Recipe[]>("recipes", []);

export const useRecipeStore = defineStore("recipe", () => {
  const $q = useQuasar();

  const { api } = useChefApi();

  const tagsStore = useTagStore();
  const unitsStore = useUnitsStore();

  const loading = ref(false);

  const all = computed(() => recipes);
  const favorites = computed(() => recipes.value.filter((rec) => rec.favorite));

  const current = computed(() =>
    recipes.value.find((r) => r.id === currentId.value)
  );

  const bus = useEventBus<ChefNotification>("notifications");

  function replaceRecipe(newRecipe: Recipe) {
    recipes.value = recipes.value.filter((r) => r?.id !== newRecipe.id);
    recipes.value.push(newRecipe);
    recipes.value.sort((a: Recipe, b: Recipe) => (a.title > b.title ? 1 : -1));
  }

  function removeRecipe(id: number) {
    recipes.value = recipes.value.filter((rec) => rec.id !== id);
  }

  async function fetch(force: boolean = false) {
    loading.value = true;
    let result = [];
    if (recipes.value.length > 0 && !force) {
      const latestUpdate = recipes.value
        .sort(
          (a, b) =>
            new Date(a.updated_at).getTime() - new Date(b.updated_at).getTime()
        )
        .reduce((a, b) => b);
      console.info(
        `LATEST: ${latestUpdate.title} @ ${latestUpdate.updated_at}`
      );
      result = await api.recipes.get({ since: latestUpdate.updated_at });
    } else {
      result = await api.recipes.get();
    }

    for (const recipe of result) {
      replaceRecipe(recipe);
    }

    recipes.value = recipes.value.sort((a: Recipe, b: Recipe) =>
      a.title > b.title ? 1 : -1
    );
    setTimeout(() => {
      loading.value = false;
    }, 300);
  }

  async function fetchSingle(recipeId: number): Promise<Recipe | undefined> {
    loading.value = true;
    try {
      const newRecipe = await api.recipes.getOne(recipeId);
      recipes.value.filter((r) => r.id !== newRecipe.id);
      recipes.value.push(newRecipe);
      loading.value = false;
      return newRecipe;
    } finally {
      loading.value = false;
    }
  }

  async function create(recipeData: CreateRecipe): Promise<Recipe> {
    loading.value = true;

    if (recipeData.ingredients) {
      for (let index = 0; index < recipeData.ingredients.length; index++) {
        recipeData.ingredients[index].order = index;
      }
    }

    let recipe: Recipe;
    try {
      recipe = await recipesApi.post<Recipe>(recipeData);
    } catch (e: unknown) {
      catchError(e, $q);
      throw e;
    } finally {
      loading.value = false;
    }

    recipes.value.push(recipe);
    recipes.value.sort((a: Recipe, b: Recipe) => (a.title > b.title ? 1 : -1));

    // Let's update other stores in case new items were added.
    tagsStore.fetch();
    unitsStore.fetch();
    return recipe;
  }

  async function update(recipeData: Recipe): Promise<Recipe | undefined> {
    loading.value = true;
    const data = JSON.parse(JSON.stringify(recipeData));

    if (data.ingredients) {
      for (let index = 0; index < data.ingredients.length; index++) {
        data.ingredients[index].order = index;
      }
    }

    let result;
    try {
      result = await recipesApi.put<Recipe>(data.id, data);
      replaceRecipe(result);
    } catch (e: unknown) {
      catchError(e, $q);
      throw e;
    } finally {
      loading.value = false;
    }
    // Let's update other stores in case new items were added.
    tagsStore.fetch();
    unitsStore.fetch();
    return result;
  }

  async function deleteById(recipeId: number) {
    loading.value = true;
    try {
      await recipesApi.delete(recipeId);
      removeRecipe(recipeId);
    } finally {
      loading.value = false;
    }

    // Let's update other stores in case new items were removed.
    tagsStore.fetch();
    unitsStore.fetch();
  }

  return {
    recipes,
    all,
    favorites,
    loading,
    current,
    currentId,
    fetch,
    fetchSingle,
    create,
    update,
    deleteById,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useRecipeStore, import.meta.hot));
}
