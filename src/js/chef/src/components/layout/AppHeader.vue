<template>
  <q-toolbar>
    <q-toolbar-title>
      <router-link :to="{ name: 'recipes' }" id="brand" class="text-white">
        <q-img
          src="@/assets/logo.svg"
          width="42px"
          height="42px"
          class="rounded-full"
        />
        <span class="ml-2 font-title text-2xl">CHEF</span>
      </router-link>
    </q-toolbar-title>

    <q-btn dense flat :icon="isOpened ? 'close' : 'menu'" @click="toggle" />

    <!-- <div class="flex flex-row items-center gap-3">
      <ui-button
        color="primary"
        type="link"
        text="categories"
        icon="folder"
        :to="{ name: 'categories' }"
      ></ui-button>

      <ui-button
        color="primary"
        text="recipe"
        icon="add"
        :to="{ name: 'new' }"
      ></ui-button>

      <q-btn
        dense
        flat
        :icon="isDark ? 'light_mode' : 'dark_mode'"
        @click="toggle"
      />
    </div> -->
  </q-toolbar>
</template>

<script setup lang="ts">
import { useDarkmode } from "@/composables/darkmode";
import { useLayoutDrawer } from "@/composables/drawer";

const { isOpened, toggle } = useLayoutDrawer()

// const { isDark, toggle } = useDarkmode();
</script>

<style lang="scss" scoped></style>
