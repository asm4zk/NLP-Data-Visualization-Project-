<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let query = "";
    let sid = "";
    let serp = {};

    function notify(serp) {
        console.log("NLPVizNavBar:notify", serp)
        dispatch("nlpviz-serp", serp)
        query = "";
    }

    async function search(rerun) {
        serp = {};
        console.log("NLPVizNavBar:search", query);
		const res = await fetch(`http://localhost:18080/search?query=${query}&rerun=${rerun}`);
        sid = await res.text();
        
        let i = setInterval(() => {
            if (serp["data"] === undefined)
                status()
            else {
                clearInterval(i);
            }
            notify(serp);
        }, 1000);

		console.log("NLPVizNavBar:search", sid);
    }

    async function status() {
        console.log("NLPVizNavBar:status", sid);
        const res = await fetch(`http://localhost:18080/status?sid=${sid}`);
        serp = await res.json();
        console.log("NLPVizNavBar:search", serp)
    }
    

</script>
<nav class="navbar navbar-expand-lg navbar-transparent navbar-absolute fixed-top ">
    <div class="container-fluid">
        <div class="navbar-wrapper">
            <p class="navbar-brand">Dashboard</p>
            </div>
            <div class="collapse navbar-collapse justify-content-end">
            <div class="navbar-form">
                <span class="bmd-form-group">
                    <div class="input-group no-border">
                        <input style="width:320px" type="text" bind:value={query} class="form-control" placeholder="Search...">
                        <button class="btn btn-white btn-round btn-just-icon" on:click={() => search(false)} on:dblclick={() => search(true)}>
                            <i class="material-icons">search</i>
                            <div class="ripple-container"></div>
                            <div class="ripple-container"></div>
                        </button>
                    </div>
                </span>
            </div>
        </div>
    </div>
</nav>