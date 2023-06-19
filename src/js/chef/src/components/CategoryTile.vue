<template>
  <div>
    <!-- EDIT -->
    <transition name="slide" mode="out-in">
    <CategoryForm
      v-if="edit"
      class="p-3"
      :inputCategory="category"
      @categoryPosted="edited"
      @cancel="edit = !edit"
    />
    <a
      v-else
      v-on:click="clicked"
      class="tile box is-child image-background clickable"
      :style="getTileStyle()"
    >
      <!-- title -->
      <p class="title tile-title">{{ category.name }}</p>

      <!-- TAGS -->
      <div class="tags my-0">
        <span class="mytag" v-for="(tag, index) in category.tags" :key="'category-tag-' + index">{{tag.name}}</span>
      </div>
      <!-- buttons -->
      <div class="level is-mobile mb-2">
        <div v-if="editable" class="level-item level-right">
          <p class="control mr-1">
            <ImageUpload
              :category=category :small="true"
              @uploadFailed="imageUploadFailed"
              @uploadSuccess="edited"
            />
          </p>
          <div class="mx-0">
            <button v-on:click="edit = !edit" class="button is-warning is-small is-rounded">
              <i class="fas fa-pen"></i>
            </button>
          </div>

          <DeleteButton @delete="deleteCategory" :small="true" :rounded="true"/>
          
        </div>
      </div>
      <span v-if="uploadError" class="help is-danger">
        Upload failed...
      </span>
      <!-- delete you sure? -->
      <span v-if="youSure" class="help is-danger">
        You absolutely sure you want to delete this category?
        <a v-on:click="deleteCategory">Yep, let's do this!</a>
      </span>
    </a>
    </transition>
    
  </div>
</template>

<script>
import axios from "axios";
import Constants from "@/components/Constants.vue";
import CategoryForm from "@/components/CategoryForm.vue";
import ImageUpload from "@/components/ImageUpload.vue";
import DeleteButton from "@/components/DeleteButton.vue";

export default {  

  data() {
    return {
      edit: false,
      youSure: false,
      uploadError: null,
    };
  },

  props: ["category", "editable"],

  components: { CategoryForm, ImageUpload, DeleteButton },

  methods: {

    imageUploadFailed(err) {
      this.uploadError = err;
    },

    clicked() {
      if (!this.editable) {
        this.$emit("clicked", this.category);
      }
    },

    edited() {
      this.edit = false;
      this.$emit("categoryEdited");
    },

    deleteCategory() {
      const path = `${Constants.HOST_URL}/categories/${this.category.id}`;
      axios
        .delete(path)
        .then((res) => {
          this.$emit('categoryDeleted', res);
        })
        .catch((err) => {
          this.postError = err;
        });
    },


    getRandomColor() {
      // storing all letter and digit combinations
      // for html color code
      var letters = "012345html6789ABCDEF";
    
      // html color code starts with #
      var color = '#';
    
      // generating 6 times as HTML color code consist
      // of 6 letter or digits
      for (var i = 0; i < 6; i++)
        color += letters[(Math.floor(Math.random() * 16))];
      return color;
    },

    getTileStyle() {
      return `background-image: url('${Constants.IMAGES_URL}/categories/${this.category.id}/landscape.jpeg');`
    }

  },

};
</script>

<style lang="scss" scoped>
  .disabled {
    pointer-events: none;
    cursor: default;
  }

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
    background-position: center;
    background-size: cover;
    border: 1px solid #888888;
    border-radius: 0.3em;
  }
  .tile-title {
    padding: 3px 10px;
    // background-color: #FFFFFFBB;
    width: fit-content;
    border-radius: 5px;
    text-shadow: 2px 2px 5px black;
    color: white;
  }
  .mytag {
    background-color: #FFFFFFBB;
    margin: 0.1em;
    border-radius: 0.2em;
    padding-left: 0.3em;
    padding-right: 0.3em;
    border: solid 1px #99999958;
  }

  .tile {
    min-height: 12em;
  }

  .noselect {
    -webkit-touch-callout: none; /* iOS Safari */
      -webkit-user-select: none; /* Safari */
      -khtml-user-select: none; /* Konqueror HTML */
        -moz-user-select: none; /* Firefox */
          -ms-user-select: none; /* Internet Explorer/Edge */
              user-select: none; /* Non-prefixed version, currently
                                    supported by Chrome and Opera */
  }
</style>
