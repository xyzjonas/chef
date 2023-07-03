<template>
  <div id="app">
    
    <Navbar class="mb-2" />

    <div class="container pb-4 px-1">
      <transition mode="out-in">
        <keep-alive>
          <router-view/>
        </keep-alive>
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

/* ----------------- */


.loading-leave-to {
  opacity: 0;
}

.loading-enter {
  opacity: 0;
  translate: -120px;
}

.loading-leave-active,
.loading-enter-active {
  transition: all 0.3s ease-out;
}

/* ----------------- */

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

/* ----------------- */

.slide-leave-active,
.slide-enter-active {
  transition: all 0.15s ease-out;
}

.slide-enter {
  transform: translateX(-30px);
  opacity: 0;
}
.slide-leave-to {
  transform: translateX(30px);
  opacity: 0;
}

/* ----------------- */

.slide-up-leave-active,
.slide-up-enter-active {
  transition: all 0.15s ease-out;
}

.slide-up-enter {
  transform: translateY(-30px);
  opacity: 0;
}
.slide-up-leave-to {
  transform: translateY(-30px);
  opacity: 0;
}
</style>