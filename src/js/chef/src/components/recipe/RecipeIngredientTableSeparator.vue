<template>
  <tr class="h-[1rem]">
    <td colspan="2">
      <div class="h-[1px] bg-gray-4 dark:bg-gray-5"></div>
    </td>
  </tr>
  <!-- two rows to correct the altering nth-of-type bg pattern -->
  <tr>
    <td colspan="2"></td>
  </tr>
</template>

<script setup lang="ts">
import type { IngredientItem } from "@/types";

defineProps<{
  ingredient: IngredientItem;
  portions: number;
  basePortions: number;
}>();
</script>

<style lang="css" scoped></style>
