<template>
    <span :class="`star ${loading ? 'loading': ''}`" @click="$emit('favorite')">
        <span v-if="favorite">
            <i class="fa-solid fa-star"></i>
        </span>
        <span v-else>
            <i class="fa-regular fa-star"></i>
        </span>
    </span>
</template>

<script setup lang="ts">
const props = defineProps<{
    favorite: boolean,
    loading: boolean,
}>()
</script>

<style lang="scss" scoped>
@keyframes loading {
    0% {
        transform: rotate(0deg)
    }
    10% {
        transform: rotate(8deg)
    }
    30% {
        transform: rotate(-8deg)
    }
    40% {
        transform: rotate(0deg)
    }
    100% {
        transform: rotate(0deg)
    }
}
.star {
    font-size: x-large;
    color: goldenrod;

    &:hover {
        color: gold;
        cursor: pointer;
    }

    &.loading {
        animation-name: loading;
        animation-duration: 0.25s;
        animation-direction: alternate-reverse;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
    }

}
</style>