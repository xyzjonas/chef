<template>
  <ui-card>
    <div class="flex h-full">
      <li class="flex-1">
        <ul v-for="item in ingredients">
          <span class="text-xl mr-2">
            {{ Math.ceil((item.amount / basePortions ?? 1) * 10 * modelValue) / 10 }}
          </span>
          {{
            item.unit.name
          }}
          <span class="text-lg font-semibold ml-2 mr-1">
            {{ item.ingredient.name }}
          </span>
          {{
            item.note
          }}
        </ul>
      </li>
      <ui-portions-counter v-model="modelValue" />
    </div>
  </ui-card>
</template>

<script setup lang="ts">
import type { IngredientItem } from "@/types/recipe";

interface Props {
  ingredients: IngredientItem[];
}

const props = defineProps<Props>();

const modelValue = defineModel({ type: Number, required: true });


let basePortions = modelValue.value;
</script>

<style lang="css" scoped>
li {
  padding: 0;
  margin: 0;
  list-style: none;
}

ul {
  display: flex;
  align-items: center;
}

ul::before {
  content: "";
  display: inline-block;
  width: 0.3rem;
  aspect-ratio: 1;
  background-color: var(--text-100);
  margin-right: 0.5rem;
  border-radius: 50%;
}

.ingredients {
  border-left: 3px solid var(--primary-100);
  padding-inline: 1rem;
  padding-block: 1rem;
  flex: 1;
}
</style>
