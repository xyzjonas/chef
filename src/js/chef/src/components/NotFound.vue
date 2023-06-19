<template>
  <section class="section is-medium has-text-centered">
    <h1 class="title">Oooops...</h1>
    <h2 class="subtitle">
      {{ msg }}
    </h2>
    <span class="icon is-large">
      <i class="fas fa-2x fa-dizzy"></i>
    </span>
  </section>
</template>

<script>
export default {
  props: ["name", "message"],

  data() {
    return {
      msg: "404 not found"
    };
  },

  created() {
    if (this.name) {
      this.msg = `404 ${this.name} not found.`;
    }
    if (this.message) {
      this.msg = this.message;
    }
  }
}
</script>

<style>

</style>