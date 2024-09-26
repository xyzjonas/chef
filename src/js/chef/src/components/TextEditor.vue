<template>
  <div>
    <div class="editor-wrapper content">
      <div v-if="editor" class="q-btns mb-1">
        <q-btn
          flat
          @click="editor.chain().focus().setParagraph().run()"
          :class="{ 'is-active': editor.isActive('paragraph') }"
          :color="editor.isActive('paragraph') ? 'primary' : ''"
        >
          <q-icon name="segment" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleBold().run()"
          :disabled="!editor.can().chain().focus().toggleBold().run()"
          :class="{ 'is-active': editor.isActive('bold') }"
          :color="editor.isActive('bold') ? 'primary' : ''"
          
        >
          <q-icon name="format_bold" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleItalic().run()"
          :disabled="!editor.can().chain().focus().toggleItalic().run()"
          :class="{ 'is-active': editor.isActive('italic') }"
          :color="editor.isActive('italic') ? 'primary' : ''"
        >
          <q-icon name="format_italic" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleStrike().run()"
          :disabled="!editor.can().chain().focus().toggleStrike().run()"
          :class="{ 'is-active': editor.isActive('strike') }"
          :color="editor.isActive('strike') ? 'primary' : ''"
        >
          <q-icon name="strikethrough_s" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
          :color="editor.isActive('heading', { level: 1 }) ? 'primary' : ''"
        >
          H1
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
          :color="editor.isActive('heading', { level: 2 }) ? 'primary' : ''"
        >
          H2
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
          :color="editor.isActive('heading', { level: 3 }) ? 'primary' : ''"
        >
          H3
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleBulletList().run()"
          :color="editor.isActive('bulletList') ? 'primary' : ''"
        >
          <q-icon name="format_list_bulleted" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleOrderedList().run()"
          :color="editor.isActive('orderedList') ? 'primary' : ''"
        >
          <q-icon name="format_list_numbered" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().toggleBlockquote().run()"
          :color="editor.isActive('blockquote') ? 'primary' : ''"
        >
          <q-icon name="comment" />
        </q-btn>
        <q-btn flat @click="editor.chain().focus().setHorizontalRule().run()">
          <q-icon name="horizontal_rule" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().undo().run()"
          :disabled="!editor.can().chain().focus().undo().run()"
        >
          <q-icon name="undo" />
        </q-btn>
        <q-btn
          flat
          @click="editor.chain().focus().redo().run()"
          :disabled="!editor.can().chain().focus().redo().run()"
        >
          <q-icon name="redo" />
        </q-btn>
      </div>
      <editor-content :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";

import { onBeforeUnmount } from "vue";

const textUpdated = defineEmits(["editorUpdate"]);
const props = defineProps(["text"]);
const editor = useEditor({
  content: props.text,
  onUpdate: ({ editor }) => {
    textUpdated("editorUpdate", editor.getHTML());
  },
  extensions: [StarterKit],
});

onBeforeUnmount(() => editor.value?.destroy());
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
  q-btn {
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
