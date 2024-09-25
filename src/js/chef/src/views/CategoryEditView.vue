<template>
  <main v-if="current">
    <h1>{{ current.name }}</h1>
    <CategoryForm
      :inputCategory="current"
      @categoryPosted="$router.push({ name: 'category', params: { id: current.id }})"
      @cancel="$router.push({ name: 'category', params: { id: current.id } })"
    />
  </main>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
import { useCategoryStore } from "@/stores/categories";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";

const categories = useCategoryStore();
const { current, currentId } = storeToRefs(categories);

const router = useRouter();
const categoryId = parseInt(router.currentRoute.value.params.id as string);

currentId.value = categoryId;

if (!current.value) {
    await categories.fetchSingle(categoryId);
}

if (!current.value) {
  router.push({
    name: "notfound",
    query: { path: router.currentRoute.value.fullPath },
  });
}
</script>
