<template>
  <div v-if="recipe">

    <!-- title -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.title"
          :class="{
            input: true,
            'is-success': recipe.title,
            'is-danger': !recipe.title
          }"
          type="text"
          placeholder="Title"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-heading"></i>
        </span>
        <span v-if="recipe.title" class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </div>
      <p v-if="!recipe.title" class="help is-danger">
        Title is required
      </p>
    </div>

    <!-- sub-title -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.subtitle"
          class="input"
          type="text"
          placeholder="Subtitle"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-font"></i>
        </span>
      </div>
    </div>

    <!-- source (url) -->
    <div class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.source"
          class="input"
          type="text"
          placeholder="Source link"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-link"></i>
        </span>
      </div>
    </div>

    <!-- source (name) -->
    <div v-if="recipe.source" class="field">
      <div class="control has-icons-left has-icons-right">
        <input
          v-model="recipe.source_name"
          class="input"
          type="text"
          placeholder="Source name"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-link"></i>
        </span>
      </div>
    </div>

    <!-- idea only -->
    <label class="checkbox my-2">
      <input type="checkbox" v-model="recipe.draft" />
      Recipe idea
      <i class="far fa-lightbulb"></i>
    </label>

    <!-- ingredients -->
    <div v-if="!recipe.draft">
      <label class="label">Ingredients</label>
       <div class="field">
         <div class="control">
           <div class="tags">
              <span
                v-for="(i, index) in recipe.ingredients" :key="i+index"
                class="tag"
              >
              <p>{{ i.amount }}<strong>{{ i.unit.name }}</strong> {{ i.ingredient.name }}
              <span v-if="i.note">({{ i.note }})</span>
              </p>
              <button v-on:click="removeIngredient(i)" class="delete is-small"></button>
            </span>
           </div>
         </div>
        </div>

      <!-- smart field -->
      <div class="field has-addons my-0">
        <div
          :class="{
            dropdown: true,
            'is-active': smartFieldAutocomplete.length > 0,
            control: true,
            'is-expanded': true,
            'is-right': true,
            'has-icons-left': true
          }"
        >
          <input
            :class="{
              'is-danger': smartFieldError,
              'is-success': parsedSmartField && !smartFieldNewIngredient,
              'is-info': smartFieldNewIngredient
            }"
            v-model="addIngredientSmartField"
            @input="parseSmartField"
            @keyup="ingredientEnterPressed"
            class="input"
            type="text"
            placeholder="100g <ingredient>"
          />
          <span class="icon is-small is-left">
            <i class="fas fa-drumstick-bite"></i>
          </span>
          <div class="dropdown-menu fullwidth" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a v-for="(item, index) in smartFieldAutocomplete" :key="index"
              v-on:click="autocomplete(item)"
              class="dropdown-item">
                {{ item }}
              </a>
            </div>
          </div>
        </div>
      
        <p class="control">
          <button :class="{
            'button':true,
            'is-success':!smartFieldError,
            'is-danger':smartFieldError,
            'is-outlined':true
            }"
            :disabled=smartFieldError||!addIngredientSmartField
            v-on:click="confirmIngredient"
          >
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
          </button>
        </p>
      </div>
      <!-- smart field hint -->
      <p v-if="smartFieldError" class="help is-danger">
        {{ smartFieldError }}
      </p>
      <p v-if="smartFieldNewIngredient" class="help is-info">
        New ingredient will be added <strong>{{ smartFieldNewIngredient }}</strong>
      </p>
    </div>

    <!-- portions -->
    <!-- PORTIONS COUNTER -->
    <div class="mt-4">
      <Counter :initialValue="recipe.portions" @counterUpdate="updateCounter"/>
    </div>
    <label class="label has-text-centered">(1 batch)</label>

    <hr>

    <div v-if="!recipe.draft" class="field my-2">
      <div class="control">
        <TextEditor @editorUpdate="updateText" :text="recipe.body"></TextEditor>
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
                'is-dark': recipe.tags && recipe.tags.map(t => t.name).includes(tag.name),
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
    <div class="mb-5">
      <div class="field has-addons">
        <div class="control is-expanded">
          <input
            v-model="createTagField"
            class="input is-small is-rounded" type="text" placeholder="new tag"
          >
        </div>
        <div class="control ">
          <button v-on:click="createTag" class="button is-success is-small is-rounded">
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="my-1">
      <button
        v-on:click="postRecipe"
        class="button is-fullwidth is-success"
        :disabled="!recipe.title"
      >Save</button>
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
import TextEditor from "@/components/TextEditor.vue";
import Counter from "@/components/Counter.vue";

const getOr = (val, def) => {
  if(val) {
    return val;
  } else {
    return def;
  }
}

