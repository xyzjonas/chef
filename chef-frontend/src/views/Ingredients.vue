<template>
  <div>
    <!-- title -->
    <h1 class="title is-4">{{ ingredients.length }} Ingredients</h1>

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

    <div class="section px-3 pt-4">
      <IngredientListItem
        v-for="(ingredient, index) in ingredients" :key="ingredient + index + 'list'"
        :ingredient="ingredient"
        @ingredientDeleted="reload();refresh();"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Constants from "../components/Constants.vue";
import IngredientListItem from "../components/IngredientListItem.vue";

export default {
  data() {
    return {
      allIngredients: [],
      ingredients: [],
      error: null,
      search: null,
    };
  },

  components: {
    IngredientListItem
  },

  methods: {

    refresh() {
      this.ingredients = this.allIngredients;
      // search & regex
      if (!this.search || this.search === ""){
        return;
      }
      var re = new RegExp(
        Constants.methods.replaceUnicode(this.search.toLowerCase()));
      this.ingredients = this.allIngredients.filter(i => {
        var match = re.exec(Constants.methods.replaceUnicode(i.name.toLowerCase()))
        if (match) {
          return true;
        }
        return false;
      })
      
    },

    reload() {
      const path = `${Constants.HOST_URL}/ingredients`;
      axios.get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.ingredients = res.data;
              this.allIngredients = res.data;
            }
          }
        })
        .catch((err) => this.error = err);
    }
  },

  created() {
    this.reload();
  }
}
</script>

<style>

</style>