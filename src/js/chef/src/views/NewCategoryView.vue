<template>
<div class="px-3">
  <h1 class="title is-3">Add a new category</h1>
  <CategoryForm
    @categoryPosted="$router.push({name: 'categories'})"
    @cancel="$router.push({name: 'categories'})"
  />
</div>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
</script>

<style lang="css" scoped>
h1 {
  font-weight: 100;
}
</style>
