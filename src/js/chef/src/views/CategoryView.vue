<template>
  <div>

    <transition name="loading" mode="out-in">
    <LoadingSection v-if="loadingCategory" :loading="loadingCategory"/>
    <CategoryTile
      v-else
      :category="category"
      :editable="true"
      @categoryDeleted="$router.push({ name: 'home' })"
      @categoryEdited="edited"
    />
    </transition>

    <div v-if="errorCategory">
      <article class="message is-danger my-5">
      <div class="message-body">{{ errorCategory }}</div>
      </article>
    </div>

    <div v-else>
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="loadingRecipes" :loading="loadingRecipes"/>
    <div v-else-if="errorRecipes">
      <article class="message is-danger my-5">
      <div class="message-body">{{ errorRecipes }}</div>
      </article>
    </div>
    <div v-else class="px-2 pt-3 recipe-list">
      <RecipeList :allRecipes="recipes" />
    </div>
    </transition>
    </div>

  </div>
</template>

<script>
import RecipeList from "@/components/RecipeList.vue";
import CategoryTile from "../components/CategoryTile.vue";
import axios from "axios";
import Constants from "../components/Constants.vue";
import LoadingSection from "../components/LoadingSection.vue"

export default {
  components: { CategoryTile, RecipeList, LoadingSection},

  data() {
    return {
      category: null,
      recipes: [],
      errorCategory: null,
      loadingCategory: false,
      errorRecipes: null,
      loadingRecipes: false
    };
  },

  methods: {
    edited() {
      this.getCategory();
      this.getRecipes();
    },

    getCategory() {
      const category = `${Constants.HOST_URL}/categories/${this.$route.params.id}`;
      this.loadingCategory = true;
      axios
        .get(category)
        .then(res => (this.category = res.data))
        .catch(() => (this.errorCategory = "Category NOT found"))
        .finally(() => (this.loadingCategory = false));
      },

      getRecipes() {
        const recipes = `${Constants.HOST_URL}/recipes?category=${this.$route.params.id}`;
        this.loadingRecipes = true;
        axios
          .get(recipes)
          .then(res => (this.recipes = res.data))
          .catch(() => (this.errorRecipes = "Error occured while fetching recipes."))
          .finally(() => (this.loadingRecipes = false));
      }
  },

  created() {
    this.getCategory();
    this.getRecipes();
  }
};
</script>

<style lang="scss" scoped>
.recipe-list {
  min-height: 1800px;
}
</style>
