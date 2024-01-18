<template>
    <nav role="navigation" aria-label="main navigation">
      <div class="container">
        <router-link :to="{ name: 'home' }" id="logo">
          <img src="../assets/favicon.png" alt="Logo">
          <span class="ml-2">CHEF</span>
        </router-link>

        <router-link :to="{ name: 'recipes'}" class="button is-primary mx-0">
          <ui-button type="link" text="recipes" icon="fas fa-list"></ui-button>
        </router-link>

        <router-link :to="{ name: 'home'}" class="button is-primary mx-0">
          <ui-button type="link" text="categories" icon="fas fa-folder"></ui-button>
        </router-link>

        <router-link :to="{ name: 'new'}" id="new-recipe">
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
}

#logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  color: var(--text-inv);
  font-weight: 100;
  font-size: x-large;
  margin-right: 2rem;
}

.container {
  display: flex;
  flex-direction: row;
  gap: .3rem;
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

#new-recipe {
  margin-left: auto;
  text-decoration: none;
}
</style>
