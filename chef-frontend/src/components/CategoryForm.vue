<template>
  <div v-if="category">

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
      <p v-if="!category.name" class="help is-danger">
        Name is required
      </p>
    </div>

    <!-- source (url) -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="category.source"
          class="input"
          type="text"
          placeholder="image link"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-link"></i>
        </span>
      </div>
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
            class="button is-fullwidth is-success"
            :disabled="!category.name"
            v-on:click="postCategory"
          >
            <i class="fas fa-save"></i>
            <span class="ml-2">Save</span>
          </button>
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
  props: ["category"],

  data() {
    return {
      availableTags: [],
      createTagField: null,

      postSuccess: null,
      postError: null,
    };
  },
  methods: {

    toggleTag(tag) {
      var tagNames = this.category.tags.map(t => t.name)
      if (!tagNames.includes(tag.name)) {
        this.category.tags.push(tag);
      } else {
        this.category.tags = this.category.tags.filter(t => t.name != tag.name)
      }
    },

    getRootData() {
      var path = `${Constants.HOST_URL}/`;
      axios.get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.availableTags = res.data.tags;
            }
          }
        })
        .catch((err) => this.error = err);

      path = `${Constants.HOST_URL}/ingredients`;
      axios.get(path)
        .then(res => {
          if (res.status !== "success") {
            if (res.data) {
              this.ingredients = res.data.map(i => i.name);
            }
          }
        })
        .catch((err) => this.error = err);
    },

    postCategory() {
      const path = `${Constants.HOST_URL}/categories`;
      const options = {
        headers: { 'Content-Type': 'application/json' },
      };
      axios
        .post(path, this.category, options)
        .then((res) => {
          this.postSuccess = `${res.status} ${res.statusText}`;
          this.$emit('categoryPosted', res);
          // setTimeout(() => this.$emit('categoryPosted', res), 500)
        })
        .catch((err) => {
          this.postError = err;
        });
    }
  },
  created() {
    this.getRootData();
  },

};
</script>

<style>
  .fullwidth {
    width: 100%;
  }
</style>
