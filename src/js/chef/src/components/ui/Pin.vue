<template>
  <span :class="clazz">{{ text }}</span>
</template>
<script lang="ts" setup>
import { computed } from "vue";

type Size = "small" | "normal";

type Props = {
  text: string;
  active?: boolean;
  clickable?: boolean;
  size?: Size;
};

const props = defineProps<Props>();

const clazz = computed(() => {
  let cls = `${props.size ?? "normal"} `;
  if (props.active) {
    cls += "active ";
  }

  if (props.clickable) {
    cls += "clickable hover:shadow dark:shadow-gray-5";
  }

  return cls;
});
</script>
<style lang="css" scoped>
span {
  background-color: #eee;
  color: var(--q-dark);
  border-radius: 1rem;
  text-decoration: none;
  transition: 0.1s ease-in-out;
}

.clickable {
  cursor: pointer;
}

.active {
  background-color: var(--primary);
  color: white;
}

.normal {
  font-size: 1rem;
  padding: 4px 12px;
}

.small {
  font-size: 0.7rem;
  padding: 4px 8px;
}
</style>
