<template>
  <div class="app-wrapper font-sans">
    <layout-head />

    <main class="page my-3">
      <slot />
    </main>
   
    <layout-foot class="footer" />
    
    <div class="notification-drawer">
      <TransitionGroup name="slide">
        <div v-for="notif in notifications" :key="notif.created.toISOString()">
          <ui-notification :notification="notif" />
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useNotifications } from "@/composables/useNotifications";
const { notifications } = useNotifications();
</script>

<style lang="css" scoped>
.app-wrapper {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
}

.page {
  flex: 1;
}

.footer {
  margin-top: auto;
}
</style>
