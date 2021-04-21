<template>
  <div class="tile is-parent">
    
    <div v-if="edit" style="width: 100%">
      <div class="level mb-1">
        <div class="level-item level-right">
          <a v-on:click="edit=!edit" class="tag is-delete"></a>
        </div>
      </div>
      <CategoryForm :category="category"/>
    </div>
    <a
      v-else
      v-on:click="clicked"
      class="tile is-child box clickable"
    >
      <button class="button is-success is-small is-fullwidth is-outlined">
        <i class="fas fa-plus"></i>
      </button>
    </a>
    
  </div>
</template>

<script>
import CategoryForm from "../components/CategoryForm.vue";

export default {  

  data() {
    return {
      edit: false,
      category: {
        tags: [],
      },
    };
  },

  components: {
    CategoryForm
  },

  methods: {
    clicked() {
      if (!this.editable) {
        this.$emit("clicked", this.category);
      }
    },

    deleteCategory() {

    }
  },

};
</script>

<style>
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
  .image-background {
    background-repeat: no-repeat;
    background-position: cover;
    background-size: cover;
    border: 1px solid #888888;
    border-radius: 0.3em;
  }
  .tile-title {
    background-color: #FFFFFFBB;
    width: fit-content;
    padding-left: 0.3em;
    padding-right: 0.3em;
    border-radius: 0.1em;
  }
  .mytag {
    margin: 0.1em;
    border-radius: 0.3em;
    padding-left: 0.2em;
    padding-right: 0.2em;
    background-color: #FFFFFFBB;
  }
</style>
