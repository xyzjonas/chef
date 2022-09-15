<template>
  <div class="mx-3 py-0">
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="loading" :loading="loading" />
    <div v-else class="columns">
      <div
        v-for="(row, index) in categoryRows" :key="'row' + index"
        class="column p-0"
      >
        <CategoryTile
          v-for="(category, index) in row" :key="'category' + index"
          :category="category"
          @clicked="$router.push({ name: 'category', params: { id: category.id } })"
        />
      </div>
    </div>
    </transition>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "../components/Constants.vue";
import CategoryTile from "../components/CategoryTile.vue";
import LoadingSection from "../components/LoadingSection.vue"

export default {
  components: { CategoryTile, LoadingSection },

  data() {
    return {
      error: null,

      columns: 3,
      categories: [],
      newCategory: false,
      loading: false,
    };
  },

  computed: {
    categoryRows() {
      // split all categories into three-item partitions to be displayed as tiles.
      var rows = []
      for (let index = 0; index < this.categories.length; index+=this.columns) {
        rows[rows.length] = this.categories.slice(index, index + this.columns);
      }
      return rows;
    }
  },

  methods: {
    getAllCategories() {
      this.loading = true;
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
        .catch((err) => this.error = err)
        .finally(() => (this.loading = false));
    },
  },
  created() {
    this.getAllCategories();
  }
};
</script>
