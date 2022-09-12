<template>
  <div id="app">

    <Navbar class="mb-5" />

    <div class="container">
      <transition mode="out-in">
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

<style>
html {
  height: 100%;
}

body {
  height: 100%;
}

#app {
  height: 100%;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}


.v-enter-from,
.v-leave-to {
  transform: translateY(10px);
  opacity: 0;
}

.v-enter-active {
  transition: all 0.1s ease-out;
}

.v-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}


.fade-leave-to {
  opacity: 0;
}

.fade-enter {
  opacity: 0;
  translate: -120px;
}

.fade-leave-active,
.fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active,
.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}

.slide-fade-enter-from {
  transform: translateX(-30px);
  opacity: 0;
}
.slide-fade-leave-to {
  transform: translateX(30px);
  opacity: 0;
}
</style>