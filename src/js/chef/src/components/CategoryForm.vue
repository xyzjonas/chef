<template>
  <div>
    <!-- title -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="category.name"
          :class="{
            input: true,
            'is-success': category.name,
            'is-danger': !category.name
          }"
          type="text"
          placeholder="Name"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-heading"></i>
        </span>
        <span v-if="category.name" class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </div>
      <p v-if="!category.name" class="help is-danger">Name is required</p>
    </div>

    <!-- tags -->
    <div class="field">
      <label class="label">Tags</label>
      <article v-if="tags.all.length < 1" class="message is-warning p-0">
        <small class="message-body p-2">no tags created yet</small>
      </article>
      <div class="control">
        <div>
          <a v-for="(tag, index) in tags.all" :key="`${tag},${index}`"
            @click="toggleTag(tag)"
          >
            <span
              :class="{
                tag: true,
                'is-dark': category.tags && category.tags.map(t => t.name).includes(tag.name),
                'is-rounded': true,
                'mr-1': true
              }"
            >
              {{ tag.name }}
            </span>
          </a>
        </div>
      </div>
    </div>

    <!-- BUTTONS -->
    <div class="my-5">     
      <div class="field is-grouped">
        <p class="control mr-1 is-expanded">
          <button
            class="button is-success mr-1"
            :disabled="!category.name"
            @click="postCategory"
          >
            <i class="fas fa-save"></i>
            <span class="ml-2">Save</span>
          </button>
          <button class="button" @click="$emit('cancel')">Cancel</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

const toggleTag = (tag: Tag) => {
  const tagNames = category.value.tags.map(t => t.name);
  if (!tagNames.includes(tag.name)) {
    category.value.tags.push(tag);
  } else {
    category.value.tags = category.value.tags.filter(tag => tag.name != tag.name)
  }
}

const emit = defineEmits(['categoryPosted']);
// const updateCategory = (category_id: number) => {
//   const path = `${Constants.HOST_URL}/categories/${category_id}`;
//   const options = {
//     headers: { 'Content-Type': 'application/json' },
//   };
//   axios
//     .put(path, this.category, options)
//     .then((res) => {
//       this.postSuccess = `${res.status} ${res.statusText}`;
//       this.$emit('categoryPosted', res.data);
//     })
//     .catch((err) => {
//       this.postError = err;
//     });
// }

const categories = useCategoryStore();
const postCategory = async () => {
  if (category.value.id) {
    await categories.update(category.value);
  }
  await categories.create(category.value);
  emit('categoryPosted');
}
</script>

<style>
  .fullwidth {
    width: 100%;
  }
</style>
