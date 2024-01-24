<template>
  <div class="mx-3 mb-3">
    <div ref="lookHere"></div>
    <div ref="recipeTitle" v-if="recipe">
      <div v-if="!editMode">
        <div class="level">
        <div class="level-left">
          <div v-show="!missingImage" class="level-item">
            <p class="image" style="width: 256px; height: 256px">
              <img
                ref="r-img"
                :src="image_url"
                @error="missingImage = true"
                alt="recipe image"
                class="is-rounded p-2">
            </p>
          </div>
          <div class="level-item">
            <div class="has-text-centered-mobile title-header">
              <h1 v-if="recipe" class="title is-4">#{{ recipe.id }}</h1>
              <h1 v-if="recipe" class="title is-4">{{ recipe.title }}</h1>
              <h2 v-if="recipe && recipe.subtitle">{{ recipe.subtitle }}</h2>

              <p v-if="recipe && recipe.source">
                <a :href="recipe.source">
                  <span v-if="recipe.source_name">{{ recipe.source_name }}</span>
                  <span v-else>{{ recipe.source }}</span>
                </a>
              </p>
            </div>
          </div>
        </div>
        </div>

        <!-- tags -->
        <div class="tags mt-5">
          <!-- CURR -->
          <ButtonFavorite :favorite="recipe.favorite" :loading="recipes.loading" @favorite="makeFavorite" class="mr-2"/>
          <span class="tag" v-for="(tag, index) in recipe.tags" :key="'item-tag-' + index">{{tag.name}}</span>
        </div>

        <!-- chevron -->
        <div ref="chevron" class="tabs is-right is-boxed">
          <ul>
            <li class="is-active">
              <a v-on:click="ingredientsCollapsed = !ingredientsCollapsed">
                <span :class="{
                  icon: true,
                  'is-small': true,
                  rotate: ingredientsCollapsed,
                  'animate-icon': true,
                  }"
                >
                  <i class="fas fa-chevron-down" aria-hidden="true"></i>
                </span>
              </a>
            </li>
          </ul>
        </div>

        <!-- ingredients -->
        <transition name="slide-up">
        <div v-show="!ingredientsCollapsed">
          <h1 v-if="recipe" class="title is-5">Ingredients</h1>

          <div v-if="recipe && recipe.ingredients" class="px-5">
            <div
              v-for="(ingredient, index) in recipe.ingredients" :key="ingredient.ingredient.name + index + 'recipe-detail'"
              class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                  <router-link :to="{ name: 'Ingredient', params: {id: ingredient.ingredient.id}}">
                    {{ingredient.ingredient.name}}
                    <span v-if="ingredient.note">({{ingredient.note}})</span>
                  </router-link>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <p>
                    <strong>{{ Math.round((ingredient.amount *portions/recipe.portions)*10)/10 }}</strong>
                    {{ ingredient.unit.name }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- portion counter  -->
          <div class="my-5">
            <Counter v-model="portions"></Counter>
            <label class="label">Enough for {{ Math.round((portions/recipe.portions)*10)/10 }} batch(es).</label>
          </div>

          <hr>
        </div>
        </transition>

        <!-- HTML body -->
        <div v-html="recipe.body" class="content section pt-1"/>
      </div>

      <!-- buttons -->
      <div v-if="!editMode" class="my-5 row">
        <DeleteButton @delete="deleteRecipe" v-model="deletePrompt" :loading="recipes.loading"/>
        <ImageUpload
          v-show="!deletePrompt"
          :recipe=recipe
          @uploadSuccess="$router.go($router.currentRoute)"
        />
        <button v-show="!deletePrompt" v-on:click="updateRecipe" class="button is-fullwidth is-warning mb-1">
          <i class="fas fa-pen"></i>
          <span class="ml-2">Edit</span>
        </button>
      </div>

      <div v-if="editMode">
        <RecipeForm
          :data="recipe"
          @posted="updateRecipe"
          @cancel="editMode=false"
        />
      </div>
    </div>
    <NotFound v-else message="Recipe not found" />

  </div>
</template>

<script setup lang="ts">
import Counter from "@/components/Counter.vue";
import RecipeForm from "@/components/RecipeForm.vue";
import ImageUpload from "@/components/ui/ImageUpload.vue";
import NotFound from "@/components/NotFound.vue";
import DeleteButton from "@/components/ui/DeleteButton.vue";
import ButtonFavorite from "@/components/ButtonFavorite.vue";

import { useRecipeStore } from "@/stores/recipe";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, toRefs } from "vue";
import { IMAGES_URL } from "@/constants";

const router = useRouter();
const route = useRoute();
const recipeId = parseInt(route.params.id as string);

const recipes = useRecipeStore();
const { all } = toRefs(recipes)

if (!all.value.find(r => r.id === recipeId)) {
  await recipes.fetchSingle(recipeId);
}

const recipe = computed(() => {
  return all.value.find(r => r.id === recipeId);
});
const portions = ref<number>(recipe.value?.portions ?? 4);


const editMode = ref(false);
const lookHere = ref(null)
const updateRecipe = () => {
  editMode.value = !editMode.value;
};


const deletePrompt = ref(false);
const deleteRecipe = async () => {
  recipes.deleteById(recipeId).then(() => router.push('/recipes'));
}

const makeFavorite = async () => {
  const data = {...recipe.value}
  data.favorite = !data.favorite;
  recipes.update(data);
}

const ingredientsCollapsed = ref<boolean>(false);

const missingImage = ref<boolean>(false);

const image_url = `${IMAGES_URL}/${recipeId}/medium.jpeg`;

</script>

<style lang="scss" scoped>
  .row {
    display: flex;
    gap: 3px;
  }

  .animate-icon {
    transition: 0.15s;
  }
  .rotate {
    transform:rotate(-90deg);
  }
  .title-header {
    h1, h2 {
      text-transform: uppercase;
    }
  }
  .tag {
    margin-bottom: 0%;
    padding-top: 1px;
  }
</style>
