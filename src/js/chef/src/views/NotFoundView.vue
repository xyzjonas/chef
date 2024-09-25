<template>
    <main>

        <empty-box 
        title="404 | not found"
        subtitle="Sorry, we couldn't find this page."
        link-text="Go home"
        route-name="recipes"
        />
    </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import EmptyBox from '@/components/ui/EmptyBox.vue';

const { currentRoute } = useRouter()
</script>

<style lang="scss" scoped>

</style>