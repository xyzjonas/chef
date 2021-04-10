<template>
  <div>
    <div v-if="ingredient">
      
      <!-- error message -->
      <div v-if="error" class="level-item">
        <p class="help is-danger">{{ error }}</p>
      </div>

      <nav class="level is-mobile my-1">
        <div class="level-left">
          <div class="level-item">
            <p class="title is-5">
              {{ ingredient.name.toUpperCase() }}
            </p>
          </div>
        </div>
        <div class="level-right">
          
          <!-- delete button -->
          <div v-if="!error" class="level-item">
            <button v-on:click="deleteIngredient()" class="button has-icons is-danger">
              <span class="icon">
                <i class="fas fa-trash"/>
              </span>
            </button>
          </div>      
          <!-- edit button -->
          <div class="level-item">
            <button v-on:click="edit=!edit" class="button has-icons is-warning">
              <span class="icon">
                <i class="fas fa-pen"/>
              </span>
            </button>
          </div>

        </div>
      </nav>

      <hr>

      <!-- tags -->
      <div v-if="!edit">

        <div v-for="(value, key) in attributes" :key="key+'ingredientDetail'"
          class="level is-mobile px-5">
          <div class="level-left">
            <div class="level-item">
              <span class="tag">{{ key }}</span>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <strong>{{ value }}</strong>
            </div>
          </div>
        </div>
      </div>

      <div v-if="edit">
        <IngredientForm :ingredientProp="ingredient"
        @cancel="edit=false"
        @posted="edit=false;fetchIngredient()"
      />
      </div>
    </div>
    <div v-else>
      <NotFound/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";
import IngredientForm from "@/components/IngredientForm.vue";
import NotFound from "@/components/NotFound.vue";

export default {
  components: {
    IngredientForm,
    NotFound
  },

  data() {
    return {
      ingredient: null,
      error: null,
      edit: false,
      attributes: {},
    };
  },

  methods: {
    fetchIngredient() {
      const path = `${Constants.HOST_URL}/ingredients/${this.$route.params.id}`;
      console.info(`Getting: ${path}`);
      axios
        .get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.ingredient = res.data;
              this.attributes = {
                energy: `${this.ingredient.energy} kcal`,
                carbs: `${this.ingredient.carbs} g`,
                fats: `${this.ingredient.fats} g`,
                proteins: `${this.ingredient.proteins} g`,
                fibres: `${this.ingredient.fibres} g`,
                salt: `${this.ingredient.salt} g`,
              }
            }
          }
        })
        .catch(err => (this.error = err));
    },

    deleteIngredient() {
      const path = `${Constants.HOST_URL}/ingredients/${this.ingredient.id}`;
      console.info(`Deleting: ${path}`);
      axios.delete(path)
        .then(() => {
          this.$emit("ingredientDeleted");
        })
        .catch(err => {
          this.error = `${err.response.data}.`;
        })
    }

  },

  created() {
    this.fetchIngredient();
  }
};
</script>

<style></style>
