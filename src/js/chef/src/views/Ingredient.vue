<template>
  <div>
    <div v-if="ingredient">
      <h1 class="title-sm">{{ ingredient.name }}</h1>
      <h3 class="mt-0 text-[1rem] line-height-[1rem] opacity-[0.9] uppercase">
        Nutritional Values
      </h3>
      <div class="flex flex-row items-center justify-end mt-5 gap-1 mb-3">
        <q-btn
          unelevated
          color="primary"
          :label="edit ? 'cancel' : 'edit ingredient'"
          @click="edit = !edit"
        ></q-btn>
        <q-btn
          unelevated
          color="secondary"
          flat
          icon="delete"
          label="delete"
          @click="deleteIngredient()"
        ></q-btn>
      </div>

      <div v-if="!edit" class="flex gap-1 flex-wrap wrapper">
        <q-card
          class="my-card"
          v-for="(value, key) in attributes"
          :key="key"
          flat
          bordered
        >
          <q-card-section
            class="grid justify-center text-center items-center h-full"
          >
            <span class="uppercase text-xl font-500">{{ key }}</span>
            <span>{{ value }}</span>
          </q-card-section>
        </q-card>
      </div>

      <div v-if="edit">
        <IngredientForm
          :ingredientProp="ingredient"
          @cancel="edit = false"
          @posted="edit = false"
        />
      </div>
    </div>
    <div v-else>
      <NotFound />
    </div>
  </div>
</template>

<script setup lang="ts">
import IngredientForm from "@/components/IngredientForm.vue";
import NotFound from "@/components/NotFound.vue";
import { useIngredientStore } from "@/stores/ingredient";
import type { IngredientFull } from "@/types";
import { storeToRefs } from "pinia";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const ingredientId = parseInt(router.currentRoute.value.params.id as string);

const ingredients = useIngredientStore();
const { current, currentId } = storeToRefs(ingredients);

currentId.value = ingredientId;

if (!current.value) {
  try {
    await ingredients.fetchSingle(ingredientId);
  } catch {}
}

if (!current.value) {
  router.push({
    name: "notfound",
    query: { path: router.currentRoute.value.fullPath },
  });
}

const ingredient = computed<IngredientFull>(
  () => current.value as IngredientFull
);

const edit = ref(false);
const attributes = computed(() => ({
  energy: `${current.value?.energy} kcal`,
  carbs: `${current.value?.carbs} g`,
  fats: `${current.value?.fats} g`,
  proteins: `${current.value?.proteins} g`,
  fibres: `${current.value?.fibres} g`,
  salt: `${current.value?.salt} g`,
}));

const emit = defineEmits(["ingredientDeleted"]);
const deleteIngredient = async () => {
  await ingredients.deleteById(ingredientId);
  router.push({ name: "ingredients" });
};
</script>

<style lang="css" scoped>
.my-card {
  flex: 1;
  min-width: 10rem;
  height: 10rem;
}

@media (min-width: 768px) {
  .my-card {
    min-width: 15rem;
  }
}
</style>
