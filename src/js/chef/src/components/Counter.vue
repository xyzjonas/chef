<template>
  <div class="field has-addons">
      <p class="control">
        <a class="button is-small" @click="decrement">
          <span class="icon is-small">
            <i class="fas fa-minus"></i>
          </span>
        </a>
      </p>
      <p class="control is-expanded">
        <input
          class="input has-text-centered is-small"
          type="text"
          :value="modelValue"
          disabled
          @input="$emit('update:modelValue')"
        >
      </p>
      <p class="control">
        <a class="button is-small" v-on:click="increment">
          <span class="icon is-small">
            <i class="fas fa-plus"></i>
          </span>
        </a>
      </p>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{ modelValue: number }>();
const emit = defineEmits(["update:modelValue"]);


const increment = () => {
  emit('update:modelValue', props.modelValue + 1);
}

const decrement = () => {
  emit('update:modelValue', props.modelValue - 1);
}

</script>

<style>

</style>