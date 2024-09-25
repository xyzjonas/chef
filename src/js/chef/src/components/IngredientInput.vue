<template>
  <q-card flat bordered class="flex flex-row flex-nowrap gap-1 p-2">
    <q-btn color="primary" dense flat @click="$emit('delete')" icon="close" />

    <ui-button
      dense
      flat
      @click="$emit('down')"
      icon="arrow_downward"
      color="secondary"
    />

    <ui-button
      dense
      flat
      @click="$emit('up')"
      icon="arrow_upward"
      color="secondary"
    />

    <div class="flex flex-row flex-nowrap gap-2 p-2 flex-1">      
      <!-- <ui-input class="amount" v-model="model.amount" size="small" label="amount" /> -->
      <q-input v-model="model.amount" borderless label="Amount" class="m-0 sm:ml-3"/>
      
      <!-- <ui-input class="unit" v-model="model.unit.name" label="unit" size="small" /> -->
      <q-select v-model="model.unit.name" borderless :options="units.map((u) => u.name)" />
        
        <!-- <ui-input class="ingredient" v-model="model.ingredient.name" label="ingredient" size="small" :success="ingredientExists" /> -->
        <q-select
        v-model="model.ingredient.name"
        label="Ingredient"
        :options="ingredientOptionsStrigs"
        use-input
        @filter="filterFn"
        clearable
        :input-debounce="0"
        hide-dropdown-icon
        new-value-mode="add-unique"
        borderless
        :rules="[(val) => !!val || 'Ingredient name is required']"
        >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              No such ingredient, new one will be created...
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      
      <q-input borderless v-model="model.note" label="note" class="flex-1"/>
    </div>

  </q-card>
</template>
<script setup lang="ts">
import UiButton from "@/components/ui/UiButton.vue";
import { useIngredientStore } from "@/stores/ingredient";
import type { Ingredient, IngredientItem } from "@/types";
import { computed, ref, watch } from "vue";
import { useUnitsStore } from "@/stores/units";
import { storeToRefs } from "pinia";

const model = defineModel<IngredientItem>({ required: true });

const props = defineProps<{ index?: number }>()

const emit = defineEmits(["update:ingredient", "delete", "up", "down"]);

const ingredientsSttore = useIngredientStore();
const unitsStore = useUnitsStore();

const { all: units } = storeToRefs(unitsStore);
const { all: ingredients } = storeToRefs(ingredientsSttore);

const ingredientExists = ref(false);
const ingredientOptions = ref<Ingredient[]>([]);
const ingredientOptionsStrigs = computed(() =>
  ingredientOptions.value.map((i) => i.name)
);
function filterFn(val: string, update: any, abort: any) {
  // call abort() at any time if you can't retrieve data somehow
  update(() => {
    if (val === "") {
      ingredientOptions.value = ingredients.value;
    } else {
      const needle = val.toLowerCase();
      ingredientOptions.value = ingredients.value.filter(
        (i) => i.name.toLowerCase().indexOf(needle) > -1
      );
    }
  });
}

function abortFilterFn() {
  // console.log('delayed filter aborted')
}


watch(model.value.ingredient, (old, n3w) => {
  console.info(n3w)
  if (!n3w || !n3w.name) {
    model.value.ingredient.id = undefined;
    return
  }

  n3w.name = n3w.name.toLocaleLowerCase();
  const match = ingredients.value.find((ing) => n3w.name === ing.name);
  if (match) {
    model.value.ingredient.id = match.id;
    ingredientExists.value = true;
  } else {
    model.value.ingredient.id = undefined;
    ingredientExists.value = false;
  }
});
</script>
<style lang="scss" scoped>
select {
  border-radius: 2px;
}
.arrow {
  width: 0.5em;
}
.ingredient-input {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
}

.amount {
  flex-basis: 4rem;
}

.unit {
  flex-basis: 2rem;
}

.ingredient {
  flex-grow: 2;
}
</style>
