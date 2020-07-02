<script>
    import {BarChart} from "./data.js"
    import {onMount} from 'svelte'

    export let data = [];

    $: if(data) console.log("Worddistribution:$", data);

    onMount(() => {
        let obj = BarChart(data.command);
        let _data = data.command.map (value => value.score)
        var options = {
          series: [{
            name: obj.title,
            data: _data,
        }],
          chart: {
          type: 'bar',
          height: 400,
          width: '100%',
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },    
        },
        dataLabels: {
          enabled: false,

        },
        yaxis: {
          show: true,
          tickamount: 10,
          decimalsInFloat: true,
        },
        xaxis: {
          categories: obj.title,
          tickPlacement: 'on',
          title: {
            show: true,
            text: "Frequency Score",
          }
        },
        title:{
          text: "Document Titles by Frequency",
          align:'center',

        }
        
        


        };

        var chart = new ApexCharts(document.querySelector("#word-distribution"), options);
        chart.render();
});
  
</script>

<div id="word-distribution"></div>
