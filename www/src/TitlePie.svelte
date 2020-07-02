<script>
    import { BarChart} from './data.js'
    import {onMount} from 'svelte'

    export let data = [];

    $: if(data) console.log("TitlePie:$", data);

    onMount(() => {
        let obj = BarChart(data.command);
        let _data = data.command.map (value => value.score)
        var options = {
            series: _data,
            chart: {
            type: 'donut',
            },
            dataLabels :{
                enabled: false
            },
            labels: [
                ["Any Surface - Design concept.."],
                ["Celebrate 25 Years of the Classic.."],
                ["Burnout Paradise Remastered.."],
                ["Electronic Arts Launches 25.."],
                ["Command & Conquer: Rivals.."],
                ["Slice of Living 2019.."],
                ["GHOSTBUSTERS ROOKIE.."],
                ["Command & Conquer Remastered Collection.."],
                ["Electronic Arts Statement.."],
                ["EA Announces Command & Conquer.."]
            ],
            responsive: [{
                breakpoint: 480,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            show: false
                        }
                    }
                }]
            };

        var chart = new ApexCharts(document.querySelector("#Title-Pie"), options);
        chart.render();

})
</script>
<div id="Title-Pie"/>