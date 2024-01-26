<template>
  <div class="wrapper">

    <!-- RECIPE COUNT -->
    <div v-if="allRecipes.length > 0">
      <h1 id="r-count">{{ displayedRecipes.length }} {{ title || 'Recipes' }}</h1>
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
    <ui-input v-if="allRecipes.length > 0" v-model="search" :icon="Search" size="large" style="margin-block: .8rem;"/>

    <!-- LIST -->
    <div class="recipe-list" v-if="allRecipes.length > 0">
      <div v-for="(recipe) in displayedRecipes" :key="'recipe_a_key+' + recipe.id" :recipe="recipe">
        <component :is="RecipeListItem" :recipe="recipe" />
      </div>
    </div>
    <div v-else class="empty-box">
      <empty-box
        link-text="add a new recipe"
        route-name="new"
        title="Goodness Gracious!"
        subtitle="The recipe list seems to have taken a tea break. Why not take charge and add your culinary masterpieces?"
      />
    </div>

  </div>  
</template>

<script setup lang="ts">
import RecipeListItem from "@/components/RecipeListItem.vue";
import EmptyBox from "@/components/ui/EmptyBox.vue";
import Search from "@/components/icons/Search.vue"
import UiInput from "./ui/UiInput.vue";
import Pin from "@/components/ui/Pin.vue";
import type { Recipe } from "@/types";
import { replaceUnicode } from "@/utils";
import { computed, ref, watch } from "vue";

const props = defineProps<{
  allRecipes: Recipe[],
  title?: string,
  hideSearch?: boolean,
  hideFilters?: boolean,
}>()

const activeTags = ref<string[]>([])
const search = ref<string>()

const tagNames = computed<string[]>(() => {
   return [...new Set(props.allRecipes.map(recipe => recipe.tags.map(tag => tag.name)).flat())]
})

const displayedRecipes = computed<Recipe[]>(() => {
  const recipes = props.allRecipes.filter(r => {
    var recipeTags = r.tags.map(t => t.name);
    if (!recipeTags) return true; // if a recipe has no tags, always show
    for (let i = 0; i < activeTags.value.length; i++) {
        const tag = activeTags.value[i];
        if (!recipeTags.includes(tag)) {
          return false;
        }
      }
      return true;
  }).sort((a, b) => {
    if (a.title > b.title) {
      return 1
    } else {
      return -1
    }
  });

  // 2) Search (regex)
  if (!search.value || search.value === "") {
    return recipes;
  }

  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return recipes.filter(r => {
    if (re.exec(replaceUnicode(r.title.toLowerCase()))) {
      return true;
    }
    return false;
  })
})

const toggleFilter = (tagName: string) => {
  // filter based on tags
  if (activeTags.value.indexOf(tagName) !== -1) {
    activeTags.value = activeTags.value.filter(t => t != tagName);
  } else {
    activeTags.value.push(tagName);
  }
}
</script>
<style scoped lang="scss">
.wrapper {
  display: flex;
  flex-direction: column;
  gap: .5rem;
}

.recipe-list {
  display: grid;
  gap: 0.3em;
  grid-template-columns: 1fr 1fr;

  @media (min-width: 768px){
    grid-template-columns: 1fr 1fr 1fr;
  }

  @media (min-width: 992px){
  	grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}

.tags {
  display: flex;
  flex-direction: row;
  gap: .3rem;
  flex-wrap: wrap;
}

#r-count {
  font-weight: 100;
  margin-top: 0;
  margin-bottom: 1rem;
}

.empty-box {
  height: 65dvh;;
}
</style>