<template>
  <main v-if="recipe" class="">
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
        <span v-if="recipe.source">
          <q-icon name="link" size="1.6rem" class="mr-1"/>
          <a :href="recipe.source" class="light:text-dark dark:text-white text-lg">
            <span v-if="recipe.source_name">{{ recipe.source_name }}</span>
            <span v-else>{{ recipe.source }}</span>
          </a>
        </span>

        <div class="flex flex-wrap gap-1 pointer-events-none select-none">
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
    <section class="ProseMirror" v-if="recipe.body" ref="reader">
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
import Counter from "@/components/Counter.vue";
import RecipeForm from "@/components/RecipeForm.vue";
import EmptyBox from "@/components/ui/EmptyBox.vue";
import ImageUpload from "@/components/ui/ImageUpload.vue";
import Pin from "@/components/ui/Pin.vue";
import UiButton from "@/components/ui/UiButton.vue";
import RecipeIngredientsSection from "@/components/recipe/RecipeIngredientsSection.vue";
import Pot from "@/components/icons/Pot.vue";

import { IMAGES_HOST } from "@/constants";
import { useRecipeStore } from "@/stores/recipe";
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import type { ChefNotification, Recipe } from "@/types";
import {
  useEventBus,
  useFullscreen,
  useLocalStorage,
  useWakeLock,
} from "@vueuse/core";
import { storeToRefs } from "pinia";
import { useLayoutDrawer } from "@/composables/drawer";

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

const responseBusId = `delete-recipe-${recipeId}`;
const bus = useEventBus<ChefNotification>("notifications");
const responseBus = useEventBus<string>(responseBusId);

const portions = ref<number>(current.value?.portions ?? 4);

const editMode = useLocalStorage(`${recipeId}-recipe-edit-mode`, false);
const updateRecipe = () => {
  router.push({ name: "editrecipe", params: { id: recipe.value.id } });
};

const ingredientsCollapsed = ref<boolean>(false);

const missingImage = ref<boolean>(false);

const image_url = computed(
  () => `${IMAGES_HOST}${current.value?.detail_image}`
);

const clickDelete = () =>
  bus.emit({
    level: "ERROR",
    message: `Delete recipe ${current.value?.title ?? "N/A"} ?`,
    action: {
      id: responseBusId,
      label: "Delete",
    },
  });

const onDeleteConfirmListener = () => {
  recipes.deleteById(recipeId).then(() => router.push("/recipes"));
};

responseBus.on(onDeleteConfirmListener);

// const imageUploaded = async (newRecipe: Recipe) => {
//   console.info(newRecipe);
//   current.value.detail_image = newRecipe.detail_image;
// };

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

function toggleReaderMode() {
  if (readerMode.value) {
    exitReaderMode();
  } else {
    enterReaderMode();
  }
  readerMode.value = !readerMode.value;
}
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

a:hover {
  filter: opacity(0.8);
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
