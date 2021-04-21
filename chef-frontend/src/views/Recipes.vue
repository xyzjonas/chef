<template>
  <div class="recipes">
    <RecipeList :allRecipes="recipes"/>
  </div>  
</template>

<script>
import axios from "axios";
import RecipeList from "@/components/RecipeList.vue";
import Constants from "../components/Constants.vue";

export default {
  data() {
    return {
      recipes: [],
      error: null,
    };
  },

  components: {
    RecipeList
  },

  created() {
    const path = `${Constants.HOST_URL}/recipes`;
    axios
      .get(path)
      .then(res => {
        if (res.status !== "success") {
          if (res.data) {
            this.recipes = res.data;
          } else {
            this.error = "No recipes received."
          }
        }
      })
      .catch((err) => this.error = err);
  }
};
</script>
