<template>
  <div>
    
  <h1 class="title is-3">Add</h1>
  <h2 class="subtitle is-5">...a new recipe</h2>

    <RecipeForm :recipe="recipe" @recipePosted="route"></RecipeForm>
    
  </div>
</template>

<script>
import RecipeForm from "@/components/RecipeForm.vue";

export default {
  components: {
    RecipeForm,
  },
  data() {
    return {
      recipe: {
        portions: 4,
        ingredients: [],
        tags: [],
        body: ""
      },
    };
  },
  methods: {
    route() {
      this.$router.push("/recipes");
    }
  }
};
</script>
