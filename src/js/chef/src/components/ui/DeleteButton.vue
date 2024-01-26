<template>
  <div style="flex-grow: 2;">

    <ui-button 
      v-if="!model"
      type="secondary"
      icon="fas fa-trash"
      @click="model = !model"
    />
    <div v-else class="level">
      <ui-button
        @click="model = !model"
        icon="fas fa-times"
      />
      <ui-button
        icon="fas fa-trash"
        @click="$emit('delete')"
      />
    </div>

  </div>
</template>

<script setup lang="ts">
import UiButton from '@/components/ui/UiButton.vue';
const model = defineModel<boolean>();
defineProps<{
  small?: boolean,
  rounded?: boolean,
  loading: boolean,
  // modelValue: boolean
}>()
defineEmits(["delete"])
</script>

<style lang="css" scoped>
.level {
  display: flex;
  flex-direction: row;
  gap: .3rem;
}
</style>