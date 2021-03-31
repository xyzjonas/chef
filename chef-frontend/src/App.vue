<template>
  <div id="app">
    <Navbar/>
    <section class="hero is-dark is-small">
      <div class="hero-body">
      </div>
    </section>
    <div class="container px-3 mt-5">
      <transition name="slide">
        <router-view/>
      </transition>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar
  },
};
</script>