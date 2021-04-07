<template>
  <div class="home">
    <timeline :items="[
      { date:'31.3.2021', recipe:{title: 'Kachna'}, comment:'bylo to moc dobre' },
      { date:'31.3.2021', recipe:{title: 'CIZRNOVÝ GULÁŠ'} },
      { date:'31.3.2021', recipe:{title: 'OBĚD Z JEDNOHO HRNCE'} },
      { date:'31.3.2021', recipe:{title: 'BROKOLICOVÁ SEKANÁ Z KRŮTÍHO MASA'} },
    ]" />

    <recipe-form></recipe-form>
  </div>
</template>

<script>
import Timeline from "@/components/Timeline.vue";
import RecipeForm from "@/components/RecipeForm.vue";

export default {
  components: {
    Timeline,
    RecipeForm
  }
};
</script>
