<template>
  <div v-on:click="clicked" class="card">
    <!-- title -->
    <h1>{{ category.name }}</h1>

    <div class="flex mt-auto">
      <div class="flex flex-wrap gap-1">
        <pin
          color="primary"
          v-for="tag in category.tags"
          rounded
          :text="tag.name"
          size="small"
        ></pin>
      </div>

      <q-btn
        v-if="editable"
        dense
        color="primary"
        unelevated
        icon="edit"
        @click="
          $router.push({ name: 'editcategory', params: { id: category.id } })
        "
        id="edit-btn"
      />
      <q-btn
        v-if="editable"
        dense
        color="white"
        flat
        unelevated
        @click="clickDelete"
        icon="delete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import CategoryForm from "@/components/CategoryForm.vue";
import ImageUpload from "@/components/ui/ImageUpload.vue";
import { IMAGES_URL } from "@/constants";
import { useCategoryStore } from "@/stores/categories";
import type { Category, ChefNotification } from "@/types";
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useEventBus } from "@vueuse/core";
import Pin from "@/components/ui/Pin.vue";

const categories = useCategoryStore();

const props = defineProps<{
  category: Category;
  editable?: boolean;
}>();
const emit = defineEmits(["categoryEdited", "categoryDeleted", "clicked"]);

const uploadError = ref(null);
const imageUploadFailed = (err: any) => {
  uploadError.value = err;
};

const edit = ref(false);
const clicked = () => {
  emit("clicked", props.category);
};

const backgroundStyle = `url('${IMAGES_URL}/categories/${props.category.id}/landscape.jpeg')`;

const router = useRouter();
const edited = () => {
  edit.value = false;
  categories.imageCache[props.category.id] = Math.random();
  emit("categoryEdited");
};

const responseBusId = `delete-category-${props.category.id}`;

const bus = useEventBus<ChefNotification>("notifications");
const responseBus = useEventBus<string>(responseBusId);

const clickDelete = () =>
  bus.emit({
    level: "ERROR",
    message: `Delete category ${props.category.name}?`,
    action: {
      id: responseBusId,
      label: "Delete",
    },
  });

const onDeleteConfirmListener = (incommingId: string) => {
  categories.deleteById(props.category.id).then((res) => {
    emit("categoryDeleted", res);
    router.push({ name: "categories" });
  });
};

responseBus.on(onDeleteConfirmListener);
</script>

<style lang="scss" scoped>
.disabled {
  pointer-events: none;
  cursor: default;
}

.clickable {
  position: relative;
}
.clickable-link::after {
  position: absolute;
}
.clickable-link::after {
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}
.card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 0.3rem;
  min-height: 18dvh;
  position: relative;

  background-color: #ffebe8;

  background-image: v-bind("backgroundStyle");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;

  cursor: pointer;

  transition: filter 0.2s ease-in-out;
}

h1,
h2 {
  margin: 0;
  color: var(--text-inv);
  text-shadow: 1px 1px 1px var(--text), 1px 1px 5px var(--text);
}

h2 {
  font-size: medium;
}

.tags {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
  flex-wrap: wrap;

  margin-top: auto;
}
.tile-title {
  padding: 3px 10px;
  // background-color: #FFFFFFBB;
  width: fit-content;
  border-radius: 5px;
  text-shadow: 2px 2px 5px black;
  color: white;
}
.mytag {
  background-color: #ffffffbb;
  margin: 0.1em;
  border-radius: 0.2em;
  padding-left: 0.3em;
  padding-right: 0.3em;
  border: solid 1px #99999958;
}

.tile {
  height: 12em;
}

.level {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  align-items: center;
}

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                    supported by Chrome and Opera */
}

#edit-btn {
  margin-left: auto;
}

#edit {
  & > h5 {
    font-weight: 100;
    font-size: xx-large;
    margin-block: 1rem;
  }

  border: 1px solid var(--bg-300);
  border-radius: 0.5rem;
  background-color: var(--bg-100);
  padding: 1rem;
}
</style>
