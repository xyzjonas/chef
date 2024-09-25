<template>
  <div v-if="ingredient" class="flex flex-col gap-2">

    <q-input outlined v-model="ingredient.name" label="Name"/>
  
    <q-input outlined v-model="ingredient.energy" label="Energy" type="number"/>
  
    <q-input outlined v-model="ingredient.carbs" label="Carbs" type="number"/>
  
    <q-input outlined v-model="ingredient.fats" label="Fats" type="number"/>
  
    <q-input outlined v-model="ingredient.proteins" label="Proteins" type="number"/>
   
    <q-input outlined v-model="ingredient.fibres" label="Fibres" type="number"/>

    <q-input outlined v-model="ingredient.salt" label="Salt" type="number"/>

    <div class="flex flex-row items-center gap-1">
      <q-btn color="primary" unelevated @click="save" label="save" icon="save" class="flex-1"></q-btn>
      <q-btn color="secondary" flat @click="cancel" label="cancel" class="flex-1"></q-btn>
    </div>

  </div>
</template>

<script setup lang="ts">
import { useIngredientStore } from '@/stores/ingredient';
import type { Ingredient, IngredientFull } from '@/types';
import { deepCopy } from '@/utils';
import { ref } from 'vue';

const ingredients = useIngredientStore();

const props = defineProps<{
  ingredientProp: IngredientFull | undefined;
}>();

const ingredient = ref<IngredientFull>();
if (props.ingredientProp) {
  ingredient.value = deepCopy(props.ingredientProp);
}
    
const emit = defineEmits(["cancel", "posted"]);
const cancel = () => emit("cancel");
const save = () => {
  ingredients.update(ingredient.value as Ingredient).then(() => emit("posted", ingredient));
}
</script>

<style>

</style>