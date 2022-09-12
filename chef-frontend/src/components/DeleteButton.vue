<template>
  <div class="ml-1">
    <transition name="slide-fade" mode="out-in">
    <button v-if="!youSure" @click="youSure=!youSure" class="button is-danger is-small is-rounded clickable-link">
      <i class="fas fa-trash"></i>
    </button>
    <div v-else>
      <div class="field has-addons">
        <p class="control">
          <button @click="$emit('delete')" class="button is-small is-rounded is-danger">
            <span class="icon is-small">
              <i class="fas fa-trash"></i>
            </span>
          </button>
        </p>
        <p class="control">
          <button @click="youSure=!youSure" class="button is-small is-rounded">
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
          </button>
        </p>
      </div>
    </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      youSure: false
    };
  },
}
</script>

<style>

</style>