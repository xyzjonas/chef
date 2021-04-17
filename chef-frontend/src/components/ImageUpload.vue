<template>
  <div>
    <!-- success -->
    <div v-if="success">
      <button class="button is-success" disabled>
        <i class="fas fa-check"></i>
      </button>
    </div>
    
    <div v-else>
      <!-- upload -->
      <button v-if="file" v-on:click="upload" class="button is-success">
        <i class="fas fa-upload"></i>
      </button>

      <!-- choose file -->
      <div v-else class="file is-info">
        <label class="file-label">
          <input v-on:change="handleFile" id="file" class="file-input" type="file" name="resume">
          <span class="file-cta">
            <span class="file-icon">
              <i class="fas fa-image"></i>
            </span>
          </span>
        </label>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";


export default {
  props: ["recipe"],

  data() {
    return {
      file: null,
      error: null,
      success: null,
    };
  },

  methods: {

    handleFile() {
      this.file = document.querySelector("#file").files[0];
    },

    upload() {
      var formData = new FormData();
      formData.append("image", this.file);
      const url = `${Constants.HOST_URL}/recipes/${this.recipe.id}/image`;
      axios
        .post(url, formData, {
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

  }
}
</script>

<style>

</style>