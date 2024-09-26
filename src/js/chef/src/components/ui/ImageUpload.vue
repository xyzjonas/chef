<template>
  <div class="flex gap-1 justify-center items-center w-full">
    <!-- upload -->
    <q-btn
      v-if="file"
      color="primary"
      unelevated
      @click="upload"
      label="upload"
    />

    <!-- choose file -->
    <q-file
      v-else
      dense
      borderless
      v-model="file"
      :label="`New ${type ?? ''} Image`"
      class="capitalize"
      accept=".jpg,.jpeg,.png,.avif"
    >
    </q-file>

    <q-btn
      v-if="file"
      @click="file = undefined"
      flat
      color="secondary"
      icon="close"
    />
  </div>
</template>

<script setup lang="ts">
import { API_URL } from "@/constants";
import type { Category, ChefNotification, Recipe } from "@/types";
import { ref } from "vue";
import { useRoute } from "vue-router";

import { useRecipeStore } from "@/stores/recipe";
import { useEventBus } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { useQuasar } from "quasar";

const $q = useQuasar()

const store = useRecipeStore();
const { current } = storeToRefs(store);

const props = defineProps<{
  recipe?: Recipe;
  category?: Category;
  type: "thumbnail" | "detail" | "category";
}>();
const file = ref();
const loading = ref();

const route = useRoute();
const itemId = parseInt(route.params.id as string);
const getURL = () => {
  if (props.category) {
    return `${API_URL}/images/categories/${itemId}`;
  }

  if (props.type === "detail") {
    return `${API_URL}/recipes/${itemId}/detail-image`;
  }

  if (props.type === "thumbnail") {
    return `${API_URL}/recipes/${itemId}/thumbnail-image`;
  }

  return `${API_URL}/recipes/${itemId}/`;
};
const url = getURL();

// const isExtensionAllowed = (filename: string) => {
//   return (
//     filename.endsWith(".jpg") ||
//     filename.endsWith(".jpeg") ||
//     filename.endsWith(".png") ||
//     filename.endsWith("PNG")
//   );
// };

// const handleFile = (event: Event) => {
//   const target = event.target as HTMLInputElement;
//   if (target.files && target.files.length >= 1) {
//     file.value = target.files[0];
//     if (!isExtensionAllowed(file.value.name)) {
//       $q.notify({
//         type: "negative"

//       })
//       file.value = undefined;
//       bus.emit({
//         level: "ERROR",
//         message: "File extension not allowed. Choose an image instead.",
//       });
//     }
//   }
// };

const emit = defineEmits(["uploadSuccess"]);

const upload = async () => {
  loading.value = true;
  const formData = new FormData();
  formData.append("image", file.value);

  try {
    const result = await fetch(url, {
      method: "POST",
      body: formData,
    });
    const data = await result.json();

    if (props.type === "detail" && current.value) {
      current.value.detail_image = data.detail_image;
    }

    if (props.type === "thumbnail" && current.value) {
      current.value.thumbnail_image = data.thumbnail_image;
    }

    file.value = undefined;
    $q.notify({
      type: 'positive',
      message: "Image uploaded!",
    })
    emit("uploadSuccess", data);
  } catch (e: unknown) {
    $q.notify({
      type: 'negative',
      message: "Image upload failed...",
    })
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="css" scoped>
input {
  display: none;
}

label {
  cursor: pointer;

  &:hover {
    filter: brightness(0.8);
  }
}

.label-btn {
  pointer-events: none;
}
</style>
