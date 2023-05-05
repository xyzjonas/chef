<template>
  <div>
    <transition name="loading" mode="out-in">
    <LoadingSection v-if="loading" :loading="loading" />
    <div v-else class="category-tiles">
      <CategoryTile
          v-for="category in categories" :category="category"
          @clicked="$router.push({ name: 'category', params: { id: category.id } })"
        />
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

<style lang="scss" scoped>
.category-tiles {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.3em;
}

@media only screen and (max-width: 900px) {
  .category-tiles {
    grid-template-columns: 1fr 1fr;
  }
}

@media only screen and (max-width: 600px) {
  .category-tiles {
    grid-template-columns: 1fr;
  }
}

</style>
