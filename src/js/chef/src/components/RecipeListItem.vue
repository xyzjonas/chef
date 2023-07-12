<template>
  <div>
    
    <router-link :to="{ name: 'recipe', params: {id: recipe.id}}">
      <article class="media box boxhov p-0">
        <figure class="media-left m-0">
          <p class="image is-96x96" style="display: flex;">
            <img
              ref="recipeImage"
              :src="getImageUrl()"
              alt="recipe image"
              class="is-rounded p-2"
            >
          </p>
        </figure>
        <div class="media-content p-3">
          <div class="content">
            <p class="title is-5">
              {{ recipe.title }}
              <br>
              <span 
                v-if="recipe.subtitle"
                style="color: gray"
              ><small>{{ recipe.subtitle }}</small></span>
            </p>
          </div>
          <nav class="level">
            <div class="level-left">
              <div class="tags my-0">
                  <span class="tag is-rounded" v-for="(tag, index) in recipe.tags" :key="'item-tag-' + index">{{tag.name}}</span>
              </div>
            </div>
          </nav>
        </div>
      </article>
    </router-link>

  </div>
</template>

<script setup lang="ts">
import type { Recipe } from '@/types';
import { onMounted, ref } from 'vue';
import { IMAGES_URL } from '@/constants';

const props = defineProps<{ recipe: Recipe }>();

const imageFailedToLoad = ref(false);
    
const getImageUrl = (): string => {
  // todo: check if image exists, replace with unknown if yes
  return `${IMAGES_URL}/${props.recipe.id}/small.jpeg`
};

const recipeImage = ref<HTMLInputElement | null>(null);
onMounted(() => {
    // Failsafe for images
    if (recipeImage.value) {
      recipeImage.value.onerror = el => {
        if (imageFailedToLoad.value) {
          el.target.src = "";
          return;
        }
        imageFailedToLoad.value = true;
        el.target.src = `${IMAGES_URL}/not-found.png`;
      }
    }
})
</script>

<style lang="scss" scoped>
  .breakline {
    display: block;
    max-width: 1em;
  }
  .boxhov:hover {
    background-color: #f5f5f5;
  }
  .bordered {
    outline-style: solid;
    outline-width: 1px;
    outline-color: lightgray;
  }
  .vertical {
    display: flex;
    align-items: center;
  }
  .title {
    font-weight: 500;
    text-transform: uppercase;
  }
</style>