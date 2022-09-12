<template>
  <section class="section has-text-centered py-0">
    <button
      v-if="loading" class="button is-loading p-0"
      disabled style="border: 0px; font-size: 120px">X</button>
  </section>
</template>

<script>
export default {

  props: ['loading']

}
</script>

<style>

</style>