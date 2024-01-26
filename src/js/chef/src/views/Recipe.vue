<template>
    <div ref="recipeTitle" v-if="recipe">
      <div v-if="editMode">
        <h1 id="edit-title">Edit recipe</h1>
        <RecipeForm
          :data="recipe"
          @posted="updateRecipe"
          @cancel="editMode=false"
        />
      </div>
      <div v-else class="recipe">
        <div class="row heading">
          <img
              ref="r-img"
              :src="image_url"
              @error="missingImage = true"
              alt="recipe image"
              class="is-rounded p-2"
          >
          <div>
            <div class="titles">
              <div class="row">
                <h1 v-if="recipe" class="title is-4">{{ recipe.title }}</h1>
                <!-- <ButtonFavorite :favorite="recipe.favorite" :loading="recipes.loading" @favorite="makeFavorite" class="mr-2"/> -->
              </div>
              <div>
                <h2 v-if="recipe && recipe.subtitle">{{ recipe.subtitle }}</h2>
              </div>
            </div>
            <div id="recipe-link">
              <a v-if="recipe && recipe.source" :href="recipe.source">
                <span v-if="recipe.source_name">{{ recipe.source_name }}</span>
                <span v-else>{{ recipe.source }}</span>
              </a>
            </div>

            <div class="tags">
              <pin v-for="(tag, index) in recipe.tags" :key="tag.name"  :text="tag.name"  active />
            </div>
          </div>
        </div>

        <!-- ingredients -->
        <section class="ingredient-card">
          <div class="row">
            <ui-button
              :icon="ingredientsCollapsed ? 'fas fa-chevron-down' : 'fas fa-chevron-up'"
              type="secondary"
              @click="ingredientsCollapsed = !ingredientsCollapsed"
            />
            <h2 class="title is-5">Ingredients</h2>
          </div>

          <transition name="slide-up">
          <div v-show="!ingredientsCollapsed" class="ingredients">
            <table>
              <tbody>
                <tr
                  v-for="(ingredient, index) in recipe.ingredients"
                  :key="ingredient.ingredient.id"
                  :class="ingredient.ingredient.name.endsWith('--') ? 'hide' : ''"
                >                  
                  <td class="amount">
                    <h1>{{ Math.round((ingredient.amount *portions/recipe.portions)*10)/10 }}</h1>
                    <small>{{ ingredient.unit.name.replace('pcs', 'ks') }}</small>
                  </td>
                  <td class="ingredient-link">
                    <router-link :to="{ name: 'Ingredient', params: {id: ingredient.ingredient.id}}">
                      {{ingredient.ingredient.name}}
                      <span v-if="ingredient.note">({{ingredient.note}})</span>
                    </router-link>
                  </td>
              </tr>
            </tbody>
          </table>
            
          </div>
          </transition>
        </section>
        
        <!-- buttons -->
        <div v-if="!editMode" class="row">
          <ui-button @click="clickDelete" id="delete-btn" icon="fas fa-trash" />
          <!-- portion counter  -->
          <transition>
            <div v-if="!ingredientsCollapsed">
              <Counter v-model="portions"></Counter>
            </div>
          </transition>
          <ImageUpload
            v-show="!deletePrompt"
            :recipe=recipe
            @uploadSuccess="$router.go($router.currentRoute)"
          />
          <ui-button v-show="!deletePrompt" @click="updateRecipe" text="edit" icon="fas fa-pen" />
        </div>

        <!-- HTML body -->
        <section class="content" v-if="recipe.body">
          <h2>Steps</h2>
          <div v-html="recipe.body"/>
        </section>
        <section v-else id="empty">
          <empty-box
            title="Good Heavens!"
            subtitle="It seems the recipe remains a blank canvas. Jolly Shame on&nbsp;Us! 🍴"
          />
        </section>
      </div>


 
    </div>
    <section v-else id="not-found">
      <NotFound msg="The recipe seems to have jolly well disappeared" />
    </section>
</template>

