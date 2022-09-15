<template>
  <div class="level is-mobile mb-3">
      <button @click="$emit('category')" class="button level-item mr-1" style="width: 50%">
        <span class="icon is-small">
          <i class="fas fa-plus"></i>
        </span>
        <span>Category</span>
      </button>
      <button @click="$router.push({ name: 'new' })" class="button level-item" style="width: 50%">
        <span class="icon is-small">
          <i class="fas fa-plus"></i>
        </span>
        <span>Recipe</span>
      </button>
  </div>
</template>

<style>

</style>