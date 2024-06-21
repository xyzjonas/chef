<template>
  <div v-if="recipe">
    <div class="flex gap-3 justify-between flex-wrap frame">
      <!-- <img :src="recipe.detail_image ?? '/notfound.jpg'" alt="recipe"> -->
      <div class="img"></div>
      <div class="flex-1 flex flex-col">
        <h1>{{ recipe.title }}</h1>
        <h2 v-if="recipe.subtitle">{{ recipe.subtitle }}</h2>
        <a v-if="recipe.source" :href="recipe.source" target="_blank">
          <i class="icon i-hugeicons-link-02"></i>
          {{ recipe.source_name ?? recipe.source }}
        </a>
        <div class="flex flex-wrap mt-5 gap-1">
          <ui-pin
            v-for="tag in recipe.tags"
            :text="tag.name"
            color="var(--primary-100)"
          />
        </div>
        <div class="flex flex-wrap mt-2 gap-1">
          <ui-pin>
            <i class="icon i-hugeicons-rice-bowl-01"></i>
            <span>{{ recipe.portions }} SERVINGS</span>
          </ui-pin>
          <ui-pin>
            <i class="icon i-hugeicons-time-02"></i>
            <span>20min</span>
          </ui-pin>
        </div>
        <recipes-ingredients-list
          v-if="recipe.ingredients.length > 0"
          v-model="recipe.portions"
          :ingredients="recipe.ingredients"
          class="flex-1 mt-3"
        />
        <ui-empty
          v-else
          class="mt-3"
          title="no ingredients"
          icon="i-hugeicons-check-list"
          fixed-height="100%"
        />
      </div>
    </div>
    <section
      v-if="recipe.body"
      class="content my-5"
      v-html="recipe.body"
    ></section>
    <ui-empty
      v-else
      class="mt-3"
      title="no recipe"
      subtitle="...shame&nbsp;on&nbsp;us!"
      icon="i-hugeicons-pot-02"
    />
  </div>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";

const route = useRoute();
const {
  data: recipe,
  refresh,
  error,
} = await useApiData<Recipe>(`api/recipes/${route.params.id}`);
if (error.value) {
  navigateTo("/404");
}

const backgroundUrl = computed(
  () => recipe.value?.detail_image ?? "/notfound.jpg"
);
const background = computed(() => `url('${backgroundUrl.value}')`);
</script>

<style lang="css" scoped>
h1,
h2 {
  text-align: left;
}

h1 {
  --font-size: min(max(5dvw, 3rem), 5rem);
  font-size: var(--font-size);
  line-height: var(--font-size);
  font-weight: 400;
  text-transform: uppercase;
  text-wrap: wrap;
}

h2 {
  font-size: 2rem;
  text-transform: uppercase;
}

.img {
  flex: 1;
  border-radius: 0.5rem;
  background-image: v-bind("background");
  background-position: center;
  background-size: cover;
  aspect-ratio: 1;
  min-width: 20rem;
}

a:hover {
  text-decoration: underline;
}
</style>
