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
            <table>
              <tbody>
                <tr
                  v-for="(ingredient, index) in recipe.ingredients"
                  :key="ingredient.ingredient.id"
                  :class="
                    ingredient.ingredient.name.endsWith('--') ? 'hide' : ''
                  "
                >
                  <td class="amount">
                    <h1 class="m-0 line-height-snug">
                      {{
                        Math.round(
                          ((ingredient.amount * portions) / recipe.portions) *
                            10
                        ) / 10
                      }}
                    </h1>
                    <small>{{
                      ingredient.unit.name.replace("pcs", "ks")
                    }}</small>
                  </td>
                  <td class="ingredient-link">
                    <router-link
                      :to="{
                        name: 'ingredient',
                        params: { id: ingredient.ingredient.id },
                      }"
                    >
                      {{ ingredient.ingredient.name }}
                      <span v-if="ingredient.note"
                        >({{ ingredient.note }})</span
                      >
                    </router-link>
                  </td>
                </tr>
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
import type { Recipe } from '@/types';
import { computed, onMounted, ref } from 'vue';

import Counter from '@/components/Counter.vue';

const props = defineProps<{
    recipe: Recipe
}>()

const portions = ref(props.recipe.portions)

const title = computed(() => {
  if (props.recipe.ingredients.length === 0) {
    return "No ingredients written down"
  } else {
    return `${props.recipe.ingredients.length} ingredient${
          props.recipe.ingredients.length === 1 ? '' : 's'
        } is all that you need`
  }
})

const expanded = ref(false)
onMounted(() => {
  if (props.recipe.ingredients.length > 0) {
    expanded.value = true
  }
})

</script>

<style lang="scss" scoped>
td {
  padding-block: 0.4rem;
  min-width: 6rem;
}

tr {
  & > .amount {
    display: flex;
    align-items: center;
    text-align: right;
    gap: 0.3rem;
    // width: 5rem;
    // border-bottom: 1px solid gray;

    & > h1 {
      font-size: x-large;
      font-weight: 400;
    }
  }

  &:nth-child(even) > .amount {
    color: var(--primary);
  }

  &:nth-child(odd) > .amount {
    color: var(--text);
  }

  &:nth-child(even) > td > a {
    color: var(--primary);
    text-decoration: none;
  }

  &:nth-child(odd) > td > a {
    color: var(--text);
    text-decoration: none;
  }
}
</style>