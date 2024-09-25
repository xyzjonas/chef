<template>
  <main>
    <h1>Add a new category</h1>
    <CategoryForm
      @categoryPosted="$router.push({name: 'categories'})"
      @cancel="$router.push({name: 'categories'})"
    />
  </main>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
</script>
