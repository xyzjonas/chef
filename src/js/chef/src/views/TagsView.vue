<template>
  <q-page padding>
    <div class="flex items-center justify-between mb-4">
      <h1 class="title-sm my-0">{{ title }}</h1>
      <q-input
        outlined
        dense
        v-model="search"
        placeholder="Search"
        class="ml-auto"
      >
        <template v-slot:prepend>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>

    <empty-box
      v-if="tagsStore.all.length === 0"
      title="No tags yet"
      subtitle="Create your first tag to start organizing recipes"
    />

    <div v-else class="tag-grid">
      <q-card
        v-for="tag in filteredTags"
        :key="tag.id"
        flat
        bordered
        class="tag-tile hover:border-primary transition"
        @click="edit(tag)"
      >
        <q-card-section class="flex items-center gap-3">
          <q-icon :name="tag.icon ?? 'label'" size="md" class="text-gray-6" />
          <span class="capitalize text-lg">{{ tag.name }}</span>
          <q-icon name="edit" size="xs" class="ml-auto text-gray-4" />
        </q-card-section>
      </q-card>

      <q-card
        flat
        bordered
        class="tag-tile add-tile flex items-center justify-center"
        @click="createNew"
      >
        <q-card-section class="flex items-center gap-2 text-primary">
          <q-icon name="add" />
          <span>New Tag</span>
        </q-card-section>
      </q-card>
    </div>

    <TagDialog />
  </q-page>
</template>

<script setup lang="ts">
import EmptyBox from "@/components/ui/EmptyBox.vue";
import TagDialog from "@/components/tag/TagDialog.vue";
import { useTagDialog } from "@/composables/tagDialog";
import { useTagStore } from "@/stores/tags";
import type { Tag } from "@/types";
import { replaceUnicode } from "@/utils";
import { computed, onMounted, ref } from "vue";

const tagsStore = useTagStore();
const { open } = useTagDialog();

const search = ref<string>();

onMounted(() => tagsStore.fetch());

const filteredTags = computed(() => {
  if (!search.value) {
    return tagsStore.all;
  }
  const re = new RegExp(replaceUnicode(search.value.toLowerCase()));
  return tagsStore.all.filter((tag) =>
    re.exec(replaceUnicode(tag.name.toLowerCase()))
  );
});

const title = computed(() =>
  tagsStore.all.length === 1 ? "Tag" : "Tags"
);

const edit = (tag: Tag) => open(tag);
const createNew = () => open();
</script>

<style scoped lang="scss">
.tag-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(12rem, 1fr));
  gap: 0.75rem;
}

.tag-tile {
  cursor: pointer;
}
</style>
