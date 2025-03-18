<template>
  <q-page padding>
    <h1 class="title-sm my-5">Add a new category</h1>
    <CategoryForm
      @categoryPosted="$router.push({ name: 'categories' })"
      @cancel="$router.push({ name: 'categories' })"
    />
  </q-page>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
</script>
