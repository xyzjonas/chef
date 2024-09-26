<template>
  <main v-if="recipe" class="pb-10">
    <div class="flex flex-row gap-3">
      <q-img
        v-if="!readerMode"
        :src="recipe.detail_image ?? 'none'"
        spinner-color="white"
        error-src="@/assets/notfound.jpg"
        class="rounded-md flex-1 min-w-[20rem] mb-3"
      />
      <div class="flex-1 flex flex-col gap-5 min-w-[10rem]">
        <div v-if="!readerMode" class="overflow-hidden max-w-[100%]">
          <h1 class="recipe-title">{{ recipe.title }}</h1>
          <h2
            v-if="recipe.subtitle"
            class="text-[1.5rem] font-400 uppercase color-gray m-0 line-height-snug"
          >
            {{ recipe.subtitle }}
          </h2>
        </div>

        <recipe-external-link v-if="!readerMode && recipe.source" :href="recipe.source" :label="recipe.source_name" />

        <div v-if="!readerMode" class="flex flex-wrap gap-1 pointer-events-none select-none">
          <pin
            v-for="tag in recipe.tags"
            :key="tag.name"
            :text="tag.name"
            active
          />
        </div>

        <div class="flex mt-auto items-center">
          <q-toggle
            v-model="readerMode"
            color="primary"
            class="ml-auto"
            checked-icon="soup_kitchen"
            size="3.5rem"
          />
          <div class="flex flex-col">
            <span>Cooking mode</span>
            <span class="text-[.6rem] text-gray-4">Keep display turned on</span>
          </div>

        </div>
      </div>
    </div>

    <recipe-ingredients-section :recipe="recipe" />

    <!-- HTML body -->
    <section class="ProseMirror mt-3" v-if="recipe.body" ref="reader">
      <div v-html="recipe.body" />
    </section>
    <section v-else id="empty">
      <empty-box
        title="recipe is missing"
        subtitle="...shame on us!"
        :icon="Pot"
      />
    </section>
  </main>
</template>

<script setup lang="ts">
import Pot from "@/components/icons/Pot.vue";
import RecipeIngredientsSection from "@/components/recipe/RecipeIngredientsSection.vue";
import EmptyBox from "@/components/ui/EmptyBox.vue";
import Pin from "@/components/ui/Pin.vue";
import RecipeExternalLink from "@/components/recipe/RecipeExternalLink.vue";

import { IMAGES_HOST } from "@/constants";
import { useRecipeStore } from "@/stores/recipe";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useLayoutDrawer } from "@/composables/drawer";
import type { ChefNotification, Recipe } from "@/types";
import {
  useEventBus,
  useLocalStorage,
  useWakeLock
} from "@vueuse/core";
import { storeToRefs } from "pinia";

const recipes = useRecipeStore();
const { current, currentId } = storeToRefs(recipes);

const router = useRouter();
const route = useRoute();
const recipeId = parseInt(route.params.id as string);

currentId.value = recipeId;

if (!current.value) {
  await recipes.fetchSingle(recipeId);
}

if (!current.value) {
  router.push({
    name: "notfound",
    query: { path: router.currentRoute.value.fullPath },
  });
}

const recipe = computed<Recipe>(() => current.value as Recipe);

const { request, release } = useWakeLock();
const { isOpened } = useLayoutDrawer();
let stateBefore = isOpened.value;

const readerMode = ref(false);

function enterReaderMode() {
  stateBefore = isOpened.value;
  isOpened.value = false;
  request("screen");
}

function exitReaderMode() {
  isOpened.value = stateBefore;
  release();
}

watch(readerMode, (value) => {
  if (value) {
    enterReaderMode()
  } else {
    exitReaderMode()
  }
})
</script>

<style lang="scss" scoped>

.tag {
  margin-bottom: 0%;
  padding-top: 1px;
}

.hide {
  visibility: hidden;
}

#empty {
  display: flex;
  flex-direction: column;
  min-height: 50dvh;
}

img {
  width: 20dvh;
  aspect-ratio: 1;
  border-radius: 50%;
  mask-image: radial-gradient(rgb(0 0 0 / 100%) 50%, transparent);
  object-fit: cover;
}

.heading {
  gap: 3rem;
}

#delete-btn {
  margin-right: auto;
}

#edit-title {
  margin-bottom: 1rem;
  text-transform: none;
}

#recipe-link {
  margin-bottom: 2rem;
}

#recipe-link > a {
  color: var(--primary);
}

.heading-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ProseMirror {
  background-color: transparent !important;
  outline-color: transparent !important;
  outline-style: none !important;
  outline-width: 0px !important;
}

.recipe-title {
  --size: 3.5rem;
  font-size: var(--size);
  line-height: calc(var(--size) * 0.95);
}
</style>
