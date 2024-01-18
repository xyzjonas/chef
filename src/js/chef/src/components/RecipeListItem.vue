<template>
  <router-link
    :to="{ name: 'recipe', params: { id: recipe.id } }"
    style="text-decoration: none"
  >
    <article>
      <!-- <img :src="image" :alt="recipe.title" > -->
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
      <svg v-if="!isContent" id="is-content" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 4V20M17 12V20M6 20H10M15 20H19M13 7V4H3V7M21 14V12H13V14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <svg v-if="!isIngredients" id="is-ingredients" version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 314.862 314.862" xmlns:xlink="http://www.w3.org/1999/xlink" enable-background="new 0 0 314.862 314.862">
        <g>
          <path d="m111.964,160.37c0.841,10.703 11.333,17.847 21.558,14.789 8.885-2.657 13.934-12.015 11.277-20.9-4.504-15.064-12.983-44.946-31.316-69.222l2.629-6.734 .458-6.887 .639-.337c3.783-2.002 6.457-5.553 7.338-9.749l2.181-10.425c0.617-2.95 0.302-5.967-0.912-8.723l-12.685-28.922c-4.474-10.203-16.361-14.852-26.568-10.37l-74.486,32.662c-10.207,4.476-14.849,16.36-10.371,26.568l23.293,53.119c4.467,10.186 16.388,14.835 26.568,10.369l50.561-22.173c6.888,21.949 8.168,32.289 9.836,56.935zm-10.865-109.055l-1.462,.772c-4.436,2.344-7.283,6.73-7.618,11.738l-.598,8.974-3.782,9.692-41.686,18.28-19.41-44.265 65.633-28.781 9.382,21.395-.459,2.195z"/>
          <path d="m302.786,77.107l-74.484-32.663c-10.183-4.466-22.101,0.184-26.57,10.369l-12.687,28.935c-1.211,2.757-1.524,5.771-0.908,8.71l2.179,10.412c0.874,4.203 3.553,7.764 7.348,9.768l.631,.333 .458,6.887 2.806,7.188c-30.768,39.907-33.418,72.477-33.672,73.524h-101.664c-6.903,0-12.5,5.597-12.5,12.5 0,30.735 14.743,58.121 37.594,75.61h-2.528c-6.903,0-12.5,5.597-12.5,12.5s5.597,12.5 12.5,12.5h122.951c6.903,0 12.5-5.597 12.5-12.5s-5.597-12.5-12.5-12.5h-2.528c22.85-17.489 37.594-44.876 37.594-75.61 0-6.903-5.597-12.5-12.5-12.5h-33c1.574-19.151 3.964-37.019 11.25-55.658l50.739,22.25c10.187,4.467 22.103-0.187 26.569-10.37l23.293-53.117c4.475-10.207-0.161-22.094-10.371-26.568zm-82.105,148.462c-6,32.957-35.292,58.044-70.416,58.044s-64.417-25.087-70.417-58.044h140.833zm48.229-83.244l-41.686-18.279-3.783-9.692-.597-8.96c-0.323-4.933-3.239-9.435-7.618-11.752l-1.462-.772-.46-2.195 9.382-21.394 65.634,28.781-19.41,44.263z"/>
        </g>
      </svg>
    </article>
  </router-link>
</template>

<script setup lang="ts">
import type { Recipe } from "@/types";
import { computed, onMounted, ref } from "vue";
import { IMAGES_URL } from "@/constants";

import Pin from "@/components/ui/Pin.vue";

const props = defineProps<{ recipe: Recipe }>();

const imageFailedToLoad = ref(false);

const getImageUrl = (): string => {
  // todo: check if image exists, replace with unknown if yes
  return `${IMAGES_URL}/${props.recipe.id}/small.jpeg`;
};

const image = computed(() => getImageUrl());
const imageUrl = computed(() => `url(${image.value})`);

const isContent = computed(() => (props.recipe.body?.length ?? 0) > 0);
const isIngredients = computed(() => (props.recipe.ingredients?.length ?? 0) > 0);

// const recipeImage = ref<HTMLInputElement | null>(null);
// onMounted(() => {
//     // Failsafe for images
//     if (recipeImage.value) {
//       recipeImage.value.onerror = el => {
//         if (imageFailedToLoad.value) {
//           el.target.src = "";
//           return;
//         }
//         imageFailedToLoad.value = true;
//         el.target.src = `${IMAGES_URL}/not-found.png`;
//       }
//     }
// })
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

  background-image: v-bind("imageUrl");
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

#is-content,
#is-ingredients {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: .8rem;
  border-radius: 50%;
  filter: drop-shadow(1px 1px 1px var(--text));

  & path {
    stroke: var(--text-inv);;
  }
}

#is-ingredients {
  right: 1.3rem;
  fill: var(--text-inv);    
}
</style>
