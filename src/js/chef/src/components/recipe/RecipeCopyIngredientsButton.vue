<template>
  <q-btn
    dense
    flat
    round
    icon="sym_o_grocery"
    aria-label="Copy ingredients"
    :disable="recipe.ingredients.length <= 0"
    @click="copy"
    label="copy ingredients"
  />
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";
import { ingredientsToText } from "@/utils";
import { useQuasar } from "quasar";

const props = defineProps<{
  recipe: Recipe;
  portions: number;
}>();

const $q = useQuasar();

async function copy() {
  const text = ingredientsToText(
    props.recipe.ingredients,
    props.portions,
    props.recipe.portions,
  );

  try {
    await navigator.clipboard.writeText(text);
    $q.notify({ type: "positive", message: "Ingredients copied to clipboard" });
  } catch (err) {
    $q.notify({ type: "negative", message: "Could not copy ingredients" });
  }
}
</script>
