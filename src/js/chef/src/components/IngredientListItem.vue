<template>
<div class="box m-0 my-1 p-4">

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
      <div class="level-item">
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

  <!-- tags -->
  <nav v-if="!edit" class="level mt-3 mb-0 py-0">
    <div class="level-left">
      <div class="tags my-0">
          <span class="tag">energy: <strong>{{ingredient.energy}} kcal</strong></span>
          <span class="tag">carbs: <strong>{{ingredient.carbs}} g</strong></span>
          <span class="tag">fats: <strong>{{ingredient.fats}} g</strong></span>
          <span class="tag">protein: <strong>{{ingredient.proteins}} g</strong></span>
          <span class="tag">fibers: <strong>{{ingredient.fibres}} g</strong></span>
          <span class="tag">salt: <strong>{{ingredient.salt}} g</strong></span>
      </div>
    </div>
  </nav>

  <!-- error message -->
  <!-- <div v-if="error" class="level-item">
    <p class="help is-danger">{{ error }}</p>
  </div> -->

  <div v-if="edit">
    <hr>
    <IngredientForm :ingredientProp="ingredient"
    @cancel="edit=false"
    @posted="posted"
  />
  </div>

</div>
</template>

<script setup lang="ts">
import IngredientForm from "@/components/IngredientForm.vue";
import { useIngredientStore } from "@/stores/ingredient";
import { ref } from "vue";

const ingredients = useIngredientStore();

const props = defineProps(["ingredient"]);
const edit = ref(false);
    
const posted = () => {
  // ingredient = ing;
  edit.value = false;
}

const emit = defineEmits(["ingredientDeleted"]);
const deleteIngredient = () => {
  ingredients.deleteById(props.ingredient.id).then(() => emit("ingredientDeleted"));
}
</script>

<style>

</style>