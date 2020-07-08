<script>
    import {BarChart} from "./data.js"
    import {onMount} from 'svelte'

    export let data;
    let chart;

    //$: if(chart && data) console.log("Worddistribution:$", data);
    $: if(chart && data) data = drawData(data);

    let options = {
          series: [],
          chart: {
          type: 'bar',
          height: 400,
          width: '100%',
          stacked: true
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
          tickPlacement: 'on',
          title: {
            show: true,
            text: "Frequency Score",
          }
        },
        title:{
          text: "Lemmas by Score",
          align:'center',

          }
        };

    function drawData(data) {
        data = data.sort((a,b) => (a.score < b.score) ? 1 : -1);
        data = data.slice(0, Math.min(data.length, 10));
        let obj = BarChart(data);

        let options = {
            series: [
              {
                name: "Scores",
                data: obj.scores
              },
              {
                name: "Frequencies",
                data: obj.frequencies
              }
            ],
            xaxis: {
              categories: obj.lemmas
            }
        }

        chart.updateOptions(options);
        console.log("WordDistribution:drawdata", options)
        return data;
    }

    onMount(() => {
        chart = new ApexCharts(document.querySelector("#word-distribution"), options);
        chart.render();
    });
  
</script>

<div id="word-distribution"></div>
