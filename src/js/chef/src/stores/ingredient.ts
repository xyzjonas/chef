// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from "pinia";
import { computed, ref } from "vue";

import { API_URL } from "@/constants";

import type {
  Ingredient,
  ChefNotification,
  ServerErrorResponse,
  IngredientFull,
} from "@/types";
import { mande } from "mande";

import { useEventBus } from "@vueuse/core";

const api = mande(API_URL + "/ingredients");
const currentId = ref<number>()

export const useIngredientStore = defineStore("ingredient", () => {
  const loading = ref<boolean>(false);

  const all = ref<IngredientFull[]>([]);

  const current = computed(() => all.value.find(i => i.id === currentId.value))

  const bus = useEventBus<ChefNotification>("notifications");

  async function fetch() {
    loading.value = true;
    api
      .get<IngredientFull[]>()
      .then(
        (ingredients: IngredientFull[]) =>
          (all.value = ingredients.sort((a: Ingredient, b: Ingredient) =>
            a.name > b.name ? 1 : -1
          ))
      )
      .catch((err: unknown) => console.error(err))
      .finally(() => (loading.value = false));
  }

  async function fetchSingle(ingredientId: number) {
    loading.value = true;
    try {
      const response = await api.get<IngredientFull>(ingredientId)
      if (all.value.find(i => i.id === ingredientId)) {
        all.value = all.value.map((r) => (r.id === response.id ? response : r))
      } else {
        all.value.push(response)
      }
    } finally {
      loading.value = false;
    }
  }

  async function update(ingredientData: Ingredient): Promise<Ingredient> {
    loading.value = true;
    try {
      const result = await api.put<IngredientFull>(
        ingredientData.id,
        ingredientData
      );
      all.value = all.value.map((ing) => ing.id === ingredientData.id ? result : ing);
    } catch (err) {
      console.error(err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteById(ingredientId: number) {
    loading.value = true;
    console.debug(`Deleting ingredient id=${ingredientId}.`);
    try {
      const result = await api.delete(ingredientId);
      all.value = all.value.filter((ing) => ing.id !== ingredientId);
    } catch (e: unknown) {
      const err = e as ServerErrorResponse;
      bus.emit({
        level: "ERROR",
        message: err.body?.detail ?? err.message,
      });
    }
    loading.value = false;
  }

  return { all, loading, current, currentId, fetch, update, fetchSingle, deleteById };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useIngredientStore, import.meta.hot));
}
