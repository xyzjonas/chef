<template>
  <div>
    <!-- success -->
    <div v-if="success">
      <button :class="{
          button: true, 'is-success': true, 'is-small': small, 'is-rounded': small
        }"
        disabled
      >
        <i class="fas fa-upload"></i>
      </button>
    </div>
    <div v-else-if="error">
      <button
        @click="file = undefined; error = undefined"
        :class="{
          button: true,
          'is-danger': true,
          'is-small': small,
          'is-rounded': small
        }"
      >
        <i class="fa-solid fa-ban"></i>
      </button>
    </div>
    <div v-else>
      <!-- upload -->
      <button v-if="file" v-on:click="upload"
        :class="{
          button: true,
          'is-success': true,
          'is-small': small,
          'is-rounded': small,
          'is-loading': loading,
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
        <input @change="handleFile" id="file" class="file-input" type="file" name="resume">
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { API_URL } from '@/constants';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const props = defineProps(["recipe", "category", "small"]);
const file = ref();
const error = ref();
const success = ref();
const loading = ref();


const route = useRoute();
const itemId = parseInt(route.params.id);
const getURL = () => {
  if (props.category) {
    return `${API_URL}/images/categories/${itemId}`;
  }
  if (props.recipe) {
    return `${API_URL}/images/recipes/${itemId}`;
  }  
}
const url = getURL();

const handleFile = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length >= 1) {
    file.value = target.files[0];
    if (file.value.name.endsWith('.jpg') || file.value.name.endsWith('.jpeg')) {
      error.value = undefined;
    } else {
      error.value = "Wrong extension, only JPEG images are supported."
      console.error(error.value);
    }
  }
}

const emit = defineEmits(["uploadSuccess", "uploadFailed"]);
const upload = () => {
  loading.value = true;
  const formData = new FormData();
  formData.append("image", file.value);
  
  fetch(url, {
    method: 'POST',
    body: formData,
  }).then(res => {
        success.value = res;
        error.value = null;
        emit("uploadSuccess", res);
    })
    .catch(err => {
      success.value = null;
      error.value = err;
      emit("uploadFailed", err);
    })
    .finally(() => {
      loading.value = false;
    })
}
</script>

<style>

</style>