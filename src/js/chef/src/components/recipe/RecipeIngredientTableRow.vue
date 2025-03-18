<template>
  <tr :class="isSeparator ? 'text-transparent' : ''">
    <td class="flex items-baseline gap-1 px-2 py-1">
      <h1 class="m-0 line-height-snug text-2xl">{{ amount }}</h1>
      <small>{{ ingredient.unit.name.replace("pcs", "ks") }}</small>
    </td>
    <td class="ingredient-link px-2 py-1">
      <router-link
        v-if="!isSeparator"
        :to="{
          name: 'ingredient',
          params: { id: ingredient.ingredient.id },
        }"
      >
        {{ ingredient.ingredient.name }}
        <span v-if="ingredient.note">({{ ingredient.note }})</span>
      </router-link>
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { IngredientItem } from "@/types";
import { computed } from "vue";

const props = defineProps<{
  ingredient: IngredientItem;
  portions: number;
  basePortions: number;
}>();

const amount = computed(
  () =>
    Math.round(
      ((props.ingredient.amount * props.portions) / props.basePortions) * 10
    ) / 10
);

const isSeparator = computed(() =>
  props.ingredient.ingredient.name.endsWith("--")
);
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
  color: var(--primary);
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }
}
</style>
