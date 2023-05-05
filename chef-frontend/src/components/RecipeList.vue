<template>
  <div>

    <!-- RECIPE COUNT -->
    <div v-if="isInitState()">
      <h1 class="title is-4 has-text-primary">{{ allRecipes.length }} Recipes</h1>
    </div>
    <div v-else>
      <h1 class="title is-4 has-text-primary">{{ recipes.length }} Recipes</h1>
    </div>

    <!-- TAGS -->
    <div class="tags mt-2">
      <a v-for="(tag) in new Set(allRecipes.map(r => r.tags.map(t => t.name)).flat())" :key="'tag_key' + tag"
        v-on:click="toggleFilter(tag)"
        :class="{ 'tag':true,  'is-rounded':true, 'is-dark': activeTags.includes(tag), 'noselect': true}"
        style="text-decoration:none;"
      >{{ tag }}</a>
    </div>

    <!-- search -->
    <p class="control has-icons-left mb-4">
      <input 
        v-model="search"
        @input="refresh"
        class="input is-rounded"
        type="text"
        placeholder="search">
      <span class="icon is-small is-left">
        <i class="fas fa-search"></i>
      </span>
    </p>

    <!-- LIST -->
    <div id="init-list" v-if="isInitState()">
      <div v-for="(recipe) in allRecipes" :key="'recipe_key+' + recipe.id">
        <RecipeListItem :recipe="recipe"/>
      </div>
    </div>
    <div v-else>
      <div v-for="(recipe) in recipes" :key="'recipe_a_key+' + recipe.id">
        <RecipeListItem :recipe="recipe"/>
      </div>
    </div>

  </div>  
</template>

<script>
// import axios from "axios";
import RecipeListItem from "../components/RecipeListItem.vue";
import Constants from "../components/Constants.vue";

export default {
  props: ["allRecipes"],

  data() {
    return {
      activeTags: [],
      search: null,

      recipesInitiated: false,
    };
  },

  components: {
    RecipeListItem,
  },

  computed: {

    recipes() {
      this.recipesInitiated = true;

      const recipes = this.allRecipes.filter(r => {
        var recipeTags = r.tags.map(t => t.name);
        if (!recipeTags) return true; // if a recipe has no tags, always show
        for (let i = 0; i < this.activeTags.length; i++) {
            const tag = this.activeTags[i];
            if (!recipeTags.includes(tag)) {
              return false;
            }
          }
          return true;
      }).sort((a, b) => {
        if (a.title > b.title) {
          return 1
        } else {
          return -1
        }
      });
      // 2) Search (regex)
      if (!this.search || this.search === "") return recipes;
      var re = new RegExp(Constants.methods.replaceUnicode(this.search.toLowerCase()));
      return recipes.filter(r => {
        var match = re.exec(
          Constants.methods.replaceUnicode(r.title.toLowerCase()))
        if (match) {
          return true;
        }
        return false;
      })
    }
  },

  methods: {
    
    isInitState() {
      // a bit hack-ish :(
      return (this.recipes.length === 0) && !this.recipesInitiated;
    },

    toggleFilter(filter) {
      // filter based on tags
      if (this.activeTags.includes(filter)) {
        this.activeTags = this.activeTags.filter(t => t != filter);
      } else {
        this.activeTags.push(filter);
      }
      this.refresh();
    },

  },

};
</script>
