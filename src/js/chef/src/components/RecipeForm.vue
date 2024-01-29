<template>
  <form v-if="recipe">
    
    <ui-input v-model="recipe.title" label="title" size="small" />
    <p v-if="!recipe.title" class="help is-danger">Title is required</p>

    <ui-input v-model="recipe.subtitle" label="subtitle" size="small" />

    <ui-input v-model="recipe.source" label="source link" size="small" />

    <ui-input v-model="recipe.source_name" label="source name" size="small" />

    <!-- idea only -->
    <!-- <label class="checkbox my-2">
      <input type="checkbox" v-model="recipe.draft" />
      Recipe idea
      <i class="far fa-lightbulb"></i>
    </label> -->

    <h3>Ingredients</h3>
    <IngredientInput
      v-for="(ingredient, index) in recipe.ingredients"
      :key="ingredient.id"
      v-model="recipe.ingredients[index]"
      :index="index"
      @update:ingredient="(ing) => (recipe.ingredients[index] = ing)"
      @delete="removeIngredient(ingredient)"
      @up="up(index)"
      @down="down(index)"
    />
    <div>
      <ui-button
        @click="recipe.ingredients.push(generateBlankIngredient())"
        icon="fas fa-plus"
        text="add ingredient"
        type="secondary"
      />
    </div>
    
    <h3>Portions</h3>
    <Counter v-model="recipe.portions" @counterUpdate="updateCounter" />

    <h3></h3>

    <div v-if="!recipe.draft" class="field my-2">
      <TextEditor @editorUpdate="updateText" :text="recipe.body"></TextEditor>
    </div>

    <h3>Tags</h3>
    <article v-if="availableTags.length < 1" class="message is-warning p-0">
      <small class="message-body p-2">no tags created yet</small>
    </article>
    <div class="tags">
      <pin
        v-for="(tag, index) in availableTags"
        :key="`${tag},${index}`"
        @click="toggleTag(tag)"
        clickable
        :active="recipe.tags.map((t) => t.name).includes(tag.name)"
        :text="tag.name"
      />
    </div>
    <div class="level mt">
      <ui-button @click="createTag" icon="fas fa-plus" />
      <ui-input v-model="createTagField" size="small" label="new tag" />
    </div>

    <div class="level mt">
      <ui-button @click="postRecipe" :disabled="!recipe.title" text="save" />
      <ui-button @click="$emit('cancel')" text="cancel" type="secondary" />
    </div>

    <!-- msg -->
    <article v-if="postSuccess" class="message is-success">
      <div class="message-body">{{ postSuccess }}</div>
    </article>
    <article v-if="postError" class="message is-danger">
      <div class="message-body">{{ postError }}</div>
    </article>
  </form>
</template>

<script setup lang="ts">
import TextEditor from "@/components/TextEditor.vue";
import Counter from "@/components/Counter.vue";
import Pin from "@/components/ui/Pin.vue";
import IngredientInput from "@/components/IngredientInput.vue";
import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import type { Recipe, IngredientItem, Tag, CreateRecipe } from "@/types";
import { computed, ref } from "vue";
import { useRecipeStore } from "@/stores/recipe";
import { useTagStore } from "@/stores/tags";
import { deepCopy } from "@/utils";
import { storeToRefs } from "pinia";

const recipeStore = useRecipeStore();
const tagStore = useTagStore();
const { all: availableTags} = storeToRefs(tagStore);

const props = defineProps<{
  data: Recipe | CreateRecipe;
}>();
const recipe = ref<Recipe>(deepCopy(props.data));
if (!recipe.value.portions) {
  recipe.value.portions = 4;
}

const counter = ref<number>(4);
const createTagField = ref<string>();

const postSuccess = ref();
const postError = ref();

const formIsValid = computed(() => {
  // todo
});

const updateCounter = (val: number) => {
  counter.value = val;
  recipe.value.portions = val;
};

const updateText = (value: string) => {
  recipe.value.body = value;
};

const generateBlankIngredient = (): IngredientItem => {
  return {
    amount: 0,
    unit: { name: "g" },
    ingredient: { name: "" },
    note: "",
  }
};
const removeIngredient = (ingredient: IngredientItem) => {
  recipe.value.ingredients = recipe.value.ingredients.filter((i) => {
    return !(
      i.ingredient.name === ingredient.ingredient.name &&
      i.amount === ingredient.amount &&
      i.unit.name === ingredient.unit.name &&
      i.note === ingredient.note
    );
  });
};

const up = (index: number) => {
  if (index === 0) {
    return;
  }
  const item = recipe.value.ingredients[index];
  recipe.value.ingredients[index] = recipe.value.ingredients[index - 1];
  recipe.value.ingredients[index - 1] = item;
};

const down = (index: number) => {
  if (index === recipe.value.ingredients.length - 1) {
    return;
  }
  const item = recipe.value.ingredients[index];
  recipe.value.ingredients[index] = recipe.value.ingredients[index + 1];
  recipe.value.ingredients[index + 1] = item;
};

const toggleTag = (tag: Tag) => {
  var tagNames = recipe.value.tags.map((t) => t.name);
  if (!tagNames.includes(tag.name)) {
    recipe.value.tags.push(tag);
  } else {
    recipe.value.tags = recipe.value.tags.filter((t) => t.name != tag.name);
  }
};

const createTag = () => {
  if (createTagField.value) {
    var tag = { name: createTagField.value };
    availableTags.value.push(tag);
    createTagField.value = undefined;
    recipe.value.tags.push(tag);
  }
};

const emit = defineEmits(["posted", "created", "cancel"]);
const postRecipe = () => {
  if (recipe.value.id) {
    console.debug("Updating existing recipe.");
    recipeStore.update(recipe.value).then((r) => emit("posted", r));
  } else {
    console.debug("Creating new recipe.");
    recipeStore.create(recipe.value).then((r) => emit("posted", r));
  }
};
</script>

<style>
form {
  display: flex;
  flex-direction: column;
  gap: .5rem;
}
.ingredient-items {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.fullwidth {
  width: 100%;
}
.help {
  font-size: x-small;
  margin: 0;
  color: var(--primary);
}

h3 {
  font-weight: 100;
  margin: 0;
  margin-top: 1rem;
}

.tags {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: .3rem;
}

.level {
  display: flex;
  flex-direction: row;
  gap: .3rem;
}

.mt {
  margin-top: 1rem;
}
</style>
