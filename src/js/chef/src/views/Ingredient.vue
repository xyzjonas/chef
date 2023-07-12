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

<script setup lang="ts">
import IngredientForm from "@/components/IngredientForm.vue";
import NotFound from "@/components/NotFound.vue";
import { useIngredientStore } from "@/stores/ingredient";
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

const ingredientId = parseInt(useRoute().params.id);

const ingredients = useIngredientStore();

if (!ingredients.all.find(ing => ing.id === ingredientId)) {
  ingredients.fetchSingle(ingredientId);
}

const ingredient = computed(() => {
  return ingredients.all.find(r => r.id === ingredientId);
});


const edit = ref(false);
const attributes = ref({})

const emit = defineEmits(["ingredientDeleted"])
const deleteIngredient = () => {
  ingredients.deleteById(ingredientId).then(() => emit("ingredientDeleted"));
}
</script>

<style></style>
