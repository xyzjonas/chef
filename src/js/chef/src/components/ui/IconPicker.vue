<template>
  <div class="icon-picker">
    <q-input
      v-model="search"
      dense
      outlined
      clearable
      autocomplete="off"
      placeholder="Search icons"
      class="mb-2"
    >
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>

    <q-scroll-area class="icon-picker-scroll" style="height: 220px">
      <div v-if="filteredGroups.length === 0" class="text-center text-gray-5 py-4">
        No icons found
      </div>

      <div v-for="group in filteredGroups" :key="group.category" class="mb-3">
        <div class="text-xs uppercase text-gray-5 font-bold mb-1 px-1">
          {{ group.category }}
        </div>
        <div class="icon-grid">
          <q-btn
            v-for="icon in group.icons"
            :key="icon"
            round
            :flat="model !== icon"
            :unelevated="model === icon"
            :color="model === icon ? 'primary' : undefined"
            @click="select(icon)"
          >
            <q-icon :name="icon" />
            <q-tooltip>{{ formatLabel(icon) }}</q-tooltip>
          </q-btn>
        </div>
      </div>
    </q-scroll-area>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

// Curated, theme-appropriate icon set (Material Icons ligature names, the
// only icon font currently loaded via @quasar/extras/material-icons).
const ICON_GROUPS: { category: string; icons: string[] }[] = [
  {
    category: "Dishes",
    icons: [
      "restaurant",
      "restaurant_menu",
      "local_dining",
      "local_pizza",
      "fastfood",
      "bakery_dining",
      "lunch_dining",
      "dinner_dining",
      "brunch_dining",
      "breakfast_dining",
      "ramen_dining",
      "set_meal",
      "tapas",
      "kebab_dining",
      "egg",
      "egg_alt",
      "soup_kitchen",
      "rice_bowl",
      "outdoor_grill",
      "cake",
      "icecream",
      "cookie",
      "donut_large",
      "donut_small",
      "bento",
      "food_bank",
    ],
  },
  {
    category: "Drinks",
    icons: [
      "local_cafe",
      "local_bar",
      "coffee",
      "coffee_maker",
      "liquor",
      "wine_bar",
      "sports_bar",
      "emoji_food_beverage",
      "local_drink",
      "water",
      "water_drop",
      "no_drinks",
      "opacity",
    ],
  },
  {
    category: "Cooking",
    icons: [
      "kitchen",
      "blender",
      "microwave",
      "countertops",
      "room_service",
      "takeout_dining",
      "delivery_dining",
      "local_fire_department",
      "whatshot",
      "ac_unit",
      "timer",
      "schedule",
      "straighten",
    ],
  },
  {
    category: "Dietary & Health",
    icons: [
      "energy_savings_leaf",
      "spa",
      "compost",
      "favorite",
      "star",
      "no_food",
    ],
  },
  {
    category: "Animals & Nature",
    icons: [
      "pets",
      "cruelty_free",
      "flutter_dash",
      "bug_report",
      "grass",
      "local_florist",
      "forest",
      "park",
      "yard",
      "agriculture",
      "nature",
      "emoji_nature",
    ],
  },
  {
    category: "Organization",
    icons: [
      "category",
      "label",
      "local_offer",
      "bookmark",
      "shopping_cart",
      "shopping_basket",
      "store",
      "storefront",
      "local_grocery_store",
      "inventory_2",
      "recycling",
    ],
  },
  {
    category: "Occasions",
    icons: [
      "celebration",
      "cottage",
      "home",
      "groups",
      "people",
      "public",
      "flag",
      "language",
      "explore",
      "travel_explore",
    ],
  },
];

const model = defineModel<string | null | undefined>();
const search = ref("");

function select(icon: string) {
  model.value = model.value === icon ? null : icon;
}

function formatLabel(icon: string) {
  return icon.replaceAll("_", " ");
}

const filteredGroups = computed(() => {
  const query = search.value?.trim().toLowerCase() ?? "";
  if (!query) {
    return ICON_GROUPS;
  }

  return ICON_GROUPS.map((group) => ({
    category: group.category,
    icons: group.icons.filter((icon) => formatLabel(icon).includes(query)),
  })).filter((group) => group.icons.length > 0);
});
</script>

<style scoped lang="scss">
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(2.5rem, 1fr));
  gap: 0.25rem;
}
</style>
