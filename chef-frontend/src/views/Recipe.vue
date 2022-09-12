<template>
  <div class="mx-3">
    <div ref="look-here"></div>
    <transition name="slide-fade" mode="out-in">
    <div ref="recipeTitle" v-if="recipe">
      <div v-if="!editMode">
        <h1 v-if="recipe" class="title is-4">{{ recipe.title.toUpperCase() }}</h1>
        <h2 v-if="recipe&&recipe.subtitle" class="subtitle">{{ recipe.subtitle.toUpperCase() }}</h2>

        <p v-if="recipe&&recipe.source" class="my-4">
          <a :href="recipe.source">
            <span v-if="recipe.source_name">{{ recipe.source_name }}</span>
            <span v-else>{{ recipe.source }}</span>
          </a>
        </p>

        <nav class="level">
          <div class="level-left">
            <div class="tags my-0">
                <span class="tag" v-for="(tag, index) in recipe.tags" :key="'item-tag-' + index">{{tag.name}}</span>
            </div>
          </div>
        </nav>
        
        <!-- chevron -->
        <div ref="chevron" class="tabs is-right is-boxed">
          <ul>
            <li class="is-active">
              <a v-on:click="ingredientsCollapsed = !ingredientsCollapsed">
                <span :class="{
                  icon: true,
                  'is-small': true,
                  rotate: ingredientsCollapsed,
                  'animate-icon': true,
                  }"
                >
                  <i class="fas fa-chevron-down" aria-hidden="true"></i>
                </span>
              </a>
            </li>
          </ul>
        </div>

        <!-- ingredients -->
        <div v-if="!ingredientsCollapsed">
          <h1 v-if="recipe" class="title is-5">Ingredients</h1>

          <div v-if="recipe && recipe.ingredients" class="px-5">
            <div
              v-for="(ingredient, index) in recipe.ingredients" :key="ingredient + index + 'recipe-detail'"
              class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                  <router-link :to="{ name: 'Ingredient', params: {id: ingredient.ingredient.id}}">
                    {{ingredient.ingredient.name}}
                    <span v-if="ingredient.note">({{ingredient.note}})</span>
                  </router-link>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <p>
                    <strong>{{ Math.round((ingredient.amount *portions/recipe.portions)*10)/10 }}</strong>
                    {{ ingredient.unit.name }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- portion counter  -->
          <div class="my-5">
            <Counter :initialValue="recipe.portions" @counterUpdate="updatePortions"></Counter>
            <label class="label">Enough for {{ Math.round((portions/recipe.portions)*10)/10 }} batch(es).</label>
          </div>

          <hr>
        </div>

        <!-- Steps -->
        <h1 v-if="recipe" class="title is-5">Recipe</h1>
        <!-- HTML body -->
        <div ref="recipe-body" class="content section pt-1"/>
      </div>

      <hr>

      <!-- buttons -->
      <div v-if="!editMode" class="my-5">     
        <div class="field is-grouped">
          <p class="control mr-1">
            <button v-on:click="youSurePrompt" class="button is-fullwidth is-danger">
              <i class="fas fa-trash-alt"></i>
              <!-- <span class="ml-2">Delete</span> -->
            </button>
          </p>
          <p class="control mr-1">
            <ImageUpload :recipe=recipe></ImageUpload>
          </p>
          <p class="control is-expanded">
            <button v-on:click="updateRecipe" class="button is-fullwidth is-warning mb-1">
              <i class="fas fa-pen"></i>
              <span class="ml-2">Edit</span>
            </button>
          </p>
        </div>
      </div>


      <!-- you sure? -->
      <p v-if="deletePrompt" class="help is-danger">
        You sure you want to delete this recipe?
        <a v-on:click="deleteRecipe">Yes, absolutely!</a>
      </p>
      <div ref="yousure"/>

      <div v-if="editMode">
        <RecipeForm :recipe="recipe" @recipePosted="updateRecipe"></RecipeForm>
      </div>

      <div v-if="editMode">
        <button v-on:click="updateRecipe" class="button is-fullwidth is-danger mb-1">
          <span class="ml-2">Cancel</span>
        </button>
      </div>
    </div>

    <!-- no recipe -->
    <LoadingSection v-else-if="loading" class="p-5" :loading="loading"/>
    <NotFound v-else message="Recipe not found" />
    </transition>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";
import Counter from "@/components/Counter.vue";
import RecipeForm from "@/components/RecipeForm.vue";
import ImageUpload from "@/components/ImageUpload.vue";
import LoadingSection from "@/components/LoadingSection.vue";
import NotFound from "@/components/NotFound.vue";


export default {
  components: { Counter, RecipeForm, ImageUpload, LoadingSection, NotFound },

  data() {
    return {
      recipe: null,
      error: null,
      portions: 4,
      editMode: false,
      deletePrompt: false,
      loading: false,

      ingredientsCollapsed: false,
    }
  },

  methods: {
    updatePortions(val) {
      this.portions = val;
    },

    updateRecipe() {
      this.editMode = !this.editMode
      this.$refs["look-here"].scrollIntoView();
      this.fetchRecipe();
    },

    youSurePrompt() {
      this.deletePrompt=!this.deletePrompt;
      this.$refs['yousure'].scrollIntoView()
    },

    deleteRecipe() {
      const path = `${Constants.HOST_URL}/recipes/${this.$route.params.id}`;
      console.info(`Deleting: ${path}`);
      axios.delete(path)
        .then(() => {
          this.$router.push('/recipes');
        })
    },

    fetchRecipe() {
      this.loading = true;
      const path = `${Constants.HOST_URL}/recipes/${this.$route.params.id}`;
      console.info(`Getting: ${path}`);
      axios.get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.recipe = res.data;
              this.portions = this.recipe.portions;
              // this.$refs["recipe-body"].innerHTML = this.recipe.body;
            }
          }
        })
        .catch((err) => this.error = err)
        .finally(() => (this.loading = false));
    },
  },

  created() {
    this.fetchRecipe();
  },

  updated() {
    if (this.$refs["recipe-body"]) {
      this.$refs["recipe-body"].innerHTML = this.recipe.body;
    }
  }

};
</script>

<style>
  .animate-icon {
    transition: 0.15s;
  }
  .rotate {
    transform:rotate(-90deg);
  }
</style>
