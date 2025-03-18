<template>
  <q-list bordered class="rounded-borders">
    <q-expansion-item
      expand-separator
      icon="restaurant_menu"
      label="INGREDIENTS"
      :caption="title"
      :disable="recipe.ingredients.length <= 0"
      v-model="expanded"
    >
      <q-card>
        <q-card-section>
          <table class="w-full">
            <tr style="background-color: transparent">
              <th class="w-[8rem]"></th>
              <th></th>
            </tr>
            <tbody class="ing-body">
              <Component
                v-for="ingredient in recipe.ingredients"
                :is="
                  ingredient.ingredient.name.endsWith('--')
                    ? RecipeIngredientTableSeparator
                    : RecipeIngredientTableRow
                "
                :ingredient="ingredient"
                :portions="portions"
                :base-portions="recipe.portions"
                :key="ingredient.ingredient.id"
              />
            </tbody>
          </table>
        </q-card-section>
        <q-separator />
        <q-card-section class="flex items-center justify-center">
          <Counter v-model="portions"></Counter>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";
import { computed, onMounted, ref } from "vue";

import Counter from "@/components/Counter.vue";
import RecipeIngredientTableRow from "./RecipeIngredientTableRow.vue";
import RecipeIngredientTableSeparator from "./RecipeIngredientTableSeparator.vue";

const props = defineProps<{
  recipe: Recipe;
}>();

const portions = ref(props.recipe.portions);

const title = computed(() => {
  if (props.recipe.ingredients.length === 0) {
    return "No ingredients written down";
  } else {
    return `${props.recipe.ingredients.length} ingredient${
      props.recipe.ingredients.length === 1 ? "" : "s"
    } is all that you need`;
  }
});

const expanded = ref(false);
onMounted(() => {
  if (props.recipe.ingredients.length > 0) {
    expanded.value = true;
  }
});
</script>

<style lang="css" scoped>
.body--light tr:nth-of-type(odd) {
  background-color: rgba(233, 233, 233, 0.4);
}

.body--dark tr:nth-of-type(odd) {
  background-color: rgba(43, 43, 43, 0.3);
}
</style>
