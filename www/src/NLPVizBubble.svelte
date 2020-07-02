<script> 
    import {BubbleChart} from './data.js'
    import {onMount} from 'svelte'


    export let data = [];
    
    $: if(data) console.log("NLPVizBubble:$", data);

    onMount(() => {
        let obj = BubbleChart(data.command);
        var options = {
          series: [{
          name: 'Title',
          data: obj.data
        }],
          chart: {
            height: 350,
            type: 'bubble',
    
        },
        dataLabels: {
            enabled: false,
        },
        plotOptions :{
            bubble: {
                minBubbleRadius: 5 
            }

        },
        fill: {
            opacity: 0.8
        },
        title: {
            text: 'Simple Bubble Chart'
        },
        xaxis: {
            max: 3.5,
            decimalsInFloat: true,
            labels: {
                formatter: function(val) {
                return parseFloat(val).toFixed(1)
                    }
        }
        },
        yaxis: {
            max: 3,
            tickAmount: 8,
            decimalsInFloat: true,
        }
        };

        var chart = new ApexCharts(document.querySelector("#nlpviz-bubble"), options);
        chart.render();

})
</script>
<div id="nlpviz-bubble"/>