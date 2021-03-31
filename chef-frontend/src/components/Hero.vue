<template>
  <section class="hero is-dark">
    <div class="hero-body">
      <div class="container has-text-centered">
        <p class="title noselect">{{ title }}</p>
        <p class="subtitle noselect">{{ subtitle }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: ["title", "subtitle"]
}
</script>

<style>

</style>