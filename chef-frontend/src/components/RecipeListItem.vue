<template>
  <div>

    <!-- <div class="box p-0 my-1 boxhov">
      <router-link :to="{ name: 'Recipe', params: {id: recipe.id}}">
      <div class="level mb-1 is-mobile">
          <div class="level-left">
            <div class="level-item">
              <figure class="image is-96x96">
                  <img
                    :src="getImageUrl()"
                    alt="recipe image"
                    class="is-rounded p-2"
                  >
              </figure>
            </div>
          </div>
          <div class="level-left">
            <div class="level-item has-text-centered breakline" style="max-width: parent;">
              <div class="content">
                <h6>{{ recipe.title.toUpperCase() }}</h6>
                <p v-if="recipe.subtitle !== 'None'">{{ recipe.subtitle }}</p>
              </div>
            </div>
          </div>
      </div>
      </router-link>
      <div class="tags my-0 px-2">
          <span class="tag is-rounded" v-for="(tag, index) in recipe.tags" :key="'item-tag-' + index">{{tag.name}}</span>
      </div>
    </div> -->
    <router-link :to="{ name: 'Recipe', params: {id: recipe.id}}">
      <article class="media my-1 box boxhov p-0">
        <figure class="media-left">
          <p class="image is-96x96" style="display: flex;">
            <img
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
              <div class="tags my-0 px-2">
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
// import axios from 'axios';

export default {
  props: ["recipe"],
  methods: {
    getImageUrl() {
      // todo: check if image exists, replace with unknown if yes
      return `http://www.recepty.home/images/${this.recipe.id}.jpeg`
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
    background-color: lightgray;
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