<template>
    <span>
        <component :is="icon" :width="styleSize" id="icon"/>
        <input type="text" v-model="model" :class="clazz" />
    </span>
</template>

<script lang="ts" setup>
import { computed, type Component } from 'vue';

type Size = "small" | "normal" | "large"
const sizes: { [key: string]: string } = {
    small: "1rem",
    normal: "1.5rem",
    large: '2rem',
}


const model = defineModel()
const props = defineProps<{
    icon?: Component
    size?: Size
}>()

const clazz = computed(() => {
    return `${props.size ?? 'normal'}`
})

const styleSize = computed(() => sizes[props.size ?? 'normal'])
const styleAdditionalLeftPadding = computed(() => props.icon ? 'var(--size)' : '0')
</script>

<style lang="css" scoped>


span {
    position: relative;
    --size: v-bind("styleSize");
    --iconSize: calc(var(--size));

    & > #icon {
        position: absolute;
        width: var(--iconSize); 
        height: var(--iconSize);
        left: .5rem;
        top: calc(var(--size) / 3);
    }
}



input {
    -moz-box-sizing: border-box; 
    -webkit-box-sizing: border-box; 
     box-sizing: border-box; 
    
    display: block;
    outline: none;
    width: 100%;
    background-color: transparent;
    padding: calc(var(--size) / 3) calc(var(--size) / 3);
    padding-left: calc(var(--size) / 3 + v-bind("styleAdditionalLeftPadding") + 5px);
    font-size: calc(var(--size) - (var(--size) * 0.2));
    color: var(--text);

    background-color: #eeeeee;
    border: none;
    border-bottom: 1px solid var(--border);
}

input:focus {
    border-bottom: 1px solid #333333;;
}

</style>