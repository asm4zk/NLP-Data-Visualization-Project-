<script>
	import NLPVizNavbar from './NLPVizNavbar.svelte';
	import NLPVizContent from './NLPVizContent.svelte';

</script>

<div class="wrapper">
	<div class="main-panel">
		<NLPVizNavbar />
		<NLPVizContent />
	</div>
</div>

<style>
	:global(.main-panel) {
		width: 100%;
	}
</style>

