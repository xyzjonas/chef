<template>
    <label :for="randomId" id="wrapper" :data-focus="focused" >
        <component :is="icon" :width="styleSize" id="icon"/>
        <span>
            <input 
                ref="inputField"
                :id="randomId"
                type="text"
                v-model="model"
                :disabled="disabled"
                :class="clazz"
            />
            <label id="actualLabel" :for="randomId" v-if="label" :data-minimize="minimizeLabel">{{ label }}</label>
        </span>
    </label>
</template>

<script lang="ts" setup>
import { computed, type Component, ref } from 'vue';
import { useFocus } from '@vueuse/core'

const randomId = (Math.random() + 1).toString(36).substring(7);

type Size = "small" | "normal" | "large"
const sizes: { [key: string]: string } = {
    small: "1rem",
    normal: "1.5rem",
    large: '2rem',
}

const inputField = ref(null);
const { focused } = useFocus(inputField);

const modelNotEmpty = computed(() => model.value !== '' && model.value !== undefined && model.value !== null)
const minimizeLabel = computed(() => modelNotEmpty.value || focused.value)

const model = defineModel()
const props = defineProps<{
    icon?: Component
    size?: Size
    label?: string
    disabled?: boolean
    centered?: boolean
}>()

const clazz = computed(() => {
    return `${props.size ?? 'normal'}`
})

const styleSize = computed(() => sizes[props.size ?? 'normal'])
const textAlign = computed(() => props.centered ? 'center' : '')
// const styleAdditionalLeftPadding = computed(() => props.icon ? 'var(--size)' : '0')
</script>

<style lang="css" scoped>


#wrapper {
    --size: v-bind("styleSize");
    --iconSize: calc(var(--size));
    --fontSize: calc(var(--size) - (var(--size) * 0.2));
    --padding-y: calc(var(--size) / 1.8);
    --padding-x: calc(var(--size) / 3);

    display: flex;
    flex-direction: row;
    align-items: center;
    gap: .3rem;

    background-color: var(--bg-200);
    border-radius: 3px;
    /* border-bottom: 1px solid var(--border); */
    /* border-top-left-radius: 2px; */
    /* border-top-right-radius: 2px; */

    padding-inline: var(--padding-x);
    padding-bottom: var(--padding-y);
    padding-top: calc(var(--padding-y));

    transition: background-color .2s ease-in-out;

    cursor: text;
    overflow-x: auto;
}

#wrapper[data-focus="true"] {
    background-color: var(--bg-300);
}

input,
input:focus {
    color: var(--text);
    border: none;
    outline: none;
    background-color: transparent;
    width: 100%;
    padding: 0;
    font-size: var(--fontSize);
    text-align: v-bind("textAlign");

    & > text::after {
        content: "xxx";
    }
}

span {
    position: relative;
    flex: 2;
}

#actualLabel {
    position: absolute;
    left: 0;
    top: 0;
    font-size: var(--fontSize);
    transition: 0.1s ease-in-out;
    color: #888;

    cursor: text;
}

#actualLabel[data-minimize=true] {
    font-size: calc(var(--padding-y) * 1.3);
    top: calc(-1.2 * var(--padding-y));
    /* color: var(--bg-300); */
}

/* span {
    position: relative;
    --size: v-bind("styleSize");
    --iconSize: calc(var(--size));
    --fontSize: calc(var(--size) - (var(--size) * 0.2));

    & > #icon {
        position: absolute;
        width: var(--iconSize); 
        height: var(--iconSize);
        left: .5rem;
        top: calc(var(--size) / 3);
    }
    & > label {
        position: absolute;
        bottom: calc(0px + var(--fontSize) / 4);
        font-size: var(--fontSize);
        left: 0;
    }
} */

/* input {
    -moz-box-sizing: border-box; 
    -webkit-box-sizing: border-box; 
     box-sizing: border-box; 
    
    display: block;
    outline: none;
    width: 100%;
    background-color: transparent;
    padding: calc(var(--size) / 3) calc(var(--size) / 3);
    padding-left: calc(var(--size) / 3 + v-bind("styleAdditionalLeftPadding") + 5px);
    font-size: var(--fontSize);
    color: var(--text);

    background-color: #eeeeee80;
    border: none;
    border-bottom: 1px solid var(--border);
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;

    transition: background-color 0.3s ease-in-out;
} */

/* input:focus {
    border-bottom: 1px solid #333333;;
    background-color: #eeeeee;

    & + label {
        color: red;
    }
} */

</style>