<script setup lang="ts">
import Pin from "@/components/ui/Pin.vue";
import UiButton from "@/components/ui/UiButton.vue";
import EmptyBox from "@/components/ui/EmptyBox.vue";
import Counter from "@/components/Counter.vue";
import RecipeForm from "@/components/RecipeForm.vue";
import ImageUpload from "@/components/ui/ImageUpload.vue";
import NotFound from "@/components/NotFound.vue";

import { useRecipeStore } from "@/stores/recipe";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, toRefs } from "vue";
import { IMAGES_URL } from "@/constants";

const router = useRouter();
const route = useRoute();
const recipeId = parseInt(route.params.id as string);

import { useEventBus } from "@vueuse/core"
import type { Notification } from "@/types";

const responseBusId = `delete-recipe-${recipeId}`
const bus = useEventBus<Notification>("notifications")
const responseBus = useEventBus<string>(responseBusId)

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

// const makeFavorite = async () => {
//   const data = {...recipe.value}
//   data.favorite = !data.favorite;
//   recipes.update(data);
// }

const ingredientsCollapsed = ref<boolean>(false);

const missingImage = ref<boolean>(false);

const image_url = `${IMAGES_URL}/${recipeId}/medium.jpeg`;

const clickDelete = () => bus.emit({
  level: "ERROR",
  message: `Delete recipe ${recipe.value?.title ?? 'N/A'} ?`,
  action: {
    id: responseBusId,
    label: "Delete",
  },
})

const onDeleteConfirmListener = () => {
  recipes.deleteById(recipeId).then(() => router.push('/recipes'));
}

responseBus.on(onDeleteConfirmListener);

</script>

<style lang="scss" scoped>
.recipe {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.content, .ingredient-card {
  border: 1px solid var(--bg-200);
  border-radius: .3rem;
  padding: .3rem;
}

h1 {
 font-weight: 100;
 text-transform: uppercase;
 margin: 0;
}

h2 {
  font-weight: 400;
  font-size: large;
  text-transform: uppercase;
  margin: 0;
}
.row {
  display: flex;
  gap: .5rem;
  align-items: center;
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

td {
  padding-block: .4rem;
  min-width: 6rem;
}

tr {
  & > .amount {
      display: flex;
      align-items: center;
      text-align: right;
      gap: .3rem;
      // width: 5rem;
      // border-bottom: 1px solid gray;

      & > h1 {
        font-size: x-large;
        font-weight: 400;
      }
    }

  &:nth-child(even) > .amount {
    color: var(--primary)
  }

  &:nth-child(odd) > .amount {
    color: var(--text)
  }

  &:nth-child(even) > td > a {
    color: var(--primary);
    text-decoration: none;
  }

  &:nth-child(odd) > td > a {
    color: var(--text);
    text-decoration: none;
  }
}

.hide {
  visibility: hidden;
}

#empty {
  height: 50dvh;
}

#not-found {
  height: 70dvh;
}

img {
  width: 20dvh;
  border-radius: 50%;
  mask-image: radial-gradient(rgb(0 0 0 / 100%) 50%, transparent);
}

.heading {
  gap: 3rem;
}

.tags {
  margin-top: .5rem;
}


@media (max-width: 575.98px) {

  #empty {
    height: 40dvh;
  }

  .tags {
    align-items: center;
    justify-content: center;
  }

  .heading {
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
  }

  img {
    width: 100dvw;
    border-radius: 0;
    margin-top: -1rem;
    mask-image: linear-gradient(rgb(0 0 0 / 100%) 60%, transparent);
  }

  #recipe-link {
    text-align: center;
  }

  .titles > div {
    text-align: center;
  }
}  

#delete-btn {
  margin-right: auto;
}

#edit-title {
  margin-bottom: 1rem;
  text-transform: none;
}

a:hover {
  filter: opacity(.8);
}


#recipe-link {
  margin-bottom: 2rem;
}

#recipe-link > a {
  color: var(--primary);
}

</style>
