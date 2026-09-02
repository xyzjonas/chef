<template>
  <div
    :class="[
      'flex flex-nowrap shrink-0 min-w-max whitespace-nowrap gap-1 items-center rounded border select-none transition-colors duration-150',
      size === 'large'
        ? 'text-base py-2 px-4 gap-2 min-h-[44px] justify-center'
        : size === 'fullsize'
          ? 'text-sm py-[2px] px-3'
          : 'text-xs px-2 py-[2px]',
      active
        ? 'bg-primary border-primary text-white'
        : 'bg-gray-1 border-gray-2 text-gray-6 dark:bg-gray-8 dark:border-gray-7 dark:text-gray-3',
      clickable ? 'cursor-pointer' : '',
      clickable && !active ? 'hover:border-primary' : '',
    ]"
  >
    <q-icon
      v-if="size === 'fullsize' || size === 'large'"
      :name="tag.icon ?? 'label'"
      :size="size === 'large' ? '20px' : '16px'"
      :class="active ? 'text-white' : 'text-gray-4'"
    />
    <span class="capitalize">{{ tag.name }}</span>
  </div>
</template>

<script setup lang="ts">
import type { Tag } from "@/types";

withDefaults(
  defineProps<{
    tag: Tag;
    size?: "small" | "fullsize" | "large";
    clickable?: boolean;
    active?: boolean;
  }>(),
  {
    size: "small",
    clickable: false,
    active: false,
  },
);
</script>
