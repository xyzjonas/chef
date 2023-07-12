<template>
  <div>

    <!-- name -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="ingredient.name"
          class="input"
          type="text"
          placeholder="name"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-font"></i>
        </span>
      </div>
    </div>

    <!-- energy -->
    <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.energy)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model.number="ingredient.energy"
          type="number"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.energy)),
          }"
          placeholder="energy"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-charging-station"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">kcal / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.energy))" class="help is-danger mt-0">Must be a number...</p>


    <!-- carbs -->
    <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.carbs)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model="ingredient.carbs"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.carbs)),
          }"
          placeholder="carbs"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-pizza-slice"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">g / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.carbs))" class="help is-danger mt-0">Must be a number...</p>

    <!-- fats -->
   <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.fats)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model="ingredient.fats"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.fats)),
          }"
          placeholder="fats"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-bacon"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">g / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.fats))" class="help is-danger mt-0">Must be a number...</p>


    <!-- proteins -->
   <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.proteins)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model="ingredient.proteins"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.proteins)),
          }"
          placeholder="proteins"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-drumstick-bite"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">g / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.proteins))" class="help is-danger mt-0">Must be a number...</p>

    <!-- fibres -->
   <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.fibres)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model="ingredient.fibres"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.fibres)),
          }"
          placeholder="fibres"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-seedling"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">g / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.fibres))" class="help is-danger mt-0">Must be a number...</p>

    <!-- salt -->
   <div :class="{
      field: true,
      'has-addons': true,
      'mb-0': isNaN(parseFloat(ingredient.salt)),
    }">
      <div class="control has-icons-left is-expanded">
        <input
          v-model="ingredient.salt"
          :class="{
            input: true,
            'is-danger': isNaN(parseFloat(ingredient.salt)),
          }"
          placeholder="salt"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-hand-spock"></i>
        </span>
      </div>
      <p class="control">
        <a class="button is-static">g / 100g</a>
      </p>
    </div>
    <p v-if="isNaN(parseFloat(ingredient.salt))" class="help is-danger mt-0">Must be a number...</p>

    <!-- error -->
    <article  v-if="postError" class="message is-danger">
      <div class="message-body">
        {{ postError }}
      </div>
    </article>

    <!-- buttons -->
    <div class="field has-addons">
      <p class="control is-expanded">
        <a v-on:click="save" class="button is-fullwidth is-success">
          <i class="fas fa-save"></i>
          <span class="ml-2">Save</span>
        </a>
      </p>
      <p class="control is-expanded">
        <a v-on:click="cancel" class="button is-fullwidth is-danger">
          <i class="fas fa-times"></i>
          <span class="ml-2">Cancel</span>
        </a>
      </p>
    </div>

  </div>
</template>

<script setup lang="ts">
import { useIngredientStore } from '@/stores/ingredient';
import type { Ingredient } from '@/types';
import { deepCopy } from '@/utils';
import { ref } from 'vue';

const ingredients = useIngredientStore();

const props = defineProps<{
  ingredientProp: Ingredient | undefined;
}>();

const ingredient = ref();
if (props.ingredientProp) {
  ingredient.value = deepCopy(props.ingredientProp);
}
    
const emit = defineEmits(["cancel", "posted"]);
const cancel = () => emit("cancel");
const save = () => {
  ingredients.update(ingredient.value).then(() => emit("posted", ingredient));
}
</script>

<style>

</style>