<template>
  <q-drawer v-model="isOpened" bordered side="left" :width="280">
    <q-scroll-area class="h-full flex flex-col">
      <q-list separator>
        <q-item
          :active="currentRoute.name === 'recipes'"
          clickable
          v-ripple
          :to="{ name: 'recipes' }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="restaurant_menu" />
          </q-item-section>

          <q-item-section> Recipes </q-item-section>
        </q-item>

        <q-item
          :active="currentRoute.name === 'categories'"
          clickable
          v-ripple
          :to="{ name: 'categories' }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="apps" />
          </q-item-section>

          <q-item-section> Categories </q-item-section>
        </q-item>

        <q-item
          :active="currentRoute.name === 'ingredients'"
          clickable
          v-ripple
          :to="{ name: 'ingredients' }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="list" />
          </q-item-section>

          <q-item-section> Ingredients </q-item-section>
        </q-item>

        <q-item
          :active="currentRoute.name === 'new'"
          clickable
          v-ripple
          :to="{ name: 'new' }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="post_add" />
          </q-item-section>

          <q-item-section> Add a Recipe </q-item-section>
        </q-item>

        <q-item
          :active="currentRoute.name === 'newcategory'"
          clickable
          v-ripple
          :to="{ name: 'newcategory' }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="new_label" />
          </q-item-section>

          <q-item-section> Add a Category </q-item-section>
        </q-item>

        <q-item clickable v-ripple @click="store.fetch(true)">
          <q-item-section avatar>
            <q-icon name="refresh" />
          </q-item-section>

          <q-item-section> Reload All Recipes </q-item-section>
        </q-item>

        <q-separator />
        <q-item-label
          header
          v-if="showRecipeControls"
          class="uppercase font-bold mt-3"
          >{{ current?.title ?? "Recipe" }}</q-item-label
        >

        <q-item v-if="showRecipeControls" clickable>
          <q-item-section avatar>
            <q-icon name="image" />
          </q-item-section>
          <ImageUpload
            type="thumbnail"
            :recipe="current"
            @upload-success="close"
          />
        </q-item>

        <q-item v-if="showRecipeControls" clickable>
          <q-item-section avatar>
            <q-icon name="image" />
          </q-item-section>
          <ImageUpload
            type="detail"
            :recipe="current"
            @upload-success="close"
          />
        </q-item>

        <q-item
          v-if="current && showRecipeControls"
          clickable
          :to="{ name: 'editrecipe', params: { id: current.id } }"
          @click="close"
        >
          <q-item-section avatar>
            <q-icon name="edit" />
          </q-item-section>
          <q-item-section> Edit Recipe </q-item-section>
        </q-item>

        <q-item
          v-if="showRecipeControls"
          clickable
          @click="toggleDeleteDialog = !toggleDeleteDialog"
        >
          <q-item-section avatar>
            <q-icon name="delete" />
          </q-item-section>
          <q-item-section> Delete Recipe </q-item-section>
        </q-item>
      </q-list>
      <q-list class="absolute-bottom">
        <q-item clickable v-ripple @click="toggle">
          <q-item-section avatar>
            <q-icon :name="isDark ? 'light_mode' : 'dark_mode'" />
          </q-item-section>

          <q-item-section>{{
            isDark ? "Light Mode" : "Dark Mode"
          }}</q-item-section>
        </q-item>
      </q-list>

      <recipe-delete-dialog
        v-if="current"
        v-model="toggleDeleteDialog"
        :recipe="current"
      />
    </q-scroll-area>
  </q-drawer>
</template>

<script setup lang="ts">
import { useDarkmode } from "@/composables/darkmode";
import { useLayoutDrawer } from "@/composables/drawer";
import { useRecipeStore } from "@/stores/recipe";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";

import RecipeDeleteDialog from "@/components/recipe/RecipeDeleteDialog.vue";
import ImageUpload from "@/components/ui/ImageUpload.vue";
import { useQuasar } from "quasar";
import { computed, ref } from "vue";

const store = useRecipeStore();
const { current } = storeToRefs(store);

const { isOpened } = useLayoutDrawer();
const { isDark, toggle } = useDarkmode();

const { currentRoute } = useRouter();

const showRecipeControls = computed(
  () => current.value && currentRoute.value.name === "recipe"
);
const toggleDeleteDialog = ref(false);

const $q = useQuasar();
const close = () => {
  if ($q.screen.lt.md) {
    isOpened.value = false;
  }
};
</script>

<style lang="css" scoped></style>
