<template lang="">
    <div class="mt-5">
        <div v-if="recipe.current" class="field is-grouped">
            <button class="button is-small mr-1 is-success is-rounded">
                <i class="fa-solid fa-check"></i>
                <span class="ml-2">planned</span>
            </button>
            <button
                class="button is-small is-rounded is-danger is-outlined"
                @click="$emit('cancel')"
            >
                <i class="fa-solid fa-ban"></i>
            </button>
        </div>
        <button v-else class="button is-small is-rounded" @click="$emit('plan')">
            <i class="fa-regular fa-calendar"></i>
            <span class="ml-2">plan</span>
        </button>
       
    </div>
</template>
<script setup>
defineProps(['recipe', 'loading'])
</script>
<style lang="">
    
</style>