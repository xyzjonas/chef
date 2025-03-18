<template>
  <q-page padding>
    <q-table
      flat
      :rows="ingredients"
      :columns="columns"
      row-key="id"
      :filter="search"
      hide-pagination
      title-class="title-sm"
      :rows-per-page-options="[0]"
      @row-click="(_, row: IngredientFull) => $router.push({ name: 'ingredient', params: { id: row.id } })"
      no-data-label="No ingredients added yet"
    >
      <template v-slot:body-cell-name="props: { row: IngredientFull }">
        <q-td :props="props">
          <span class="text-lg capitalize font-400">
            {{ props.row.name }}
          </span>
        </q-td>
      </template>
      <template v-slot:top>
        <h1 class="title-sm">
          {{ title }}
        </h1>
        <q-input
          outlined
          dense
          v-model="search"
          placeholder="Search"
          class="ml-auto mt-5"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
    </q-table>
  </q-page>
</template>

<script setup lang="ts">
import { useIngredientStore } from "@/stores/ingredient";
import type { IngredientFull } from "@/types";
import { replaceUnicode } from "@/utils";
import { storeToRefs } from "pinia";
import { computed, ref } from "vue";

const ingredientsStore = useIngredientStore();
const { all } = storeToRefs(ingredientsStore);

const search = ref<string>();

const ingredients = computed(() => {
  if (!search.value || search.value === "") {
    return all.value;
  }
  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return all.value.filter((ing) => {
    const match = re.exec(replaceUnicode(ing.name.toLowerCase()));
    if (match) {
      return true;
    }
    return false;
  });
});

const title = computed(() =>
  ingredients.value.length > 1 ? "ingredients" : "ingredient"
);

const columns = [
  {
    name: "name",
    required: true,
    label: "Ingredient",
    align: "left",
    field: (row: any) => row.name,
    format: (val: string) => `${val}`,
    sortable: true,
  },
  {
    name: "energy",
    required: true,
    label: "Energy",
    align: "left",
    field: (row: any) => row.energy,
    format: (val: string) => `${val} kcal`,
    sortable: true,
  },
  {
    name: "fat",
    required: true,
    label: "Fats",
    align: "left",
    field: (row: IngredientFull) => row.fats,
    format: (val: string) => `${val} g`,
    sortable: true,
  },
  {
    name: "proteins",
    required: true,
    label: "Proteins",
    align: "left",
    field: (row: IngredientFull) => row.proteins,
    format: (val: string) => `${val} g`,
    sortable: true,
  },
  {
    name: "carbs",
    required: true,
    label: "Carbs",
    align: "left",
    field: (row: IngredientFull) => row.carbs,
    format: (val: string) => `${val} g`,
    sortable: true,
  },
];
</script>
