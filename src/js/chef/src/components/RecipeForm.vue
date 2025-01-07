<template>
    <q-form ref="$form" v-if="recipe" @submit="postRecipe">
      <KeepDraftDialog v-model="draftDialog" @discard="resetForm" />
      <q-input
        outlined
        v-model="recipe.title"
        label="Title"
        autocomplete="off"
        hint="The main title"
        :rules="[(val: string) => !!val || 'Title is required']"
      />

      <q-input
        outlined
        v-model="recipe.subtitle"
        label="Subtitle"
        autocomplete="off"
        hint="Recipe's subtitle"
      />

      <q-input
        outlined
        v-model="recipe.source"
        label="Source Link"
        hint="Link to the original recipe, needs to be a valid URL"
        autocomplete="off"
      />

      <q-input
        outlined
        v-model="recipe.source_name"
        label="Source Name"
        hint="Display name of the link"
        autocomplete="off"
      />

      <div class="flex items-center justify-between sm:justify-end">
        <h3 class="text-xl md:text-2xl uppercase">Ingredients</h3>
        <Counter
          v-model="recipe.portions"
          @counterUpdate="updateCounter"
          class="sm:m-0"
        />
      </div>
      <transition-group name="ingredientlist">
        <IngredientInput
          v-for="(ingredient, index) in recipe.ingredients"
          :key="ingredient.uuid"
          v-model="recipe.ingredients[index]"
          :index="index"
          @update:ingredient="(ing) => (recipe.ingredients[index] = ing)"
          @delete="removeIngredient(ingredient)"
          @up="up(index)"
          @down="down(index)"
        />
      </transition-group>
      <div>
        <q-btn
          flat
          color="primary"
          @click="recipe.ingredients.push(generateBlankIngredient())"
          icon="add"
          label="add ingredient"
        />
      </div>

      <q-separator />

      <div v-if="!recipe.draft" class="field my-2">
        <TextEditor @editorUpdate="updateText" :text="recipe.body"></TextEditor>
      </div>

      <h3 class="text-2xl uppercase mt-5 mb-0">Labels</h3>
      <article v-if="availableTags.length < 1" class="message is-warning p-0">
        <small class="message-body p-2">no tags created yet</small>
      </article>

      <q-select
        filled
        v-model="recipe.tags"
        multiple
        :options="availableTags"
        :option-label="(opt) => opt.name"
        use-chips
        use-input
        @new-value="addTag"
        stack-label
        label="Recipe Labels"
        hint="Select labels to help define recipe's category"
        class="mb-5"
      />

      <div class="flex mt-auto gap-2 h-[3rem]">
        <q-btn
          unelevated
          color="primary"
          :disabled="!recipe.title"
          label="save"
          class="flex-1"
          type="submit"
        />
        <ui-button
          color="secondary"
          flat
          @click="$emit('cancel')"
          text="cancel"
          type="secondary"
          class="flex-1"
        />
      </div>
    </q-form>
</template>

<script setup lang="ts">
import Counter from "@/components/Counter.vue";
import IngredientInput from "@/components/IngredientInput.vue";
import TextEditor from "@/components/TextEditor.vue";
import UiButton from "@/components/ui/UiButton.vue";
import { useRecipeStore } from "@/stores/recipe";
import { useTagStore } from "@/stores/tags";
import type { CreateRecipe, IngredientItem, Recipe, Tag } from "@/types";
import { deepCopy, generateUUID } from "@/utils";
import { useLocalStorage } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { QForm } from "quasar";
import { ref, useTemplateRef } from "vue";
import KeepDraftDialog from "./recipe/KeepDraftDialog.vue";

const recipeStore = useRecipeStore();
const tagStore = useTagStore();
const { all: availableTags } = storeToRefs(tagStore);

const $form = useTemplateRef("$form");

const props = defineProps<{
  id: string;
  data: Recipe | CreateRecipe;
}>();
const recipe = useLocalStorage<Recipe>(
  `autosave-${props.id}`,
  deepCopy(props.data)
);
if (!recipe.value.portions) {
  recipe.value.portions = 4;
}

const draftDialog = ref(false);
if (JSON.stringify(recipe.value) !== JSON.stringify(props.data)) {
  draftDialog.value = true;
}
const resetForm = () => {
  recipe.value = deepCopy(props.data);
};

const counter = ref<number>(4);

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
    uuid: generateUUID(),
  };
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
  const item = recipe.value.ingredients.splice(index, 1)[0];
  setTimeout(() => recipe.value.ingredients.splice(index - 1, 0, item), 300);
};

const down = (index: number) => {
  if (index === recipe.value.ingredients.length - 1) {
    return;
  }
  const item = recipe.value.ingredients.splice(index, 1)[0];
  setTimeout(() => recipe.value.ingredients.splice(index + 1, 0, item), 300);
};

const toggleTag = (tag: Tag) => {
  var tagNames = recipe.value.tags.map((t) => t.name);
  if (!tagNames.includes(tag.name)) {
    recipe.value.tags.push(tag);
  } else {
    recipe.value.tags = recipe.value.tags.filter((t) => t.name != tag.name);
  }
};

const addTag = (value: string, done: (val: any) => void) => {
  const newTag = { name: value };
  done(newTag);
};

const emit = defineEmits(["posted", "created", "cancel"]);
const postRecipe = async () => {
  if (!(await $form.value?.validate())) {
    return;
  }
  if (recipe.value.id) {
    console.debug("Updating existing recipe.");
    recipeStore.update(recipe.value).then((r) => emit("posted", r));
  } else {
    console.debug("Creating new recipe.");
    recipeStore.create(recipe.value).then((r) => emit("posted", r));
  }
};
</script>

<style lang="css" scoped>
.ingredientlist-enter-active {
  transition: all 0.3s ease-out;
}
.ingredientlist-leave-active {
  transition: all 0.3s ease-in;
}
.ingredientlist-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.ingredientlist-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.tags {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.level {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
}

.mt {
  margin-top: 1rem;
}
</style>
