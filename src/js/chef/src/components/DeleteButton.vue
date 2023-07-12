<template>
  <div style="flex-grow: 2;">

    <button 
      v-if="!modelValue"
      @click="$emit('update:modelValue', !modelValue)"
      :class="{
        button: true,
        'is-danger': true,
        'is-small': small,
        'is-rounded': rounded,
        'clickable-link': true
      }">
      <i class="fas fa-trash"></i>
    </button>
    <div v-else style="display: flex;">
      <button
        @click="$emit('update:modelValue', !modelValue)"
        :class="{
          button: true,
          'is-small': small,
          'is-rounded': rounded,
          'is-fullwidth': true,
          'clickable-link': true
        }">
        <span class="icon is-small">
          <i class="fas fa-times"></i>
        </span>
      </button>
      <button
        @click="$emit('delete')"
        :class="{
          button: true,
          'is-danger': true,
          'is-small': small,
          'is-rounded': rounded,
          'is-fullwidth': true,
          'clickable-link': true,
          'is-loading': loading,
          'ml-1': true,
        }">
        <span class="icon is-small">
          <i class="fas fa-trash"></i>
        </span>
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  small: boolean,
  rounded: boolean,
  loading: boolean,
  modelValue: boolean
}>()
defineEmits(["update:modelValue"])
</script>

<style>

</style>