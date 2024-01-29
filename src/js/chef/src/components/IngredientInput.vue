<template>
<div class="ingredient-input">

    <ui-button @click="$emit('down')" icon="fas fa-chevron-down" type="secondary" />

    <ui-button @click="$emit('up')" icon="fas fa-chevron-up" type="secondary" />

    <ui-input class="amount" v-model="model.amount" size="small" label="amount" />

    <ui-input class="unit" v-model="model.unit.name" label="unit" size="small" />

    <ui-input class="ingredient" v-model="model.ingredient.name" label="ingredient" size="small" :success="ingredientExists" />

    <ui-input v-model="model.note" label="note" size="small" />

    <ui-button @click="$emit('delete')" icon="fas fa-trash" />
</div>
</template>
<script setup lang="ts">
import UiInput from '@/components/ui/UiInput.vue';
import UiButton from '@/components/ui/UiButton.vue';
import { useIngredientStore } from '@/stores/ingredient';
import type { IngredientItem } from '@/types';
import { ref, watch } from 'vue';

const model = defineModel<IngredientItem>({ required: true })

const emit = defineEmits([
    'update:ingredient',
    'delete',
    'up',
    'down'
])

const ingredients = useIngredientStore();

const ingredientExists = ref(false)

watch(model.value.ingredient, (old, n3w) => {
    n3w.name = n3w.name.toLocaleLowerCase()
    const match = ingredients.all.find((ing) => n3w.name === ing.name)
    if (match) {
        model.value.ingredient.id = match.id
        ingredientExists.value = true;
    } else {
        model.value.ingredient.id = undefined;
        ingredientExists.value = false;
    }
})
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