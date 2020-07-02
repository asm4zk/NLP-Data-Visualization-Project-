<script> 
    import {BubbleChart} from './data4.js'
    import {onMount} from 'svelte'


    export let data4 = [];
    
    $: if(data4) console.log("WordBubbleKM:$", data4);

    onMount(() => {
        let obj = BubbleChart(data4.command);
        var options = {
          series: [{
          name: 'Title',
          data: obj.value,
        }],
          chart: {
            height: 500,
            type: 'bubble',
    
        },
        dataLabels: {
            enabled: false,
        },
        plotOptions :{
            bubble: {
                minBubbleRadius: 20 
            }

        },
        fill: {
            opacity: 0.8
        },
        title: {
            text: 'Simple Bubble Chart'
        },
        xaxis: {
            max: 10,
            tickAmount: 10,
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

        var chart = new ApexCharts(document.querySelector("#word-bubblekm"), options);
        chart.render();

})
</script>
<div id="word-bubblekm"/>