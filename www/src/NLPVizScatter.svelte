<script> 
  import {ScatterChart} from "./data.js"
  import {onMount} from 'svelte'

  export let data = [];
  
  $: if(data) console.log("TitleScatter:$", data);


  onMount(() => {
      let obj = ScatterChart(data.command);
      let title = obj.title
      console.log(obj)
      var options = {
            series: [{
            name: "title",
            data: obj.data,
            }],
            chart: {
              height: 350,
              width: '100%',
              type: 'scatter',
              zoom: {
                  enabled: true, 
                  type: 'xy'
              }
              },
              dataLabels :{
                  enabled: false
              },
              xaxis: {
                  type: 'titles',
                  tickAmount: 10,
              
                  labels: {
                      formatter: function(val) {
                      return parseFloat(val).toFixed(1)
                  }
              }
              },
              yaxis: {
              tickAmount: 7,
              decimalsInFloat: true
              },
      };

              var chart = new ApexCharts(document.querySelector("#title-scatter"), options);
              chart.render();
  });
</script>

<div id="title-scatter"></div>