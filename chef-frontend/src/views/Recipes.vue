<template>
  <div class="recipes">

    <h1 class="title is-4">{{ recipes.length }} Recipes</h1>
    <!-- TAGS -->
    <div class="tags">
      <a v-for="(tag) in allTags" :key="'tag_key' + tag"
        v-on:click="toggleFilter(tag)"
        :class="{ 'tag':true,  'is-rounded':true, 'is-dark': activeTags.includes(tag), 'noselect': true}"
        style="text-decoration:none;"
      >{{ tag }}</a>
    </div>

    <!-- search -->
    <p class="control has-icons-left">
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

    <!-- sort-tabs  -->
    <div class="tabs is-toggle is-fullwidth mt-2">
      <ul>
        <li class="p-0">
          <a>
            <span class="icon m-0"><i class="fas fa-sort-alpha-up" aria-hidden="true"></i></span>
          </a>
        </li>
        <li>
          <a>
            <span class="icon m-0"><i class="fas fa-sort-alpha-down" aria-hidden="true"></i></span>
          </a>
        </li>
        <li>
          <a>
            <span class="icon m-0"><i class="fas fa-sort-numeric-up" aria-hidden="true"></i></span>
          </a>
        </li>
        <li>
          <a>
            <span class="icon m-0"><i class="fas fa-sort-numeric-down" aria-hidden="true"></i></span>
          </a>
        </li>
        <li>
          <a>
            <span class="icon"><i class="fas fa-sort-amount-up" aria-hidden="true"></i></span>
          </a>
        </li>
        <li>
          <a>
            <span class="icon m-0"><i class="fas fa-sort-amount-down" aria-hidden="true"></i></span>
          </a>
        </li>
      </ul>
    </div>

    <!-- ERROR -->
    <div v-if="error" class="notification is-danger is-light">{{ error }}</div>

    <!-- LIST -->
    <div v-for="(recipe) in recipes" :key="'recipe_key+' + recipe.id">
      <RecipeListItem :recipe="recipe"/>
    </div>

  </div>  
</template>

<script>
import axios from "axios";
import RecipeListItem from "../components/RecipeListItem.vue";
import Constants from "../components/Constants.vue";

export default {
  data() {
    return {
      allRecipes: [],
      recipes: [],
      allTags: ["chicken", "pasta", "soup"],
      activeTags: [],
      error: null,

      search: null,
    };
  },

  components: {
    RecipeListItem,
  },

  methods: {
    
    toggleFilter(filter) {
      // filter based on tags
      if (this.activeTags.includes(filter)) {
        this.activeTags = this.activeTags.filter(t => t != filter);
      } else {
        this.activeTags.push(filter);
      }
      this.refresh();
    },

    refresh() {
      // refresh list of displayed recipes based on tag filters and search input
      // 1) tags
      this.recipes = this.allRecipes.filter(r => {
        var recipeTags = r.tags.map(t => t.name);
        if (!recipeTags) return true; // if a recipe has no tags, always show
        for (let i = 0; i < this.activeTags.length; i++) {
          const tag = this.activeTags[i];
          if (!recipeTags.includes(tag)) {
            return false;
          }
        }
        return true;
      });
      // 2) search & regex
      if (!this.search || this.search === "") return;
      var re = new RegExp(
        Constants.methods.replaceUnicode(this.search.toLowerCase()));

      this.recipes = this.recipes.filter(r => {
        var match = re.exec(
          Constants.methods.replaceUnicode(r.title.toLowerCase()))
        if (match) {
          return true;
        }
        return false;
      })
    },
  },

  created() {
    const path = `${Constants.HOST_URL}/recipes`;
    axios.get(path)
      .then(res => {
        if (res.status !== "success") {
          if (res.data) {
            this.recipes = res.data;
            this.allRecipes = res.data;
            // use existing recipes to show possible tags to filter
            this.allTags = new Set(this.allRecipes.map(r => r.tags.map(t => t.name)).flat())
          }
        }
      })
      .catch((err) => this.error = err);
  }
};
</script>
