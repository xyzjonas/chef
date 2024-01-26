<template>
  <form>
    <!-- title -->
    <ui-input v-model="category.name" label="name" />
    <p v-if="!category.name" class="help">Name is required</p>

    <!-- tags -->
    <div class="tags">
      <pin
        v-for="tag in tags.all"
        :key="tag.id"
        :text="tag.name"
        clickable
        :active="category.tags && category.tags.map(t => t.name).includes(tag.name)"
        @click="toggleTag(tag)"
      />
    </div>
    <article v-if="tags.all.length < 1" class="message is-warning p-0">
      <small class="message-body p-2">no tags created yet</small>
    </article>

    <!-- BUTTONS -->

    <div class="level">
      <ui-button @click="postCategory" :disabled="!category.name" text="save" type="primary" icon="fas fa-save" />
      <ui-button @click="$emit('cancel')" text="cancel" type="secondary"/>
    </div>
  </form>
</template>

<script setup lang="ts">
import UiInput from "@/components/ui/UiInput.vue";
import UiButton from "./ui/UiButton.vue";
import Pin from "@/components/ui/Pin.vue";
import Search from "./icons/Search.vue";
import { useCategoryStore } from "@/stores/categories";
import { useTagStore } from "@/stores/tags";
import type { CreateCategory, Tag } from "@/types";
import { deepCopy } from "@/utils";
import { ref } from "vue";

const tags = useTagStore();

const props = defineProps<{
  inputCategory: CreateCategory | undefined
}>()

const category = ref<CreateCategory>({
  name: "",
  tags: []
})
if (props.inputCategory) {
  category.value = deepCopy(props.inputCategory);
}

const toggleTag = (beingToggled: Tag) => {
  const tagNames = category.value.tags.map(t => t.name);
  if (!tagNames.includes(beingToggled.name)) {
    category.value.tags.push(beingToggled);
  } else {
    category.value.tags = category.value.tags.filter(tag => beingToggled.name !== tag.name)
  }
}

const emit = defineEmits(['categoryPosted', 'cancel']);

const categories = useCategoryStore();
const postCategory = async () => {
  if (!!category.value.id) {
    await categories.update(category.value);
  } else {
    await categories.create(category.value);
  }
  emit('categoryPosted');
}
</script>

<style lang="css" scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  gap: .3rem
}

.help {
  margin: 0;
  font-size: x-small;
  margin-top: -.5rem;
  color: var(--primary);
}
</style>
