// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from "pinia";
import { computed, ref } from "vue";

import { mande } from "mande";

import { API_URL } from "@/constants";

import type {
  CreateRecipe,
  ChefNotification,
  Recipe,
  ServerErrorResponse,
} from "@/types";
import { useTagStore } from "./tags";
import { useUnitsStore } from "./units";
import { useEventBus } from "@vueuse/core";

const recipesApi = mande(API_URL + "/recipes");

export const useRecipeStore = defineStore("recipe", () => {
  const tagsStore = useTagStore();
  const unitsStore = useUnitsStore();

  const loading = ref(false);

  const recipes = ref<Recipe[]>([]);

  const all = computed(() => recipes);
  const favorites = computed(() => recipes.value.filter((rec) => rec.favorite));

  const bus = useEventBus<ChefNotification>("notifications");

  async function fetch(force: boolean = true) {
    if (recipes.value.length > 0 && !force) {
      return;
    }

    loading.value = true;
    const result = await recipesApi.get<Recipe[]>("details");
    recipes.value = result.sort((a: Recipe, b: Recipe) =>
      a.title > b.title ? 1 : -1
    );
    setTimeout(() => {
      loading.value = false;
    }, 300);
  }

  async function fetchSingle(recipeId: number): Promise<Recipe | undefined> {
    loading.value = true;
    try {
      const newRecipe = await recipesApi.get<Recipe>(recipeId);
      recipes.value.filter(r => r.id !== newRecipe.id)
      recipes.value.push(newRecipe)
      loading.value = false;
      return newRecipe;

    } catch (err: unknown) {
      bus.emit({ level: "ERROR", message: `failed to fetch recipe #${recipeId}` });
      throw err

    } finally {
      loading.value = false;
    }
  }

  async function create(recipeData: CreateRecipe): Promise<Recipe> {
    loading.value = true;
    console.debug("Creating recipe.");

    let recipe: Recipe;
    try {
      recipe = await recipesApi.post<Recipe>(recipeData);
    } catch (e: unknown) {
      const err = e as ServerErrorResponse;
      bus.emit({
        level: "ERROR",
        message: err.body?.detail ?? err.message,
      });
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
    console.debug(`Updating recipe id=${recipeData.id}.`);

    let result;
    try {
      result = await recipesApi.put<Recipe>(recipeData.id, recipeData);
    } catch (e: unknown) {
      const err = e as ServerErrorResponse;
      bus.emit({
        level: "ERROR",
        message: err.body?.detail ?? err.message,
      });
      throw e;
    }
    recipes.value = recipes.value.filter((r) => r?.id !== recipeData.id);
    recipes.value.push(result);
    recipes.value.sort((a: Recipe, b: Recipe) => (a.title > b.title ? 1 : -1));
    loading.value = false;

    // Let's update other stores in case new items were added.
    tagsStore.fetch();
    unitsStore.fetch();
    return result;
  }

  async function deleteById(recipeId: number) {
    loading.value = true;
    console.debug(`Deleting recipe id=${recipeId}.`);
    try {
      await recipesApi.delete(recipeId);
      recipes.value = recipes.value.filter((rec) => rec.id !== recipeId);
    } catch (err) {
      console.error(err);
    }
    loading.value = false;

    // Let's update other stores in case new items were removed.
    tagsStore.fetch();
    unitsStore.fetch();
  }

  return {
    recipes,
    all,
    favorites,
    loading,
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
