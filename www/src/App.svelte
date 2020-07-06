<script>
	import WordDistribution from './WordDistribution.svelte'
	import NLPVizNavbar from './NLPVizNavbar.svelte';
	import NLPVizContent from './NLPVizContent.svelte';

	let serp = {};

	function notify(e) {
		serp = e.detail;
		console.log("App:notify", serp);	
	}

</script>

<div class="wrapper">
	<div class="main-panel">
		<NLPVizNavbar on:nlpviz-serp={ notify }/>
		<NLPVizContent {serp} >
			<WordDistribution />
		</NLPVizContent>
	</div>
</div>

<style>
	:global(.main-panel) {
		width: 100%;
	}
</style>

