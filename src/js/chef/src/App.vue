<template>
  <q-layout view="hHh lpR fff" class="font-sans light:text-[#273440] dark:text-white">
    <q-header class="bg-primary text-white py-1">
      <app-header />
    </q-header>

    <app-left-drawer />

    <q-page-container class="max-w-[1200px] mx-auto">
      <RouterView v-slot="{ Component }" class="p-2">
          <template v-if="Component">
            <!-- <Transition mode="out-in" name="blur"> -->
              <!-- <KeepAlive> -->
                <Suspense>
                  <component :is="Component"></component>
                  <template #fallback>
                    <q-page class="grid justify-center items-center">
                      <div class="flex flex-col items-center gap-2">
                        <q-spinner color="primary" size="4rem" :thickness="1" ></q-spinner>
                        <h1 class="uppercase text-xl text-primary">Loading</h1>
                      </div>
                  </q-page>
                  </template>
                </Suspense>
              <!-- </KeepAlive> -->
            <!-- </Transition> -->
          </template>
        </RouterView>
    </q-page-container>


    <Notificaton />

    <q-footer class="bg-grey-8 text-white">
      <app-footer />
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import AppFooter from "@/components/layout/AppFooter.vue";
import AppHeader from "@/components/layout/AppHeader.vue";
import Notificaton from "@/components/ui/Notificaton.vue";
import AppLeftDrawer from "./components/layout/AppLeftDrawer.vue";
import { useCategoryStore } from "./stores/categories";
import { useIngredientStore } from "./stores/ingredient";
import { useRecipeStore } from "./stores/recipe";
import { useTagStore } from "./stores/tags";
import { useUnitsStore } from "./stores/units";

import { useLayoutDrawer } from "@/composables/drawer";

const { isOpened, toggle } = useLayoutDrawer();

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

document.body.classList.add('font-sans')
</script>

<style lang="css">
.spinner {
  position: absolute;
  inset: 0;
  display: grid;
  align-content: center;
  justify-content: center;
}

#brand {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
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

.blur-leave-to, .blur-enter {
  filter: blur(50px);
}

.blur-leave-active,
.blur-enter-active {
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
