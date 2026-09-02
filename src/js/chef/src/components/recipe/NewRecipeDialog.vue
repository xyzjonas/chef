<template>
  <q-dialog v-model="isOpened" @hide="onHide" position="bottom">
    <q-card class="w-[24rem] px-1 py-3">
      <q-form @submit="doCreate">
        <q-card-section>
          <h3 class="my-0 mb-1">Create a new recipe</h3>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            autofocus
            v-model="title"
            label="Title"
            autocomplete="off"
            :rules="[(val: string) => !!val || 'Title is required']"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" @click="close" />
          <q-btn
            unelevated
            label="Create"
            color="primary"
            type="submit"
            :loading="loading"
          />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useNewRecipeDialog } from "@/composables/newRecipeDialog";
import { useRecipeStore } from "@/stores/recipe";
import { ref } from "vue";
import { useRouter } from "vue-router";

const { isOpened, close } = useNewRecipeDialog();
const recipeStore = useRecipeStore();
const router = useRouter();

const title = ref("");
const loading = ref(false);
const createdRecipeId = ref<number | null>(null);

const MIN_LOADING_MS = 400;
const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const doCreate = async () => {
  loading.value = true;
  const start = Date.now();
  try {
    const recipe = await recipeStore.create(title.value);
    const remaining = MIN_LOADING_MS - (Date.now() - start);
    if (remaining > 0) {
      await wait(remaining);
    }
    createdRecipeId.value = recipe.id;
    close();
  } finally {
    loading.value = false;
  }
};

const onHide = () => {
  title.value = "";
  if (createdRecipeId.value !== null) {
    router.push({ name: "editrecipe", params: { id: createdRecipeId.value } });
    createdRecipeId.value = null;
  }
};
</script>
