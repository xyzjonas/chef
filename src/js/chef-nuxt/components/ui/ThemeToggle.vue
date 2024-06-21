<template>

  <ui-button
    @click="toggle"
    :icon="isDark ? 'i-hugeicons-moon-02' : 'i-hugeicons-sun-02'"
    rounded
    color="primary"
  />
</template>

<script setup lang="ts">
const { isDark, toggle } = useTheme()
</script>
