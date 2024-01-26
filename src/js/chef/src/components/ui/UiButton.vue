<template>
    <button :class="type ?? 'primary'" :disabled="disabled" >
        <span class="icon" v-if="icon">
            <i :class="icon"></i>
        </span>
        {{ text ?? ""}}
        <slot />
    </button>
</template>
<script lang="ts" setup>
const props = defineProps<{
    type?: "primary" | "secondary" | "link"
    icon?: string,
    disabled?: boolean,
    text?: string,
}>()
</script>
<style lang="css" scoped>

.primary {
    color: var(--text-inv);
    background-color: var(--primary);

    & > .icon {
        color: var(--text-inv);
    }

    &:hover {
        background-color: var(--primary-transparent);
    }
}

span {
    height: 1rem;
}

.secondary {
    background-color: var(--bg-200);

    & > .icon {
        color: var(--text);
    }

    &:hover {
        background-color: var(--secondary);
    }
}

.icon {
    font-size: medium;
}

.link {
    background-color: transparent;
    color: var(--text-inv);
}

.link:hover {
    background-color: #ffffff33;
}

button {
    display: flex;
    align-items: center;
    justify-content: center;

    gap: .3rem;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: .2rem;

    min-width: 1.8rem;

    transition: 0.2s ease-in-out;
    user-select: none;
}

button:disabled {
    pointer-events: none;
    filter: opacity(.5);
}
</style>