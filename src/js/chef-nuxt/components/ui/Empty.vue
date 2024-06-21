<template>
  <ui-card :class="{
    empty: true,
    dashed,
    'fixed-height': props.fixedHeight,
  }">
    <ui-spinner v-if="loading" type="roller" />
    <section class="flex flex-col items-center gap-2" v-else>
      <div id="icon" v-show="icon" :class="icon"></div>
      <div>
        <div class="title">{{ title }}</div>
        <div class="subtitle" v-show="subtitle">{{ subtitle }}</div>
      </div>
    </section>
  </ui-card>
</template>
<script setup lang="ts">
interface Props {
  loading?: boolean;
  icon?: string;
  title: string;
  subtitle?: string;
  dashed?: boolean;
  fixedHeight?: string;
}
const props = defineProps<Props>();

if (props.fixedHeight) {

}
</script>
<style lang="css" scoped>
.empty {
  display: grid;
  justify-content: center;
  align-content: center;
  text-align: center;
  height: 50dvh;
}

.title {
  font-size: 2rem;
  line-height: 2.5rem;
  font-weight: 500;
  text-transform: uppercase;
}

.subtitle {
  font-size: 1.2rem;
  /* filter: opacity(0.6); */
  font-weight: 300;
  text-transform: lowercase;
}

#icon {
  font-size: 3rem;
  color: var(--text-200);
  /* filter: opacity(.6); */
}

h1 {
  text-transform: uppercase;
}

@media (min-width: 576px) {
  .empty {
    height: 40rem;
  }
}

.fixed-height {
  height: v-bind('fixedHeight');
}
</style>
