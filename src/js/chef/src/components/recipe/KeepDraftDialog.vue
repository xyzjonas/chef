<template>
  <q-dialog v-model="model" auto-close>
    <q-card class="w-sm p-3">
      <q-card-section class="row items-center">
        <span class="text-lg opacity-[0.8]"
          >Do you want to resume editing your previous draft?</span
        >
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
        <q-btn
          flat
          label="Discard"
          icon="delete"
          @click="$emit('discard')"
        />
        <q-btn
          flat
          label="continue editing"
          color="primary"
          @click="model = !model"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
const model = defineModel<boolean>();

defineEmits<{
  discard: [];
}>();
</script>

<style lang="scss" scoped></style>
