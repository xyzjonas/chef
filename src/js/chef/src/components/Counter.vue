<template>
  <div class="flex items-center gap-5 p-1">
    <ui-button dense flat @click="decrement" icon="remove" color="secondary" />
    <span class="flex items-center gap-3">
      <span class="font-bold text-lg">{{ model }}</span>SERVINGS
    </span>
    <!-- <ui-input v-model="model" disabled size="small" centered label="portions" /> -->
    <ui-button dense flat @click="increment" icon="add" color="secondary" />
  </div>
</template>

<script setup lang="ts">
import UiButton from './ui/UiButton.vue';
import UiInput from './ui/UiInput.vue';
const model = defineModel<number>();

const increment = () => {
  model.value = !!model.value ? model.value + 1 : 1
}

const decrement = () => {
  model.value = !!model.value ? model.value - 1 : 0
  if (model.value <= 1) {
    model.value = 1;
  }
}

</script>

<style lang="css" scoped>
</style>