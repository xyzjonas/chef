<template>
  <section class="section has-text-centered py-0">
    <button
      v-if="loading"
      class="loading-btn button is-loading p-0"
      disabled>X</button>
  </section>
</template>

<script>
export default {

  props: ['loading']

}
</script>

<style>
.loading-btn {
  border: 0px !important;
  font-size: 120px !important;
}
.loading-btn::after {
  border: 3px solid #d35559 !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
}
</style>