<template>
  <div class="level">
    <!-- upload -->
    <ui-button v-if="file" @click="upload" icon="fas fa-upload" text="upload" />

    <!-- choose file -->
    <label v-else :for="inputId">
      <ui-button
        icon="fas fa-image"
        class="label-btn"
        type="secondary"
        :text="type"
      />
    </label>
    <input
      @change="handleFile"
      :id="inputId"
      class="file-input"
      type="file"
      name="resume"
    />
    <ui-button
      v-if="file"
      @click="file = undefined"
      icon="fa-solid fa-ban"
      text="cancel"
      type="secondary"
    />
  </div>
</template>

<script setup lang="ts">
import UiButton from "./UiButton.vue";
import { API_URL } from "@/constants";
import { ref } from "vue";
import { useRoute } from "vue-router";
import type { Category, ChefNotification, Recipe } from "@/types";

import { useEventBus } from "@vueuse/core";

const bus = useEventBus<ChefNotification>("notifications");

const props = defineProps<{
  recipe?: Recipe;
  category?: Category;
  type: "thumbnail" | "detail" | "category";
}>();
const inputId = `image-${props.type}`;
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

const isExtensionAllowed = (filename: string) => {
  return (
    filename.endsWith(".jpg") ||
    filename.endsWith(".jpeg") ||
    filename.endsWith(".png") ||
    filename.endsWith("PNG")
  );
};

const handleFile = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length >= 1) {
    file.value = target.files[0];
    if (!isExtensionAllowed(file.value.name)) {
      file.value = undefined;
      bus.emit({
        level: "ERROR",
        message: "File extension not allowed. Choose an image instead.",
      });
    }
  }
};

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
    file.value = undefined;
    bus.emit({
      level: "SUCCESS",
      message: "Image uploaded",
    });
    emit("uploadSuccess", data);
  } catch (e: unknown) {
    bus.emit({
      level: "ERROR",
      message: "Image upload failed",
    });
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
