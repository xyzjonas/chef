<template>
  <q-btn
    dense
    flat
    round
    icon="share"
    aria-label="Share recipe"
    size="sm"
    @click="share"
  />
</template>

<script setup lang="ts">
import { useQuasar } from "quasar";

const props = defineProps<{
  title: string;
}>();

const $q = useQuasar();

async function share() {
  const url = window.location.href;

  if (navigator.share) {
    try {
      await navigator.share({ title: props.title, url });
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        $q.notify({ type: "negative", message: "Could not share recipe" });
      }
    }
    return;
  }

  await navigator.clipboard.writeText(url);
  $q.notify({ type: "positive", message: "Link copied to clipboard" });
}
</script>