export default {
  props: ["recipe"],

  components: {
    TextEditor,
    Counter,
  },
  data() {
    return {
      addIngredientSmartField: null,
      smartFieldError: null,
      smartFieldAutocomplete: [],
      smartFieldNewIngredient: null,
      parsedSmartField: null,
      addIngredientNoteField: null,

      counter: 4,
      availableTags: [],
      createTagField: null,

      postSuccess: null,
      postError: null,

      ingredients: ["rice", "chicken", "penne"],
    };
  },
  methods: {
    updateCounter(val) {
      this.counter = val // why is this needed?
      this.recipe.portions = val
    },

    updateText(value) {
      // this.text = value;  // why is this needed?
      this.recipe.body = value;
    },

    autocomplete(value) {
      this.parseSmartField(value);
    },

    ingredientEnterPressed(event) {
      if (event.keyCode === 13) {
          this.confirmIngredient();
      } 
    },
    
    confirmIngredient() {
      this.recipe.ingredients.push(this.parsedSmartField);
      this.addIngredientSmartField = "";
      this.resetSmartField();
    },

    removeIngredient(ingredient) {
      this.recipe.ingredients = this.recipe.ingredients.filter(i => {
        return !(
          i.ingredient.name === ingredient.ingredient.name
          && i.amount === ingredient.amount
          && i.note === ingredient.note
        );
      });
    },

    resetSmartField() {
      this.smartFieldError = null;
      this.parsedSmartField = null;
      this.smartFieldAutocomplete = [];
      this.smartFieldNewIngredient = null;
      this.addIngredientNoteField = null;
    },

    toggleTag(tag) {
      var tagNames = this.recipe.tags.map(t => t.name)
      if (!tagNames.includes(tag.name)) {
        this.recipe.tags.push(tag);
      } else {
        this.recipe.tags = this.recipe.tags.filter(t => t.name != tag.name)
      }
    },

    createTag() {
      if (this.createTagField) {
        var tag = { name: this.createTagField }
        this.availableTags.push(tag);
        this.createTagField = null;
        this.recipe.tags.push(tag)
      }
    },

    filterAutocomplete(text) {
      var re = new RegExp(
        Constants.methods.replaceUnicode(text.toLowerCase()));

      return this.ingredients.filter(i => {
        var match = re.exec(
          Constants.methods.replaceUnicode(i.toLowerCase()))
        if (match) {
          return true;
        }
        return false;
      })
    },

    parseSmartField(prefill) {
      this.resetSmartField();

      // group 1 = amount, 2 = unit, 3 = name, 4 = note
      var re = /([\d.]+)([^\s\\/><)(}{]+)? +([^\\/><)(}{0-9]*) *(\([^\\/><)(}{]+\))?$/

      var match = re.exec(this.addIngredientSmartField);
      if (!match) {
        this.smartFieldError = "Expected format: <amount><unit> <item> (<note>)";
        return;
      }
      var amount = parseFloat(match[1]);
      var name = match[3].trim();
      var note = match[4];
      var unit = match[2];
      if (isNaN(amount)) {
        this.smartFieldError = `First item '${match[1]}' must be a number.`
      }

      if (typeof prefill === "string") {
        console.log(`prefill: ${prefill}`)
        console.log(`name: ${name}`)
        // this.addIngredientSmartField = this.addIngredientSmartField.replace(name, prefill);
        this.addIngredientSmartField = `${amount}${getOr(unit, "")} ${prefill} ${getOr(note, "")}`
        name = prefill;
      } else {
        this.smartFieldAutocomplete = this.filterAutocomplete(name);
      }

      if (note) {
        note = note.replace("(", "").replace(")", "");
      }

      if (!this.ingredients.includes(name)) {
        this.smartFieldNewIngredient = name;
      }

      this.parsedSmartField = {
        amount: amount,
        unit: {
          name: unit,
        },
        ingredient: {name: name},
        note: note,
      };
    },

    getRootData() {
      var path = `${Constants.HOST_URL}`;
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

    postRecipe() {
      const path = `${Constants.HOST_URL}/recipes/new`;
      const options = {
        headers: { 'Content-Type': 'application/json' },
      };
      axios.post(path, this.recipe, options)
        .then((res) => {
          this.postSuccess = `${res.status} ${res.statusText}`;
          this.$emit('recipePosted', res);
          // this.$router.push(to-the-new-recipe);
        })
        .catch((err) => {
          this.postError = err.response.data;
        });
    }
  },
  created() {
    this.getRootData();
    this.counter = this.recipe.portions;
  },

};
</script>

<style>
  .fullwidth {
    width: 100%;
  }
</style>
