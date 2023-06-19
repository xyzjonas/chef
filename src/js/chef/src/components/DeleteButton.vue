<template>
  <div class="ml-1">
    <transition name="slide-up" mode="out-in">
    <button 
      v-if="!youSure"
      @click="youSure=!youSure"
      :class="{
        button: true,
        'is-danger': true,
        'is-small': small,
        'is-rounded': rounded,
        'clickable-link': true
      }">
      <i class="fas fa-trash"></i>
    </button>
    <div v-else>
      <div class="field has-addons">
        <p class="control">
          <button
            @click="$emit('delete')"
            :class="{
              button: true,
              'is-danger': true,
              'is-small': small,
              'is-rounded': rounded,
              'clickable-link': true
            }">
            <span class="icon is-small">
              <i class="fas fa-trash"></i>
            </span>
          </button>
        </p>
        <p class="control">
          <button
            @click="youSure=!youSure"
            :class="{
              button: true,
              'is-small': small,
              'is-rounded': rounded,
              'clickable-link': true
            }">
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

  props: ['small', 'rounded'],

  data() {
    return {
      youSure: false
    };
  },
}
</script>

<style>

</style>