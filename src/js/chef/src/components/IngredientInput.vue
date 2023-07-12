<template>
<div class="ingredient-input">
    <button class="button is-small arrow" @click="$emit('down')">
        <i class="fas fa-chevron-down" aria-hidden="true"></i>
    </button>
    <button class="button is-small arrow" @click="$emit('up')">
        <i class="fas fa-chevron-up" aria-hidden="true"></i>
    </button>
    <input
        v-model="ingredientItem.amount"
        id="amount"
        type="number"
        :class="{
            input: true,
            'is-small': true,
            'is-success': ingredientItem.amount,
            'is-danger': !ingredientItem.amount
        }"
    >
    <input
        list="units"
        v-model="selectedUnitName"
        id="unit"
        :class="{
            input: true,
            'is-small': true,
            'is-warning': !selectedUnitOk,
            'is-success': selectedUnitOk,
            'is-danger': !selectedUnitName
        }"
        placeholder="g"
        type="text"
        autocomplete="off"
        @input="event => selectUnit()"
    >
    <datalist id="units">
        <option v-for="unit in units.all" :value="unit.name">{{ unit.name }}</option>
    </datalist>

    <input
        list="ingredients"
        v-model="selectedIngredientName"
        id="name"
        :class="{
            input: true,
            'is-small': true,
            'is-warning': !selectedIngredientOk,
            'is-success': selectedIngredientOk,
            'is-danger': !selectedIngredientName,
        }"
        placeholder="ingredient"
        type="text"
        autocomplete="off"
        @input="event => selectIngredient()"
    >
    <datalist id="ingredients">
        <option v-for="ingredient in ingredients.all" :value="ingredient.name">{{ ingredient.name }}</option>
    </datalist>
    <input v-model="ingredientItem.note" id="note" class="input is-small" placeholder="note">
    <button class="button is-small is-danger is-outlined" @click="$emit('delete')">
        <i class="fas fa-trash"></i>
    </button>
</div>
</template>
<script setup lang="ts">
import { useIngredientStore } from '@/stores/ingredient';
import { useUnitsStore } from '@/stores/units';
import type { Ingredient, IngredientItem } from '@/types';
import { ref, watch } from 'vue';

const props = defineProps<{'initialData': IngredientItem}>()


const ingredientItem = ref<IngredientItem>(
    JSON.parse(JSON.stringify(props.initialData))
)
const emit = defineEmits([
    'update:ingredient',
    'delete',
    'up',
    'down'
])
const emitUpdate = () => {
    emit('update:ingredient', ingredientItem.value);
}

const ingredients = useIngredientStore();
const selectedIngredientName = ref<string>(ingredientItem.value.ingredient.name);
const selectedIngredientOk = ref();
const selectIngredient = () => {
    const match = ingredients.all.find(ing => ing.name === selectedIngredientName.value)
    if( match ) {
        selectedIngredientOk.value = true;
        ingredientItem.value.ingredient = match;
    } else {
        selectedIngredientOk.value = false;
        ingredientItem.value.ingredient = { name: selectedIngredientName.value };
    }
    emitUpdate();
}
selectIngredient();

const units = useUnitsStore();
const selectedUnitName = ref<string>(ingredientItem.value.unit.name);
const selectedUnitOk = ref();
const selectUnit = () => {
    const match = units.all.find(u => u.name === selectedUnitName.value)
    if( match ) {
        selectedUnitOk.value = true;
        ingredientItem.value.unit = match;
    } else {
        selectedUnitOk.value = false;
        ingredientItem.value.unit = { name: selectedUnitName.value };
    }
    emitUpdate();
}
selectUnit();



// const ingredientItem = ref<IngredientItem>()
</script>
<style lang="scss" scoped>
select {
    border-radius: 2px;
}
.arrow {
    width: 0.5em;
}
.ingredient-input {
    display: flex;
    gap: 1px;

    #amount {
        max-width: 5em;
    }
    #unit {
        max-width: 4em;
    }
    #note {
        width: 5em;
        transition: width 0.1s ease-in;
        &:focus {
            width: 100%;
            transition: width 0.1s ease-in;
        }
    }
    
}
</style>