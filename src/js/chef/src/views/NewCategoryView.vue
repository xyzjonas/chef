<template>
<div class="px-3">
  <h1 class="title is-3">Add</h1>
  <h2 class="subtitle is-5">a new category</h2>
  <CategoryForm
    @categoryPosted="$router.push({name: 'home'})"
    @cancel="$router.push({name: 'home'})"
  />
</div>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
</script>
