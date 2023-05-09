<template>
  <div>
    <div class="editor-wrapper content">
      <div v-if="editor" class="buttons">
        <button @click="editor.chain().focus().setParagraph().run()" :class="{ 'is-active': editor.isActive('paragraph') }">
          <i class="fa fa-paragraph" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleBold().run()" :disabled="!editor.can().chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
          <i class="fa fa-bold" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleItalic().run()" :disabled="!editor.can().chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
          <i class="fa fa-italic" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleStrike().run()" :disabled="!editor.can().chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
          <i class="fa fa-strikethrough" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
          <i class="fa fa-heading" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
          <i class="fa fa-heading" aria-hidden="true"></i>2
        </button>
        <button @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
          <i class="fa fa-heading" aria-hidden="true"></i>3
        </button>
        <button @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }">
          <i class="fa fa-heading" aria-hidden="true"></i>4
        </button>
        <button @click="editor.chain().focus().toggleHeading({ level: 5 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }">
          <i class="fa fa-heading" aria-hidden="true"></i>5
        </button>
        <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
          <i class="fa fa-list-ul" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
          <i class="fa fa-list-ol" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'is-active': editor.isActive('codeBlock') }">
          <i class="fa fa-code" aria-hidden="true"></i>
        </button>
        <button @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'is-active': editor.isActive('blockquote') }">
          <i class="fa-solid fa-comment-dots"></i>
        </button>
        <button @click="editor.chain().focus().setHorizontalRule().run()">
          <i class="fa-solid fa-ruler-horizontal"></i>
        </button>
        <button @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().focus().undo().run()">
          <i class="fa-solid fa-rotate-left"></i>
        </button>
        <button @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().focus().redo().run()">
          <i class="fa-solid fa-rotate-right"></i>
        </button>
      </div>
      <editor-content :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'

import { onBeforeUnmount } from 'vue';

const textUpdated = defineEmits(['editorUpdate'])
const props = defineProps(["text"])
const editor = useEditor({
  content: props.text,
  onUpdate: ({ editor }) => { 
    textUpdated('editorUpdate', editor.getHTML() );
  },
  extensions: [
    StarterKit
  ],
})

onBeforeUnmount(() => editor.value?.destroy())
</script>

<style lang="scss">
.ProseMirror {
  padding-top: 0.5em;
  padding-left: 0.5em;
  padding-right: 0.5em;
  min-height: 10em;
  outline-color: darkgray;
  outline-style: dashed;
  outline-width: 1px;
}

.ProseMirror:focus {
  min-height: 10em;
  outline-color: black;
  outline-style: solid;
  outline-width: 1px;
}

.editor-wrapper {
  button {
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    flex: auto;

    &.is-active {
      background-color: darkgray;
      border-radius: 1px;
    }

    &:hover {
      background-color: lightgray; 
    }
  }
}

</style>