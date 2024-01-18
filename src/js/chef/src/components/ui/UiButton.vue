<template>
    <button :class="type">
        <span class="icon is-small">
            <i :class="icon"></i>
        </span>
        {{ text }}
    </button>
</template>
<script lang="ts" setup>
const props = defineProps<{
    type: "primary" | "link"
    icon: string,
    text: string,
}>()
</script>
<style lang="css" scoped>

.link {
    background-color: transparent;
    color: var(--text-inv);
}

.link:hover {
    background-color: rgb(from var(--primary) r g b / 0.8);
    background-color: oklch(from var(--primary) calc(l + 8) c h);
}

button {
    display: flex;
    flex-direction: row;
    align-content: center;
    gap: .3rem;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: .2rem;

    transition: 0.2s ease-in-out;
}
</style>