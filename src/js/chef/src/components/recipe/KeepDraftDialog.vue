<template>
  <q-dialog v-model="model" seamless auto-close position="bottom">
    <q-card class="w-[30rem] p-3">
      <q-card-section class="row items-center">
        <span class="text-lg text-gray-7"
          >Continue working on your previous edit?</span
        >
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          flat
          label="Discard"
          color="secondary"
          @click="$emit('discard')"
        />
        <q-btn
          flat
          label="Yes, I ain't done yet"
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
