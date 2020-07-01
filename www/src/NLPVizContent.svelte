<script>
    import NLPVizStats from './NLPVizStats.svelte'
    import NLPVizChart from './NLPVizChart.svelte'
    import NLPVizBar from './NLPVizBar.svelte'
    import NLPVizScatter from './NLPVizScatter.svelte'
</script>
<div class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-6">	
                <NLPVizStats icon="horizontal_split" label="Total Documents" value="1000" unit=""/>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-6">
                <NLPVizStats icon="horizontal_split" label="Total Results" value="100" unit= "docs" color="card-header-success"/>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-6">
                <NLPVizStats icon="label" label="Most frequent Lemma" value="Command&Conquer" unit="" color="card-header-danger"/>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="Titles by Frequency Score" description="These are the top documents in the query based on your search with the comparison of their TFIDF score" color="white"><NLPVizBar /></NLPVizChart>
            </div>
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 2" description="this is the description for test2" color="white"><NLPVizScatter /></NLPVizChart>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="danger">Hello World</NLPVizChart>
            </div>
            <div class="col-lg-6 col-md-6 col-sm-6">
                <NLPVizChart title="test 1" description="this is the description for test1" color="success">Hello World</NLPVizChart>
            </div>
        </div>
    </div>
</div>	
<style>
        
</style>