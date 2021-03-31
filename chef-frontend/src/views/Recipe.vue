<template>
  <div>
    <h1 v-if="recipe" class="title is-4">{{ recipe.title.toUpperCase() }}</h1>
    <h2 v-if="recipe&&recipe.subtitle" class="subtitle">{{ recipe.subtitle.toUpperCase() }}</h2>

    <p v-if="recipe&&recipe.source">
      <a :href="recipe.source">
        <span v-if="recipe.source_name">{{ recipe.source_name }}</span>
        <span v-else>{{ recipe.source }}</span>
      </a>
    </p>

    <hr>
    
    <h1 v-if="recipe" class="title is-5">Ingredients</h1>

    <div v-if="recipe && recipe.ingredients">
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

      <!-- portion counter  -->
      <counter @counterUpdate="updatePortions" />
    </div>

    <hr>

    <!-- <h1 v-if="recipe" class="title is-5">Postup</h1> -->
    <!-- HTML body -->
    <div ref="recipe-body" class="content section"/>

    <hr>

    <div class="my-5 section">
      <button v-on:click="updateRecipe" class="button is-fullwidth is-warning mb-1">
        <i class="fas fa-pen"></i>
        <span class="ml-2">update</span>
      </button>
      <button v-on:click="deleteRecipe" class="button is-fullwidth is-danger">
        <i class="fas fa-trash-alt"></i>
        <span class="ml-2">Delete</span>
      </button>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";
import Counter from "@/components/Counter.vue";

export default {
  components: {
    Counter,
  },

  data() {
    return {
      recipe: null,
      error: null,
      portions: 4,
    }
  },

  methods: {
    updatePortions(val) {
      this.portions = val;
    },

    updateRecipe() {
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
              this.$refs["recipe-body"].innerHTML = this.recipe.body;
            }
          }
        })
        .catch((err) => this.error = err);
    },
  },

  created() {
    this.fetchRecipe();
  },

  mounted() {
    if (!this.recipe) {
      this.fetchRecipe();
    }
  }

};
</script>
