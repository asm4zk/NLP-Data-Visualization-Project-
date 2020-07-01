<script>
    export let title = "example";
    export let description = "this is a chart description"
    export let color = "success";
</script>


<div class="card card-chart">
<div class="card-header card-header-{ color }">
    <div class="ct-chart" id="dailySalesChart">
        <slot></slot>
    </div>
</div>
<div class="card-body">
    <h4 class="card-title">{ title }/</h4>
    <p class="card-category">
    <span class="text-success"> {description }</p>
</div>
<div class="card-footer">
    <div class="stats">
    <i class="material-icons">access_time</i> updated 4 minutes ago
    </div>
</div>
</div>

<style>
    .card-header-white {
        border: 1px solid #ddd;
        border-radius: 16px;
        background-color: white;
    }
    .card-title.svelte-p2mnt9 {
        font-weight: bold,
    }
    .text-sucess {
        color: blue,
    }

    
</style>