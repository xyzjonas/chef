<template>
  <main>
    <q-table
      flat
      
      :title="`${ingredients.length} INGREDIENT${ingredients.length === 1 ? '' : 's'}`"
      :rows="ingredients"
      :columns="columns"
      row-key="id"
      :filter="search"
      hide-pagination
      :rows-per-page-options="[0]"
      @row-click="(_, row: IngredientFull) => $router.push({ name: 'ingredient', params: { id: row.id } })"
      no-data-label="No ingredients added yet"
    >
      <template v-slot:body-cell-name="props: { row: IngredientFull }" >
        <q-td :props="props">
          <span class="text-lg capitalize font-400">
            {{props.row.name }}
          </span>
        </q-td>
      </template>
      <template v-slot:top>
        <h1>{{ `${ingredients.length} INGREDIENT${ingredients.length === 1 ? '' : 's'}` }}</h1>
        <q-input outlined dense v-model="search" placeholder="Search" class="ml-auto">
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

    </q-table>
  </main>
</template>

<script setup lang="ts">
import { useIngredientStore } from "@/stores/ingredient";
import { computed, ref } from "vue";
import { replaceUnicode } from "@/utils";
import type { Ingredient, IngredientFull } from "@/types";
import { storeToRefs } from "pinia";

const ingredientsStore = useIngredientStore();
const { all } = storeToRefs(ingredientsStore)

const search = ref<string>();

const ingredients = computed(() => {
  if (!search.value || search.value === ""){
    return all.value;
  }
  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return all.value.filter(ing => {
    const match = re.exec(replaceUnicode(ing.name.toLowerCase()))
    if (match) {
      return true;
    }
    return false;
  })
})

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Ingredient',
    align: 'left',
    field: (row: any) => row.name,
    format: (val: string) => `${val}`,
    sortable: true
  },
  {
    name: 'energy',
    required: true,
    label: 'Energy',
    align: 'left',
    field: (row: any) => row.energy,
    format: (val: string) => `${val} kcal`,
    sortable: true
  },
  {
    name: 'fat',
    required: true,
    label: 'Fats',
    align: 'left',
    field: (row: IngredientFull) => row.fats,
    format: (val: string) => `${val} g`,
    sortable: true
  },
  {
    name: 'proteins',
    required: true,
    label: 'Proteins',
    align: 'left',
    field: (row: IngredientFull) => row.proteins,
    format: (val: string) => `${val} g`,
    sortable: true
  },
  {
    name: 'carbs',
    required: true,
    label: 'Carbs',
    align: 'left',
    field: (row: IngredientFull) => row.carbs,
    format: (val: string) => `${val} g`,
    sortable: true
  },
]


</script>

<style>

</style>