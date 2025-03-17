<template>
  <div class="wrapper">
    <!-- RECIPE COUNT -->
    <div v-if="allRecipes.length > 0" class="flex justify-between items-center">
      <h4 class="my-1 uppercase">
        {{ displayedRecipes.length }}
        {{ title || `Recipe${displayedRecipes.length === 1 ? "" : "s"}` }}
      </h4>
      <transition>
        <span class="text-primary" v-if="loading">
          <q-spinner />
          <span class="ml-2">Loading...</span>
        </span>
      </transition>
    </div>

    <!-- TAGS -->
    <div v-if="!hideFilters" class="tags">
      <pin
        v-for="tag in tagNames"
        :text="tag"
        :active="activeTags.includes(tag)"
        clickable
        @click="toggleFilter(tag)"
      />
    </div>

    <!-- SEARCH -->
    <ui-input
      v-if="allRecipes.length > 0"
      v-model="search"
      icon-before="search"
      placeholder="Search"
      style="margin-block: 0.8rem"
    />

    <!-- LIST -->
    <div class="recipe-list" v-if="displayedRecipes.length > 0">
      <recipe-grid-item
        :recipe="recipe"
        v-for="recipe in displayedRecipes"
        :key="'recipe_a_key+' + recipe.id"
      />
    </div>
    <div v-else class="empty-box">
      <empty-box
        link-text="Add a new recipe"
        route-name="new"
        :title="
          allRecipes.length === 0 ? 'No recipes created yet' : 'no matches'
        "
        :subtitle="
          allRecipes.length === 0
            ? ' Start by adding a new recipe.'
            : 'no recipes match the search criteria'
        "
        :icon="allRecipes.length === 0 ? Rocket : Search"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import EmptyBox from "@/components/ui/EmptyBox.vue";
import Pin from "@/components/ui/Pin.vue";
import type { Recipe } from "@/types";
import { replaceUnicode } from "@/utils";
import { computed, ref } from "vue";
import RecipeGridItem from "@/components/recipe/RecipeGridItem.vue";
import UiInput from "@/components/ui/UiInput.vue";
import Search from "@/components/icons/Search.vue";
import Rocket from "@/components/icons/Rocket.vue";
import { useLocalStorage } from "@vueuse/core";

const props = defineProps<{
  storageId: string;
  allRecipes: Recipe[];
  title?: string;
  hideSearch?: boolean;
  hideFilters?: boolean;
  loading?: boolean;
}>();
const activeTags = ref<string[]>([]);
const search = ref("");

const tagNames = computed<string[]>(() => {
  return [
    ...new Set(
      props.allRecipes
        .map((recipe) => recipe.tags.map((tag) => tag.name))
        .flat()
    ),
  ];
});

const displayedRecipes = computed<Recipe[]>(() => {
  const recipes = props.allRecipes
    .filter((r) => {
      var recipeTags = r.tags.map((t) => t.name);
      if (!recipeTags) return true; // if a recipe has no tags, always show
      for (let i = 0; i < activeTags.value.length; i++) {
        const tag = activeTags.value[i];
        if (!recipeTags.includes(tag)) {
          return false;
        }
      }
      return true;
    })
    .sort((a, b) => {
      if (a.title > b.title) {
        return 1;
      } else {
        return -1;
      }
    });

  // 2) Search (regex)
  if (!search.value || search.value === "") {
    return recipes;
  }

  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return recipes.filter((r) => {
    if (re.exec(replaceUnicode(r.title.toLowerCase()))) {
      return true;
    }
    return false;
  });
});

const toggleFilter = (tagName: string) => {
  // filter based on tags
  if (activeTags.value.indexOf(tagName) !== -1) {
    activeTags.value = activeTags.value.filter((t) => t != tagName);
  } else {
    activeTags.value.push(tagName);
  }
};
</script>
<style scoped lang="scss">
.wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.recipe-list {
  display: grid;
  gap: 0.3em;
  grid-template-columns: 1fr 1fr;
  // grid-template-rows: auto-fill;

  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr 1fr;
  }

  @media (min-width: 992px) {
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  }
}

.tags {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
  flex-wrap: wrap;
}

.empty-box {
  min-height: 65dvh;
  display: flex;
  flex-direction: column;
}
</style>
