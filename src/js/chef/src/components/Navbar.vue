<template>
    <nav role="navigation" aria-label="main navigation">
      <div class="container">
        <router-link :to="{ name: 'home' }" id="logo">
          <img src="../assets/favicon.png" alt="Logo">
          <span class="ml-2">CHEF</span>
        </router-link>
     
        <router-link :to="{ name: 'categories'}" class="margin-left">
          <ui-button type="link" text="categories" icon="fas fa-folder"></ui-button>
        </router-link>

        <router-link :to="{ name: 'new'}" >
          <ui-button type="link" text="recipe" icon="fas fa-plus"></ui-button>
        </router-link>
      </div>
    </nav>
</template>

<script lang="ts" setup>
import UiButton from "@/components/ui/UiButton.vue"
</script>

<style lang="css" scoped>
nav {
  background-color: var(--primary);
  margin-bottom: .3rem;
}

#logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  color: var(--text-inv);
  font-weight: 100;
  font-size: xx-large;
}

.container {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-block: 1rem;
}

img {
  height: 3rem;
  aspect-ratio: 1;
  transition: filter 0.1s ease-in-out;

  &:hover {
    filter: brightness(1.05);
  }
}

.buttons {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  gap: 1rem;
}

a {
  text-decoration: none;
}

.margin-left {
  margin-left: auto;
  text-decoration: none;
}
</style>
