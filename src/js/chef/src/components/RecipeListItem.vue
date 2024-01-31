<template>
  <router-link
    :to="{ name: 'recipe', params: { id: recipe.id } }"
    style="text-decoration: none"
  >
    <article class="not-found">
      <h1>{{ recipe.title }}</h1>
      <h2 v-if="recipe.subtitle">{{ recipe.subtitle }}</h2>

      <div class="tags">
        <pin
          v-for="(tag, index) in recipe.tags"
          :text="tag.name"
          active
          size="small"
        />
      </div>
      <checkmark v-if="hasContent && hasIngredients" class="icon" width=".7rem" color="--success" />
    </article>
  </router-link>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";
import { computed } from "vue";
import { IMAGES_HOST } from "@/constants";

import Pin from "@/components/ui/Pin.vue";
import Checkmark from "./icons/Checkmark.vue";

const props = defineProps<{ recipe: Recipe }>();

const hasContent = computed(() => (props.recipe.body?.length ?? 0) > 0);
const hasIngredients = computed(() => (props.recipe.ingredients?.length ?? 0) > 0);

const image_url = computed(() => props.recipe.thumbnail_image ? `url(${IMAGES_HOST}${props.recipe.thumbnail_image})` : '@/assets/notfound.jpg')
</script>

<style lang="scss" scoped>
article {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 0.3rem;
  height: 10rem;
  position: relative;

  background-color: #ffebe8;

  background-image: v-bind("image_url");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;

  transition: filter 0.2s ease-in-out;


  &:hover {
    filter: contrast(1.2);
  }

}

h1,
h2 {
  margin: 0;
  color: var(--text-inv);
  text-shadow: 1px 1px 1px var(--text), 1px 1px 5px var(--text);
}

h2 {
  font-size: medium;
}

.tags {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
  flex-wrap: wrap;

  margin-top: auto;
}

.icon {
  position: absolute;
  top: 0.3rem;
  right: 0.3rem;
}
</style>
