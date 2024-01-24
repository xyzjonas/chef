<template>
  <div class="level">
    <!-- success -->
    <ui-button v-if="success" disabled icon="fas fa-upload" />
    <ui-button v-else-if="error" :text="error" disabled />
    <div v-else>
      <!-- upload -->
      <ui-button v-if="file" @click="upload" icon="fas fa-upload" />

      <!-- choose file -->
      
      <ui-button v-else icon="fas fa-file" type="secondary">
        <label for="file">Choose a file</label>
      </ui-button>
      <input @change="handleFile" id="file" class="file-input" type="file" name="resume" >
    </div>
    <ui-button v-if="file" @click="file = undefined; error = undefined" icon="fa-solid fa-ban" />

  </div>
</template>

<script setup lang="ts">
import UiButton from './UiButton.vue';
import { API_URL } from '@/constants';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import type { Notification } from '@/types';

import { useEventBus } from '@vueuse/core';

const bus = useEventBus<Notification>("notifications")

// const send = useNotifications();

const props = defineProps(["recipe", "category", "small"]);
const file = ref();
const error = ref();
const success = ref();
const loading = ref();


const route = useRoute();
const itemId = parseInt(route.params.id as string);
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
      file.value = undefined;
      bus.emit({
        level: 'ERROR',
        message: "Wrong extension, only JPEG images are supported!"
      })
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

<style lang="css" scoped>
#file {
  display: none;
}

</style>