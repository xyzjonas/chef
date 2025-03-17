<template>
  <q-input
    v-model="model"
    :dense="isDense"
    filled
    :disable="disabled"
    type="text"
    :label="label"
    :rules="rules"
    :placeholder="placeholder"
  >
    <template v-if="iconBefore" v-slot:prepend>
      <q-icon :name="iconBefore" />
    </template>
    <template v-if="iconAfter" v-slot:append>
      <q-icon :name="iconAfter" />
    </template>
    <template v-else-if="clearable && model.length > 0" v-slot:append>
      <q-icon name="close" @click="model = ''" class="cursor-pointer" />
    </template>
  </q-input>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue";

const model = defineModel<string>({ required: true });
const props = defineProps<{
  iconBefore?: string;
  iconAfter?: string;
  size?: any;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  centered?: boolean;
  success?: boolean;
  dense?: boolean;
  rules?: any[];
  clearable?: boolean;
}>();

const isDense = computed(() =>
  props.dense === undefined ? true : props.dense
);
</script>
