<template>
  <div class="level">
    <ui-button @click="decrement" icon="fas fa-minus" type="secondary" />
    <ui-input v-model="model" disabled size="small" centered label="portions counter" />
    <ui-button @click="increment" icon="fas fa-plus" type="secondary" />
    </div>
</template>

<script setup lang="ts">
import UiButton from './ui/UiButton.vue';
import UiInput from './ui/UiInput.vue';
const model = defineModel<number>();
// const props = defineProps<{ modelValue: number }>();
// const emit = defineEmits(["update:modelValue"]);


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
.level {
  display: flex;
  flex-direction: row;
  gap: .3rem
}
</style>