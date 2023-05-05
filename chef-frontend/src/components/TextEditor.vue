<template>
  <div>
    <div class="editor-wrapper content">
        <!-- MENU -->
        <!-- <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
          <div class="menubar">
            <button
                class="menubar__button"
                :class="{ 'is-active': isActive.bold() }"
                @click="commands.bold"
            >
              <i class="fa fa-bold" aria-hidden="true"></i>
            </button>

            <button
              class="menubar__button"
              :class="{ 'is-active': isActive.italic() }"
              @click="commands.italic"
            >
              <i class="fa fa-italic" aria-hidden="true"></i>
            </button>
            
            <button
              class="menubar__button"
              :class="{ 'is-active': isActive.heading({ level: 3 }) }"
              @click="commands.heading({ level: 3 })"
            >
              <i class="fa fa-heading" aria-hidden="true"></i>
            </button>

            <button
              class="menubar__button"
              :class="{ 'is-active': isActive.ordered_list() }"
              @click="commands.ordered_list"
            >
              <i class="fa fa-list" aria-hidden="true"></i>
            </button>
          </div>
        </editor-menu-bar> -->

        <!-- EDITOR -->
        <editor-content :editor="editor"/>
    </div>
  </div>
</template>

<script setup lang="ts">
// import { Editor, EditorContent, EditorMenuBar } from '@tiptap/vue-3'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
// import { text } from 'stream/consumers';
// import { 
//   Blockquote,
//   CodeBlock,
//   HardBreak,
//   Heading,
//   HorizontalRule,
//   OrderedList,
//   BulletList,
//   ListItem,
//   TodoItem,
//   TodoList,
//   Bold,
//   Code,
//   Italic,
//   Link,
//   Strike,
//   Underline,
//   History,
// } from '@tiptap/vue-3'
const props = defineProps(["text"])
const editor = useEditor({
  content: props.text,
  // onUpdate: ({getHTML}) => { 
  //   $emit('editorUpdate', getHTML() );
  // }),
  extensions: [
    StarterKit,
  ],
})
// export default {
//   components: {
//     EditorContent,
//     EditorMenuBar,
//   },

//   props: ["text"],
//   data() {
//     return {
//       editor: new Editor({
//         content: this.text,
//         onUpdate: ({getHTML}) => { 
//           this.$emit('editorUpdate', getHTML() );
//           },
//         // extensions: [
//         //   new Blockquote(),
//         //   new BulletList(),
//         //   new CodeBlock(),
//         //   new HardBreak(),
//         //   new Heading({
//         //      levels: [1, 2, 3, 4, 5],
//         //      HTMLAttributes: {class: 'title'},
//         //   }),
//         //   new HorizontalRule(),
//         //   new ListItem(),
//         //   new OrderedList(),
//         //   new TodoItem(),
//         //   new TodoList(),
//         //   new Link(),
//         //   new Bold(),
//         //   new Code(),
//         //   new Italic(),
//         //   new Strike(),
//         //   new Underline(),
//         //   new History(),
//         // ]
//       }),
//     };
//   },
//   beforeDestroy() {
//     // Always destroy your editor instance when it's no longer needed
//     this.editor.destroy()
//   },
// };
</script>

<style>
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

/* .editor-wrapper ol {
  list-style: square;
  padding: 0 1em;
}

.editor-wrapper h1 {
  font-weight: bold;
  font-size: 1.5em;
} */

.editor-wrapper button {
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

.editor-wrapper button:hover {
  background-color: lightgray;
}

.editor-wrapper button.is-active  {
  background-color: darkgray;
  border-radius: 1px;
}
</style>