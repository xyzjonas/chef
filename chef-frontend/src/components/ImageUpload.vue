<template>
  <div>
    <!-- success -->
    <div v-if="success">
      <button :class="{
          button: true, 'is-success': true, 'is-small': small, 'is-rounded': small
        }"
        disabled
      >
        <i class="fas fa-check"></i>
      </button>
    </div>
    
    <div v-else>
      <!-- upload -->
      <button v-if="file" v-on:click="upload"
        :class="{
          button: true, 'is-success': true, 'is-small': small, 'is-rounded': small
        }"
      >
        <i class="fas fa-upload"></i>
      </button>

      <!-- choose file -->
      <button v-else
        :class="{
          button: true, file: true, 'is-info': true, 'is-rounded': small, 'is-small': small
        }"
      >
        <span><i class="fas fa-upload"></i></span>
        <input v-on:change="handleFile" id="file" class="file-input" type="file" name="resume">
      </button>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";


export default {
  props: ["recipe", "category", "small"],

  data() {
    return {
      file: null,
      error: null,
      success: null,

      url: null,
    };
  },

  methods: {

    handleFile() {
      this.file = document.querySelector("#file").files[0];
    },

    upload() {
      var formData = new FormData();
      formData.append("image", this.file);
      axios
        .post(this.url, formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(res => {
          this.success = res;
          this.error = null;
          this.$emit("uploadSuccess", res);
        })
        .catch(err => {
          this.success = null;
          this.error = err;
          this.$emit("uploadFailed", err);
        })
    }

  },

  created() {
    if (this.category) {
      this.url = `${Constants.HOST_URL}/categories/${this.category.id}/image`;
    }
    if (this.recipe) {
      this.url = `${Constants.HOST_URL}/recipes/${this.recipe.id}/image`;
    }
  }
}
</script>

<style>

</style>