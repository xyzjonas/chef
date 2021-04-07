<template>
  <div>
    <div ref="look-here"></div>
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
                  <p>{{ingredient.ingredient.name}}
                    <span v-if="ingredient.note">({{ingredient.note}})</span>
                  </p>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <p><strong>{{ ingredient.amount *portions/4 }}</strong> {{ ingredient.unit }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- portion counter  -->
          <div class="my-5">
            <Counter @counterUpdate="updatePortions"></Counter>
          </div>
        </div>


        <!-- <h1 v-if="recipe" class="title is-5">Postup</h1> -->
        <!-- HTML body -->
        <div ref="recipe-body" class="content section pt-1"/>
      </div>

      <hr>

      <div v-if="!editMode" class="my-5 animate-icon">
        <button v-on:click="updateRecipe" class="button is-fullwidth is-warning mb-1">
          <i class="fas fa-pen"></i>
          <span class="ml-2">update</span>
        </button>
        <button v-on:click="deleteRecipe" class="button is-fullwidth is-danger">
          <i class="fas fa-trash-alt"></i>
          <span class="ml-2">Delete</span>
        </button>
      </div>

      <div v-if="editMode">
        <RecipeForm :recipe="recipe" @recipePosted="updateRecipe"></RecipeForm>
      </div>

      <div v-if="editMode">
        <button v-on:click="updateRecipe" class="button is-fullwidth is-warning mb-1">
          <span class="ml-2">Cancel</span>
        </button>
      </div>
    </div>
    
    <!-- no recipe -->
    <div v-else class="p-5">
      <section class="section is-medium has-text-centered">
        <h1 class="title">Oooops...</h1>
        <h2 class="subtitle">
          404 recipe <strong>not</strong> found
        </h2>
        <span class="icon is-large">
          <i class="fas fa-2x fa-dizzy"></i>
        </span>
      </section>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";
import Counter from "@/components/Counter.vue";
import RecipeForm from "@/components/RecipeForm.vue";

export default {
  components: {
    Counter,
    RecipeForm,
  },

  data() {
    return {
      recipe: null,
      error: null,
      portions: 4,
      editMode: false,

      ingredientsCollapsed: true,
    }
  },

  methods: {
    updatePortions(val) {
      this.portions = val;
    },

    updateRecipe() {
      this.editMode = !this.editMode
      this.$refs["look-here"].scrollIntoView();

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
      const path = `${Constants.HOST_URL}/recipes/${this.$route.params.id}`;
      console.info(`Getting: ${path}`);
      axios.get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.recipe = res.data;
              // this.$refs["recipe-body"].innerHTML = this.recipe.body;
            }
          }
        })
        .catch((err) => this.error = err);
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
    transition: 0.4s;
  }
  .rotate {
    transform:rotate(-90deg);
  }
</style>
