<template>
  <div class="container content timeline">

    <div
      v-for="(item, index) in items" :key="item+index"
      class="timeline-item" :date-is="item.date"
    >
      <h1>{{ item.recipe.title }}</h1>
      <p>{{ item.comment }}</p>
    </div>
    
  </div>
</template>

<script>
export default {
  props: [
    "items"
  ]
}
</script>
<!--
<style lang="scss">

.timeline {
	max-width: 1024px;
	width: 90%;
	margin: 0 auto;
}

$border-color: rgba(black, .3);

.timeline-item {
	padding: 3em 2em 2em;
	position: relative;
	color: rgba(black, .7);
	border-left: 2px solid $border-color;
	
	p {
		font-size: 1rem;
	}
	
	&::before {
		content: attr(date-is);
		position: absolute;
		left: 2em;
		font-weight: bold;
		top: 1em;
		display: block;
		font-family: 'Roboto', sans-serif;
		font-weight: 700;
		font-size: .785rem;
	}

	&::after {
		width: 10px;
		height: 10px;
		display: block;
		top: 1em;
		position: absolute;
		left: -7px;
		border-radius: 10px;
		content: '';
		border: 2px solid $border-color;
		background: white;
	}

	&:last-child {
		border-image: linear-gradient(
			to bottom,
			$border-color 60%,
			rgba($border-color, 0)) 1 100%
		;
	}
}
</style>
-->