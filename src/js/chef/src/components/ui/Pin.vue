<template>
  <span :class="clazz">
    {{ text }}
  </span>
</template>
<script lang="ts" setup>
import { computed } from 'vue';

type Size = "small" | "normal"

type Props = {
    text: string
    active?: boolean
    clickable?: boolean
    size?: Size
}

const props = defineProps<Props>();

const clazz = computed(() => {
    return `${props.active ? 'active' : ''} ${props.size ?? 'normal'} ${props.clickable ? 'clickable' : ''}`
})
    

</script>
<style lang="css" scoped>
span {
    background-color: #eee;
    border-radius: 12px;

    text-decoration: none;


    transition: background-color 0.2s ease-in-out;

}

.clickable {
    cursor: pointer;
    &:hover {
        background-color: rgb(from var(--primary) r g b / 0.2);
        color: var(--text-inv);
    }

    &:hover, .active {
        background-color: rgb(from var(--primary) r g b / 0.9);
    }
}

.active {
    background-color: var(--primary);
    color: var(--text-inv);
}

.normal {
    font-size: 1rem;
    padding: 4px 12px;
}

.small {
    font-size: .7rem;
    padding: 4px 8px;
}


</style>
