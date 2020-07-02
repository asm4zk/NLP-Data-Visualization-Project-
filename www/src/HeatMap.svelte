<script>
    import {HeatmapChart} from './data3.js'
    import {onMount} from 'svelte'

    export let data3 =[];
    
    $: if(data3) console.log("HeatMap:$", data3); 
          
        onMount(() => {
        let obj = HeatmapChart(data3.command);
        console.log(obj)
            var options = {
                    series: obj.data3,
                    chart: {
                        height: 350,
                        type: 'heatmap',
                    },
                    dataLabels: {
                        enabled: false
                    },
                    colors: ["#008FFB", "#b19cd9","#ff0000","#008000"],
                    xaxis: {
                        type: 'value',
                        categories: obj.value,
                    },
                    title: {
                    text: 'HeatMap Chart (Different color shades for each series)'
                    },
                    grid: {
                    padding: {
                        right: 20
                    }
                    }
                    };

                    var chart = new ApexCharts(document.querySelector("#heatmap"), options);
                    chart.render();
})
</script>
<div id="heatmap" />