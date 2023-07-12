<template>
  <div>

    <!-- RECIPE COUNT -->
    <div class="mb-2">
      <h1 class="title is-4 has-text-primary">{{ recipes.length }} {{ title || 'Recipes' }}</h1>
    </div>

    <!-- TAGS -->
    <div v-if="!hideFilters" class="tags">
      <a v-for="tag in tagNames" :key="'tag_key' + tag"
        @click="toggleFilter(tag)"
        :class="{ 'tag':true,  'is-rounded':true, 'is-dark': activeTags.includes(tag), 'noselect': true}"
        style="text-decoration:none;"
      >{{ tag }}</a>
    </div>

    <!-- search -->
    <p v-if="!hideSearch" class="control has-icons-left mb-4">
      <input 
        v-model="search"
        class="input is-rounded"
        type="text"
        placeholder="search">
      <span class="icon is-small is-left">
        <i class="fas fa-search"></i>
      </span>
    </p>

    <!-- LIST -->
    <div class="recipe-list">
      <RecipeListItem v-for="(recipe) in recipes" :key="'recipe_a_key+' + recipe.id" :recipe="recipe" />
    </div>

  </div>  
</template>

<script setup lang="ts">
import RecipeListItem from "@/components/RecipeListItem.vue";
import type { Recipe } from "@/types";
import { replaceUnicode } from "@/utils";
import { computed, ref } from "vue";

const props = defineProps<{
  allRecipes: Recipe[],
  title: string,
  hideSearch: boolean,
  hideFilters: boolean
}>()

const activeTags = ref<string[]>([])
const search = ref<string>()
const recipesInitiated = ref(false)


const tagNames = computed<string[]>(() => {
   return [...new Set(props.allRecipes.map(recipe => recipe.tags.map(tag => tag.name)).flat())]
})

const recipes = computed<Recipe[]>(() => {
  recipesInitiated.value = true;

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
  if (!search.value || search.value === "") return recipes;
  var re = new RegExp(replaceUnicode(search.value.toLowerCase()));
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
.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 0.3em;
}
</style>