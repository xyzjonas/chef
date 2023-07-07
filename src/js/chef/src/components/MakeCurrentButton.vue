<template>
    <span :class="`star ${loading ? 'loading': ''}`" @click="$emit('favorite')">
        <span v-if="recipe.favorite">
            <i class="fa-solid fa-star"></i>
        </span>
        <span v-else>
            <i class="fa-regular fa-star"></i>
        </span>
    </span>
</template>
<script setup>
defineProps(['recipe', 'loading'])
</script>
<style lang="scss" scoped>
@keyframes loading {
    from {
        transform: rotate(-100deg)
    }
    to {
        transform: rotate(100deg)
    }
}
.star {
    font-size: x-large;
    color: goldenrod;
    transform: rotate(0deg);
    transition: all 1s;

    &:hover {
        color: gold;
        cursor: pointer;
    }

    &.loading {
        animation-name: loading;
        animation-duration: 0.3s;
        animation-direction: alternate-reverse;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
    }

}
</style>