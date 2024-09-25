<template>
  <q-dialog v-model="model" seamless auto-close position="bottom">
    <q-card class="w-[30rem] p-3">
      <q-card-section class="row items-center">
        <span class="ml-3 text-lg">Do you really want to delete this recipe?</span
        >
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="secondary" @click="model = !model" />
        <q-btn
          flat
          label="Delete"
          color="primary"
          @click="doDelete"
          :loading="loading"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useRecipeStore } from "@/stores/recipe";
import type { Recipe } from "@/types";
import { ref } from "vue";
import { useRouter } from "vue-router";

const recipes = useRecipeStore();
const props = defineProps<{ recipe: Recipe }>();

const model = defineModel<boolean>();
const loading = ref(false);

const router = useRouter()

const doDelete = () => {
  loading.value = true;
  
  recipes
    .deleteById(props.recipe.id)
    .then(() => router.push({ name: 'recipes' }))
    .finally(() => {
        loading.value = false;
        model.value = false;
    });
};
</script>

<style lang="scss" scoped></style>
