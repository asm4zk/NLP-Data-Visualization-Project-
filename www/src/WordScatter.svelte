<script>
    import { ScatterChart} from './new_data.js'
    import {onMount} from 'svelte'

    export let data2 = [];

    $: if(data2) console.log("WordScatter:$", data2);

    onMount(() => {
        let obj = ScatterChart(data2.command);
        console.log(obj)
        var options = {
          series: [{
          name: "title",
          data: obj.data2
          }],
          chart: {
          height: 350,
          type: 'scatter',
          zoom: {
            enabled: true,
            type: 'xy'
          }
        },
        xaxis: {
          tickAmount: 4,
          max: 3,
          labels: {
            formatter: function(val) {
              return parseFloat(val).toFixed(1)
            }
          }
        },
        yaxis: {
          tickAmount: 4,
          max:3.5,
          decimalsInFloat: true,
        }
        };

        var chart = new ApexCharts(document.querySelector("#word-scatter"), options);
        chart.render();
    })
</script>
<div id="word-scatter" />