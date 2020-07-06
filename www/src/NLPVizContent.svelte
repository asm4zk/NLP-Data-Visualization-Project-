<script>
    export let serp = {};

    import NLPVizStats from './NLPVizStats.svelte'
    import NLPVizChart from './NLPVizChart.svelte'
    import NLPVizBar from './NLPVizBar.svelte'
    import WordDistribution from './WordDistribution.svelte'
    import NLPVizScatter from './NLPVizScatter.svelte'
    import NLPVizBubble from './NLPVizBubble.svelte'
    import WordScatter from './WordScatter.svelte'
    import TitlePie from './TitlePie.svelte'
    import HeatMap from './HeatMap.svelte'
    import WordBubbleKM from './WordBubbleKM.svelte'

    $: if (serp.data) console.log("NLPVizContent:$", serp);

    function findMainLemma(data) {
        let maxF = 0;
        let maxW = "";
        for (let item of data) {
            const f = item.frequency;
            if (f > maxF)  {
                maxF = f;
                maxW = item.word;
            }
        }
        return maxW;
    }

</script>

<div class="content">
    <div class="container-fluid">
        {#if serp.data !== undefined}
        <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-6">	
                <NLPVizStats icon="horizontal_split" label="Total Documents" value="{ serp.ncorpus }" unit=""/>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-6">
                <NLPVizStats icon="horizontal_split" label="Total Results" value="{serp.nserp}" unit= "docs" color="card-header-success"/>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-6">
                <NLPVizStats icon="label" label="Most frequent Lemma" value="{ findMainLemma(serp.data) }" unit="" color="card-header-danger"/>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="Titles by Frequency Score" description="These are the top documents in the query based on your search with the comparison of their TFIDF score" color="white">
                    <WordDistribution data={ serp.data } /> 
                </NLPVizChart>
            </div>
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 2" description="this is the description for test2" color="white">
                    <NLPVizScatter data={ serp.data } />
                </NLPVizChart>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="white">
                    <NLPVizBubble  data={serp.data} />
                </NLPVizChart>
            </div>
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="white">
                    <WordScatter data={serp.data} />
                </NLPVizChart>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="white">
                    <TitlePie data={serp.data} />
                </NLPVizChart>
            </div>
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="white">
                    <HeatMap data={serp.data} /> 
                </NLPVizChart>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="white">
                    <WordBubbleKM data={serp.data} />
                </NLPVizChart>
            </div>    
        
        </div>
        {/if}
    </div>
</div>	
<style>
        
</style>