<template>
  <div ref="recipeTitle" v-if="recipe">
    <div v-if="editMode">
      <h1 id="edit-title">Edit recipe</h1>
      <RecipeForm
        :data="recipe"
        @posted="updateRecipe"
        @cancel="editMode = false"
      />
    </div>
    <div v-else class="recipe">
      <div class="row heading">
        <img
          v-if="recipe.detail_image"
          ref="r-img"
          :src="image_url"
          @error="missingImage = true"
          alt="recipe image"
        />
        <img v-else src="@/assets/notfound.jpg" alt="no image" />
        <div class="heading-right">
          <div class="titles">
            <div class="row">
              <h1 v-if="recipe" class="title is-4">{{ recipe.title }}</h1>
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
            <pin
              v-for="(tag, index) in recipe.tags"
              :key="tag.name"
              :text="tag.name"
              active
            />
          </div>

          <div class="row tags">
            <ImageUpload type="thumbnail" :recipe="recipe" />
            <ImageUpload
              type="detail"
              :recipe="recipe"
              @uploadSuccess="imageUploaded"
            />
          </div>
        </div>
      </div>

      <!-- ingredients -->
      <section class="ingredient-card">
        <div class="row">
          <ui-button
            :icon="
              ingredientsCollapsed ? 'fas fa-chevron-down' : 'fas fa-chevron-up'
            "
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
                  :class="
                    ingredient.ingredient.name.endsWith('--') ? 'hide' : ''
                  "
                >
                  <td class="amount">
                    <h1>
                      {{
                        Math.round(
                          ((ingredient.amount * portions) / recipe.portions) *
                            10
                        ) / 10
                      }}
                    </h1>
                    <small>{{
                      ingredient.unit.name.replace("pcs", "ks")
                    }}</small>
                  </td>
                  <td class="ingredient-link">
                    <router-link
                      :to="{
                        name: 'Ingredient',
                        params: { id: ingredient.ingredient.id },
                      }"
                    >
                      {{ ingredient.ingredient.name }}
                      <span v-if="ingredient.note"
                        >({{ ingredient.note }})</span
                      >
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
        <ui-button @click="updateRecipe" text="edit" icon="fas fa-pen" />
      </div>

      <!-- HTML body -->
      <section class="content" v-if="recipe.body">
        <div v-html="recipe.body" />
      </section>
      <section v-else id="empty">
        <empty-box
          title="Good Heavens!"
          subtitle="It seems the recipe remains a&nbsp;blank canvas. Jolly&nbsp;shame&nbsp;on&nbsp;us!&nbsp;🍴"
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
import { IMAGES_HOST } from "@/constants";

const router = useRouter();
const route = useRoute();
const recipeId = parseInt(route.params.id as string);

import { useEventBus } from "@vueuse/core";
import type { ChefNotification, Recipe } from "@/types";

const responseBusId = `delete-recipe-${recipeId}`;
const bus = useEventBus<ChefNotification>("notifications");
const responseBus = useEventBus<string>(responseBusId);

const recipes = useRecipeStore();
const { all } = toRefs(recipes);

if (!all.value.find((r) => r.id === recipeId)) {
  await recipes.fetchSingle(recipeId);
}

const recipe = computed(() => {
  const match = all.value.find((r) => r.id === recipeId);
  if (!match) {
    throw Error("This should never happen");
  }
  return match;
});
const portions = ref<number>(recipe.value?.portions ?? 4);

const editMode = ref(false);
const updateRecipe = () => {
  editMode.value = !editMode.value;
};

const ingredientsCollapsed = ref<boolean>(false);

const missingImage = ref<boolean>(false);

const image_url = computed(() => `${IMAGES_HOST}${recipe.value?.detail_image}`);

const clickDelete = () =>
  bus.emit({
    level: "ERROR",
    message: `Delete recipe ${recipe.value?.title ?? "N/A"} ?`,
    action: {
      id: responseBusId,
      label: "Delete",
    },
  });

const onDeleteConfirmListener = () => {
  recipes.deleteById(recipeId).then(() => router.push("/recipes"));
};

responseBus.on(onDeleteConfirmListener);

const imageUploaded = async (newRecipe: Recipe) => {
  console.info(newRecipe);
  recipe.value.detail_image = newRecipe.detail_image;
};
</script>

<style lang="scss" scoped>
.recipe {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.content,
.ingredient-card {
  border: 1px solid var(--bg-200);
  border-radius: 0.3rem;
  padding: 0.3rem;
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
  gap: 0.5rem;
  align-items: center;
}

.animate-icon {
  transition: 0.15s;
}
.rotate {
  transform: rotate(-90deg);
}
.title-header {
  h1,
  h2 {
    text-transform: uppercase;
  }
}
.tag {
  margin-bottom: 0%;
  padding-top: 1px;
}

td {
  padding-block: 0.4rem;
  min-width: 6rem;
}

tr {
  & > .amount {
    display: flex;
    align-items: center;
    text-align: right;
    gap: 0.3rem;
    // width: 5rem;
    // border-bottom: 1px solid gray;

    & > h1 {
      font-size: x-large;
      font-weight: 400;
    }
  }

  &:nth-child(even) > .amount {
    color: var(--primary);
  }

  &:nth-child(odd) > .amount {
    color: var(--text);
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
  display: flex;
  flex-direction: column;
  min-height: 50dvh;
}

img {
  width: 20dvh;
  aspect-ratio: 1;
  border-radius: 50%;
  mask-image: radial-gradient(rgb(0 0 0 / 100%) 50%, transparent);
  object-fit: cover;
}

.heading {
  gap: 3rem;
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
    z-index: -1000;
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
  filter: opacity(0.8);
}

#recipe-link {
  margin-bottom: 2rem;
}

#recipe-link > a {
  color: var(--primary);
}

.heading-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
