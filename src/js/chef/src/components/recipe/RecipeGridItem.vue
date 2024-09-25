<template>
  <q-card flat bordered class="hover:cursor-pointer hover:border-primary transition" @click="router.push({ name: 'recipe', params: { id: recipe.id } })">
      <q-img :src="recipe.thumbnail_image ?? 'none'" error-src="@/assets/notfound.jpg" :ratio="1.6" />

      <q-card-section>
        <div class="text-lg uppercase line-height-snug">{{ recipe.title }}</div>
        <div class="text-xs uppercase text-gray-7 dark:text-gray-4">{{ recipe.subtitle }}</div>
      </q-card-section>

      <q-card-section class="q-pt-none flex gap-1">
        <q-badge rounded v-for="tag in recipe.tags">{{ tag.name }}</q-badge>
      </q-card-section>
      
    </q-card>

</template>

<script setup lang="ts">
import type { Recipe } from "@/types";
import { computed } from "vue";
import { useRouter } from "vue-router";

import Card from "@/components/ui/Card.vue";
import Pin from "@/components/ui/Pin.vue";
import router from "@/router";

const { push } = useRouter();

interface Props {
  recipe: Recipe;
}
const props = defineProps<Props>();

const image = computed(() => props.recipe.thumbnail_image ?? "@/assets/notfound.jpg");
</script>

<style lang="css" scoped>
.title {
  font-size: medium;
  font-weight: 500;
  letter-spacing: -1px;
}

.subtitle {
  font-size: small;
}

.card {
  transition: 0.2s ease-in-out;
}

.card:hover {
  border-color: var(--primary-100);
  cursor: pointer;
}

.card:hover p {
  text-decoration: underline;
}
</style>
