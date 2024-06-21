<template>
  <div>
    <div v-if="data && data.length > 0">
       <recipes-grid :recipes="data"/>
    </div>
    <div v-else-if="error">
      <ui-empty
        icon="i-hugeicons-wifi-disconnected-01"
        title="Oh boi!"
        subtitle="Something wrong happened while fetching the data"
      />
    </div>
    <div v-else>
      <ui-empty
        icon="i-hugeicons-license-no"
        title="Goodness Gracious!"
        subtitle="The recipe list seems to have taken a tea break. Why not take charge and add your culinary masterpieces?"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RecipeListItem } from '@/types';

const { data, refresh, error } = await useApiData<RecipeListItem[]>('api/recipes')
</script>

<style lang="scss" scoped>

</style>