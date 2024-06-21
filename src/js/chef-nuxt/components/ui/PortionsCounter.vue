<template>
  <div class="flex flex-col gap-1 counter justify-between items-center">
    <ui-button @click="increment" outlined rounded icon="i-hugeicons-add-01" />
    <div class="flex items-center">
      <span class="label">{{ modelValue }}</span>
      <i class="icon i-hugeicons-rice-bowl-01 translate-y-[-2px] ml-1"></i>
    </div>
    <ui-button @click="decrement" outlined rounded icon="i-hugeicons-remove-01"/>
  </div>
</template>

<script setup lang="ts">
const modelValue = defineModel<number>();

const MAX = 60;

const increment = () => {
  if (modelValue.value && modelValue.value < MAX) {
    modelValue.value += 1;
  }
};

const decrement = () => {
  if (modelValue.value && modelValue.value > 1) {
    modelValue.value -= 1;
  }
};
</script>

<style lang="css" scoped>

.counter {
  min-height: 12rem;
}

.line {
  position: absolute;
  border-right: 3px solid red;
  min-width: 3px;
}
</style>
