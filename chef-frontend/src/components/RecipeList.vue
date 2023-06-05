<template>
  <div>

    <!-- RECIPE COUNT -->
    <div class="mb-2">
      <h1 class="title is-4 has-text-primary">{{ recipes.length }} {{ title || 'Recipes' }}</h1>
    </div>

    <!-- TAGS -->
    <div v-if="!hideFilters" class="tags">
      <a v-for="tag in tags" :key="'tag_key' + tag"
        v-on:click="toggleFilter(tag)"
        :class="{ 'tag':true,  'is-rounded':true, 'is-dark': activeTags.includes(tag), 'noselect': true}"
        style="text-decoration:none;"
      >{{ tag }}</a>
    </div>

    <!-- search -->
    <p v-if="!hideSearch" class="control has-icons-left mb-4">
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
    <div class="recipe-list">
      <RecipeListItem v-for="(recipe) in recipes" :key="'recipe_a_key+' + recipe.id" :recipe="recipe" />
    </div>

  </div>  
</template>

<script>
// import axios from "axios";
import RecipeListItem from "../components/RecipeListItem.vue";
import Constants from "../components/Constants.vue";

export default {
  props: ["allRecipes", "title", "hideSearch", "hideFilters"],

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

    tags() {
      return new Set(this.allRecipes.map(r => r.tags.map(t => t.name)).flat())
    },

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

    toggleFilter(filter) {
      // filter based on tags
      if (this.activeTags.includes(filter)) {
        this.activeTags = this.activeTags.filter(t => t != filter);
      } else {
        this.activeTags.push(filter);
      }
    },

  },

};
</script>
<style scoped lang="scss">
.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 0.3em;
}
</style>