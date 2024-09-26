<template>
  <a :href="href" class="light:text-dark dark:text-white text-lg">
    <q-icon name="link" size="1.6rem" class="mr-1"/>
    {{ label ? label : href }}
  </a>
</template>

<script setup lang="ts">
defineProps<{
    href: string
    label?: string
}>()
</script>

<style lang="css" scoped>
a {
    text-decoration: none
}

a:hover {
    text-decoration: underline;
}

.body--dark a {
    color: white;
}

.body--light a {
    color: var(--q-dark);
}
</style>
