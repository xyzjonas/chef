<template>
  <div>
    
    <router-link :to="{ name: 'recipe', params: {id: recipe.id}}">
      <article class="media my-1 box boxhov p-0">
        <figure class="media-left">
          <p class="image is-96x96" style="display: flex;">
            <img
              ref="r-img"
              :src="getImageUrl()"
              alt="recipe image"
              class="is-rounded p-2"
            >
          </p>
        </figure>
        <div class="media-content p-4">
          <div class="content">
            <p class="title is-5">
              {{ recipe.title.toUpperCase() }}
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

<script>
import Constants from '@/components/Constants.vue';
// import axios from 'axios';

export default {
  props: ["recipe"],

  data() {
    return {
      imageFailedToLoad: false,
    }
  },

  methods: {
    getImageUrl() {
      // todo: check if image exists, replace with unknown if yes
      return `${Constants.IMAGES_URL}/${this.recipe.id}/medium.jpeg`
    },
  },

  mounted() {

    // Failsafe for images
    this.$refs["r-img"].onerror = el => {
      if (this.imageFailedToLoad) {
        el.target.src = "";
        return;
      }
      this.imageFailedToLoad = true;
      el.target.src = `${Constants.IMAGES_URL}/not-found.png`;
    }
  }
};
</script>

<style>
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
</style>