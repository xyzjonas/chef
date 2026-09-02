<template>
  <div class="level is-mobile mb-3">
      <button @click="open()" class="button level-item" style="width: 100%">
        <span class="icon is-small">
          <i class="fas fa-plus"></i>
        </span>
        <span>Recipe</span>
      </button>
  </div>
</template>

<script setup lang="ts">
import { useNewRecipeDialog } from "@/composables/newRecipeDialog";

const { open } = useNewRecipeDialog();
</script>

<style>

</style>