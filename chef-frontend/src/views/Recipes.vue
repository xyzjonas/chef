<template>
  <div class="recipes px-3">
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="loading" :loading="loading" />
    <RecipeList v-else :allRecipes="recipes"/>
    </transition>
  </div>  
</template>

<script>
import axios from "axios";
import RecipeList from "@/components/RecipeList.vue";
import Constants from "../components/Constants.vue";
import LoadingSection from "../components/LoadingSection.vue"

export default {
  data() {
    return {
      recipes: [],
      loading: false,
      error: null,
    };
  },

  components: { RecipeList, LoadingSection },

  created() {
    this.loading = true;
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
      .catch((err) => this.error = err)
      .finally(() => (this.loading = false));
  }
};
</script>
