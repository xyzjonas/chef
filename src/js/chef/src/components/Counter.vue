<template>
  <div class="field has-addons">
      <p class="control">
        <a class="button is-small" v-on:click="decrement">
          <span class="icon is-small">
            <i class="fas fa-minus"></i>
          </span>
        </a>
      </p>
      <p class="control is-expanded">
        <input class="input has-text-centered is-small" type="text" v-model="counter" disabled>
      </p>
      <p class="control">
        <a class="button is-small" v-on:click="increment">
          <span class="icon is-small">
            <i class="fas fa-plus"></i>
          </span>
        </a>
      </p>
    </div>
</template>

<script>
export default {

  props: ["initialValue"],

  data() {
    return {
      counter: 4,
    };
  },
  methods: {

    increment() {
      this.$emit('counterUpdate', ++this.counter);
    },

    decrement() {
      if (this.counter == 0) return;
      this.$emit('counterUpdate', --this.counter);
    }

  },
  created() {
    if (this.initialValue) {
      this.counter = this.initialValue;
    }
  },
}
</script>

<style>

</style>