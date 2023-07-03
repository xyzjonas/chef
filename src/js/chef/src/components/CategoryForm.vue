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
        <span v-if="category.title" class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </div>
      <p v-if="!category.name" class="help is-danger">Name is required</p>
    </div>

    <!-- tags -->
    <div class="field">
      <label class="label">Tags</label>
      <article v-if="availableTags.length < 1" class="message is-warning p-0">
        <small class="message-body p-2">no tags created yet</small>
      </article>
      <div class="control">
        <div>
          <a v-for="(tag, index) in availableTags" :key="tag + index"
            v-on:click="toggleTag(tag)"
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
            v-on:click="postCategory"
          >
            <i class="fas fa-save"></i>
            <span class="ml-2">Save</span>
          </button>
          <button class="button" @click="$emit('cancel')">Cancel</button>
        </p>
      </div>
    </div>

    <!-- msg -->
    <article v-if="postSuccess" class="message is-success">
      <div class="message-body">{{ postSuccess }}</div>
    </article>
    <article v-if="postError" class="message is-danger">
      <div class="message-body">{{ postError }}</div>
    </article>
  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";

export default {
  props: ["inputCategory"],

  data() {
    return {
      availableTags: [],
      createTagField: null,

      postSuccess: null,
      postError: null,
      category: {
        tags: [],
      },
    };
  },
  methods: {

    toggleTag(tag) {
      const tagNames = this.category.tags.map(t => t.name)
      if (!tagNames.includes(tag.name)) {
        this.category.tags.push(tag);
      } else {
        this.category.tags = this.category.tags.filter(t => t.name != tag.name)
      }
    },

    getRootData() {
      axios.get(`${Constants.HOST_URL}/tags`)
        .then(res => {
          if (res.status !== "success") {
            this.availableTags = res.data;
          }
        })
        .catch((err) => this.error = err);

      axios.get(`${Constants.HOST_URL}/ingredients`)
        .then(res => {
          if (res.status !== "success") {
            this.ingredients = res.data.map(i => i.name);
          }
        })
        .catch((err) => this.error = err);
    },
    updateCategory(category_id) {
      const path = `${Constants.HOST_URL}/categories/${category_id}`;
      const options = {
        headers: { 'Content-Type': 'application/json' },
      };
      axios
        .put(path, this.category, options)
        .then((res) => {
          this.postSuccess = `${res.status} ${res.statusText}`;
          this.$emit('categoryPosted', res.data);
        })
        .catch((err) => {
          this.postError = err;
        });
    },
    postCategory() {
      if (this.category.id) {
        return this.updateCategory(this.category.id);
      }
      const path = `${Constants.HOST_URL}/categories`;
      const options = {
        headers: { 'Content-Type': 'application/json' },
      };
      axios
        .post(path, this.category, options)
        .then((res) => {
          this.postSuccess = `${res.status} ${res.statusText}`;
          this.$emit('categoryPosted', res.data);
          // setTimeout(() => this.$emit('categoryPosted', res), 500)
        })
        .catch((err) => {
          this.postError = err;
        });
    }
  },
  created() {
    if (this.inputCategory) {
      this.category = { ...this.inputCategory };
    }
    this.getRootData();
  },

};
</script>

<style>
  .fullwidth {
    width: 100%;
  }
</style>
