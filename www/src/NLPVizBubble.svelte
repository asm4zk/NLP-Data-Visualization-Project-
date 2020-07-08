<script> 
    import {BubbleChart} from './data.js'
    import {onMount} from 'svelte'


    export let data = [];
    export let algo = "lda"
    let chart;

    $: if(chart && data) data = drawData(data);

    var options = {
          series: [],
          chart: {
            height: 400,
            type: 'bubble',
    
        },
        dataLabels: {
            enabled: true,
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

    function drawData(data) {
        console.log("NLPVizBubble:drawData", data);
        let series = BubbleChart(data, algo);
        let options = {
            series: series
        }

        chart.updateOptions(options);
        return data;
    }

    onMount(() => {
        chart = new ApexCharts(document.querySelector(`#nlpviz-bubble-${algo}`), options);
        chart.render();

})
</script>
<div id="nlpviz-bubble-{algo}"/>