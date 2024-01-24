<template>
<div class="ingredient-input">
    <ui-button @click="$emit('down')" icon="fas fa-chevron-down" type="secondary" />

    <ui-button @click="$emit('up')" icon="fas fa-chevron-up" type="secondary" />

    <ui-input class="amount" v-model="ingredientItem.amount" size="small" label="amount" />

    <ui-input class="unit" v-model="selectedUnitName" label="unit" size="small" />

    <ui-input class="ingredient" v-model="selectedIngredientName" label="ingredient" size="small" />

    <ui-input v-model="ingredientItem.note" label="note" size="small" />

    <ui-button @click="$emit('delete')" icon="fas fa-trash" />
</div>
</template>
<script setup lang="ts">
import UiInput from '@/components/ui/UiInput.vue';
import UiButton from '@/components/ui/UiButton.vue';
import { useIngredientStore } from '@/stores/ingredient';
import { useUnitsStore } from '@/stores/units';
import type { IngredientItem } from '@/types';
import { ref } from 'vue';

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
    flex-direction: row;
    gap: .3rem;
    
}

.amount {
    flex-basis: 4rem;
}

.unit {
    flex-basis: 2rem;
}

.ingredient {
    flex-grow: 2;
}
</style>