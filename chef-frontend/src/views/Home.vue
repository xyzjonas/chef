<template>
  <div class="home">
    <!-- SELECTED TILE -->
    <div v-if="selectedCategory">
      <div class="tile is-ancestor mb-0">
        <CategoryTile
          :category="selectedCategory" :editable="true"
          @categoryDeleted="selectedCategory=null;getAllCategories()"
          @categoryEdited="refresh()"
        />
      </div>
      <div>
        <div class="level">
          <div class="level-item level-right">
            <button
              v-on:click="deselectCategory()"
              class="button is-small"
              style="width: 8em"
            >
              <i class="fas fa-arrow-left"></i>
            </button>
          </div>
        </div>
      </div>
      <hr class="my-2">
    </div>

    <!-- TILES -->
    <div v-else>
      <div
        v-for="(row, index) in getCategoryRows()" :key="'row' + index"
        class="tile is-ancestor"
      >
        <CategoryTile
          v-for="(category, index) in row" :key="'category' + index"
          :category="category"
          @clicked="selectCategory"
        />
      </div>
      
      <!-- ADD CATEGORY -->
      <div v-if="edit">
        <!-- form -->
        <div class="level mb-1">
          <div class="level-item level-right">
            <a v-on:click="edit=!edit" class="tag is-delete"></a>
          </div>
        </div>
        <CategoryForm
          :category="newCategory"
          @categoryPosted="edit=false;getAllCategories()"
        />
      </div>
      <!-- button -->
      <button
        v-else
        v-on:click="edit = !edit"
        class="button is-success is-small is-fullwidth is-outlined"
      >
        <i class="fas fa-plus"></i>
      </button>
    </div>

    <!-- RECIPE LIST - IF A CATEGORY IS SELECTED -->
    <div v-if="selectedCategory">
      <RecipeList :allRecipes="recipes"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RecipeList from "@/components/RecipeList.vue";
import Constants from "../components/Constants.vue";
import CategoryTile from "../components/CategoryTile.vue";
import CategoryForm from "../components/CategoryForm.vue";

export default {
  components: {
    RecipeList,
    CategoryTile,
    CategoryForm,
  },

  data() {
    return {
      collapsed: true,
      allRecipes: [],
      recipes: [],
      error: null,

      edit: false,
      newCategory: {
        tags: [],
      },

      selectedCategory: null,
      columns: 3,
      categories: [
        // {
        //   name: "Pasta",
        //   background_url: 'https://images.creativemarket.com/0.1.0/ps/213318/1360/906/m1/fpnw/wm1/bsltxic97ggsaxa6wh5m94bcpk5murm8hbyqvmy9472gydwetnjqnyyds86hw9xx-.jpg?1413876159&s=6c845345eba4f615819502a140a4ebe4',
        //   tags: [
        //     {name: "pasta"}, {name: "Marcela"}
        //   ],
        // },
        // {
        //   name: "Food",
        //   background_url: 'https://cache.desktopnexus.com/thumbseg/2450/2450621-bigthumbnail.jpg',
        //   tags: [
        //     {name: "madeup"}, {name: "Marcela"}, {name: "pasta"},
        //   ],
        // },
        // {
        //   name: "Soups",
        //   background_url: 'https://marketresearchbiz-ikwnsbmbizhvmufcjx.netdna-ssl.com/wp-content/uploads/2018/08/organic-soups-market.jpg',
        //   tags: [
        //     {name: "soup"}
        //   ],
        // },
        // {
        //   name: "Czech",
        //   background_url: 'https://ak8.picdn.net/shutterstock/videos/14799118/thumb/1.jpg',
        //   tags: [
        //     {name: "czech"}
        //   ],
        // },
        // {
        //   name: "Italian",
        //   background_url: 'https://guywebsterconsulting.com/wp-content/uploads/2019/01/italian-flag-768x512.jpg',
        //   tags: [
        //     {name: "italian"}
        //   ],
        // },
      ],
    };
  },

  methods: {

    getCategoryRows() {
      // split all categories into three-item partitions to be displayed as tiles.
      var rows = []
      for (let index = 0; index < this.categories.length; index+=this.columns) {
        rows[rows.length] = this.categories.slice(index, index + this.columns);
      }
      return rows;
    },

    refresh() {
      let category = this.selectedCategory;
      this.recipes = this.allRecipes.filter(r => {
        var recipeTags = r.tags.map(t => t.name);
        if (!recipeTags) return true; // if a recipe has no tags, always show
        for (let i = 0; i < category.tags.length; i++) {
          const tag = category.tags[i];
          if (!recipeTags.includes(tag.name)) {
            return false;
          }
        }
        return true;
      });
    },

    selectCategoryByName(categoryName) {
      let cats = this.categories.filter(c => c.name.toLowerCase() == categoryName.toLowerCase())
      if (cats.length > 0) {
        this.selectedCategory = cats[0];
      }
      this.refresh();
    },

    selectCategory(category) {
      // Select category to display filtered recipes.
      this.selectedCategory = category;
      this.refresh();
    },

    deselectCategory() {
      // Return back to all tiles view.
      this.selectedCategory = null;
    },

    getAllCategories() {
      const path = `${Constants.HOST_URL}/categories`;
      axios
        .get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.categories = res.data;

              // select category if url query
              if (this.$route.query.category) {
                this.selectCategoryByName(this.$route.query.category)
              }

            } else {
              this.error = "No categories received.";
            }
          }
        })
        .catch((err) => this.error = err);
    },

    getAllRecipes() {
      const path = `${Constants.HOST_URL}/recipes`;
      axios
        .get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.allRecipes = res.data;
              this.refresh();
            } else {
              this.error = "No recipes received.";
            }
          }
        })
        .catch((err) => this.error = err);
      }

  },
  // "categoryPosted"
  created() {
    this.getAllRecipes();
    this.getAllCategories();
  }
};
</script>
