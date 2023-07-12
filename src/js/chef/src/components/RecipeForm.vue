<template>
  <div v-if="recipe">

    <!-- title -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.title"
          :class="{
            input: true,
            'is-success': recipe.title,
            'is-danger': !recipe.title
          }"
          type="text"
          placeholder="Title"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-heading"></i>
        </span>
        <span v-if="recipe.title" class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </div>
      <p v-if="!recipe.title" class="help is-danger">Title is required</p>
    </div>

    <!-- sub-title -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.subtitle"
          class="input"
          type="text"
          placeholder="Subtitle"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-font"></i>
        </span>
      </div>
    </div>

    <!-- source (url) -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.source"
          class="input"
          type="text"
          placeholder="Source link"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-link"></i>
        </span>
      </div>
    </div>

    <!-- source (name) -->
    <div v-if="recipe.source" class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.source_name"
          class="input"
          type="text"
          placeholder="Source name"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-link"></i>
        </span>
      </div>
    </div>

    <!-- idea only -->
    <label class="checkbox my-2">
      <input type="checkbox" v-model="recipe.draft" />
      Recipe idea
      <i class="far fa-lightbulb"></i>
    </label>

    <!-- ingredients -->
    <div v-if="!recipe.draft">
      <label class="label">Ingredients</label>
       <div class="field">
         <div class="control">
           <div class="tags">
              <span v-for="(i, index) in recipe.ingredients" class="tag">
                <p>{{ i.amount }}<strong>{{ i.unit.name }}</strong> {{ i.ingredient.name }}
                  <span v-if="i.note">({{ i.note }})</span>
                </p>
                <button v-on:click="removeIngredient(i)" class="delete is-small"></button>
            </span>
           </div>
         </div>
        </div>
    </div>

    <div class="ingredient-items">
      <IngredientInput
        v-for="(i, index) in recipe.ingredients"
        :key="i.id"
        :initialData="i"
        @update:ingredient="ing => recipe.ingredients[index] = ing"
        @delete="removeIngredient(i)"
        @up="up(index)"
        @down="down(index)"
      />
      <button class="button mt-3" @click="recipe.ingredients.push(blankIngredient)">+</button>
    </div>

    <!-- portions -->
    <!-- PORTIONS COUNTER -->
    <div class="mt-4">
      <Counter :initialValue="recipe.portions" @counterUpdate="updateCounter"/>
    </div>
    <label class="label has-text-centered">(1 batch)</label>

    <hr>

    <div v-if="!recipe.draft" class="field my-2">
      <div class="control">
        <TextEditor @editorUpdate="updateText" :text="recipe.body"></TextEditor>
      </div>
    </div>


    <!-- tags -->
    <div class="field">
      <label class="label">Tags</label>
      <article v-if="availableTags.length < 1" class="message is-warning p-0">
        <small class="message-body p-2">no tags created yet</small>
      </article>
      <div class="control">
        <div>
          <a v-for="(tag, index) in availableTags" :key="`${tag},${index}`"
            v-on:click="toggleTag(tag)"
          >
            <span
              :class="{
                tag: true,
                'is-dark': recipe.tags && recipe.tags.map(t => t.name).includes(tag.name),
                'is-rounded': true,
                'mr-1': true
              }"
            >
              {{ tag.name }}
            </span>
          </a>
        </div>
      </div>
    </div>
    <div class="mb-5">
      <div class="field has-addons">
        <div class="control is-expanded">
          <input
            v-model="createTagField"
            class="input is-small is-rounded" type="text" placeholder="new tag"
          >
        </div>
        <div class="control ">
          <button v-on:click="createTag" class="button is-success is-small is-rounded">
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="my-1">
      <button
        @click="postRecipe"
        :class="{
          'button': true,
          'is-fullwidth': true,
          'is-success': true,
          'is-loading': recipeStore.loading
        }"
        :disabled="!recipe.title"
      >Save</button>
    </div>
    <div class="my-1">
      <button @click="$emit('cancel')" class="button is-fullwidth">Cancel</button>
    </div>

    <!-- msg -->
    <article v-if="postSuccess" class="message is-success">
      <div class="message-body">{{ postSuccess }}</div>
    </article>
    <article v-if="postError" class="message is-danger">
      <div class="message-body">{{ postError }}</div>
    </article>
  </div>
</template>

<script setup lang="ts">
import TextEditor from "@/components/TextEditor.vue";
import Counter from "@/components/Counter.vue";
import IngredientInput from "@/components/IngredientInput.vue";
import type { Recipe, IngredientItem, Tag, CreateRecipe } from "@/types";
import { computed, ref } from "vue";
import { useRecipeStore } from "@/stores/recipe";
import { useTagStore } from "@/stores/tags";
import { deepCopy } from "@/utils";


const recipeStore = useRecipeStore();
const tagStore = useTagStore();
const availableTags = tagStore.all;


const props = defineProps<{
  data: Recipe | CreateRecipe
}>()
const recipe = ref<Recipe>(deepCopy(props.data));

const counter = ref<number>(4);
const createTagField = ref<string>();

const postSuccess = ref();
const postError = ref();

const formIsValid = computed(() => {
  // todo
})


const updateCounter = (val: number) => {
  counter.value = val
  recipe.value.portions = val
}

const updateText = (value: string) => {
  recipe.value.body = value;
}

const blankIngredient: IngredientItem = {
  amount: 0,
  unit: { name: "g" },
  ingredient: { name: "" },
  note: "",
}
const removeIngredient = (ingredient: IngredientItem) => {
  recipe.value.ingredients = recipe.value.ingredients.filter(i => {
    return !(
      i.ingredient.name === ingredient.ingredient.name
      && i.amount === ingredient.amount
      && i.unit.name === ingredient.unit.name
      && i.note === ingredient.note
    );
  });
}

const up = (index: number) => {
  if (index === 0) {
    return
  }
  const item = recipe.value.ingredients[index];
  recipe.value.ingredients[index] = recipe.value.ingredients[index - 1];
  recipe.value.ingredients[index - 1] = item;
}

const down = (index: number) => {
  if (index === recipe.value.ingredients.length - 1) {
    return
  }
  const item = recipe.value.ingredients[index];
  recipe.value.ingredients[index] = recipe.value.ingredients[index + 1];
  recipe.value.ingredients[index + 1] = item;
}

const toggleTag = (tag: Tag) => {
  var tagNames = recipe.value.tags.map(t => t.name)
  if (!tagNames.includes(tag.name)) {
    recipe.value.tags.push(tag);
  } else {
    recipe.value.tags = recipe.value.tags.filter(t => t.name != tag.name)
  }
}

const createTag = () => {
  if (createTagField.value) {
    var tag = { name: createTagField.value };
    availableTags.push(tag);
    createTagField.value = undefined;
    recipe.value.tags.push(tag);
  }
}

const emit = defineEmits(['posted', 'created']);
const postRecipe = () => {
  if (recipe.value.id) {
    console.debug('Updating existing recipe.')
    recipeStore.update(recipe.value).then(r => emit('posted', r));
  } else {
    console.debug('Creating new recipe.')
    recipeStore.create(recipe.value).then(r => emit('posted', r));
  }
}

</script>

<style>
  .ingredient-items {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .fullwidth {
    width: 100%;
  }
</style>
