<template>
    <div id="app">
    
      <Navbar class="mb-2" />

      <main class="container">
        <RouterView v-slot="{ Component }">
          <template v-if="Component">

            <Transition mode="out-in">
              <KeepAlive :exclude="['Recipe', 'CategoryView', 'CategoryTile']">
                <Suspense>
                  <component :is="Component"></component>
                  <template #fallback>
                    LOADING...
                  </template>
                </Suspense>
              </KeepAlive>
            </Transition>

          </template>
        </RouterView>
      </main>

      <app-footer />

      <Notificaton />

    </div>

</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import Notificaton from './components/ui/Notificaton.vue';
import { useRecipeStore } from './stores/recipe';
import { useIngredientStore } from './stores/ingredient';
import { useTagStore } from './stores/tags';
import { useUnitsStore } from './stores/units';
import { useCategoryStore } from './stores/categories';

const recipes = useRecipeStore();
recipes.fetch();

const categories = useCategoryStore();
categories.fetch();

const ingredients = useIngredientStore();
ingredients.fetch();

const tags = useTagStore();
tags.fetch();

const units = useUnitsStore();
units.fetch();

</script>

<style>

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}

main {
  padding-bottom: .5rem;
}

footer {
  margin-top: auto;
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