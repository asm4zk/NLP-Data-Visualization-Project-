<script>
    export let icon = "content_copy"
    export let label = "Used Space"
    export let value = "20/30"
    export let unit = "GB"
    export let color = "card-header-warning"

</script>
<div class="card card-stats">
    <div class="card-header { color } card-header-icon">
        <div class="card-icon">
        <i class="material-icons">{ icon }</i>
        </div>
        <p class="card-category"> { label }</p>
        <h3 class="card-title">{ value }
        <small>{ unit }</small>
        </h3>
    </div>
    <!--div class="card-footer">
        <div class="stats">
        <i class="material-icons text-danger">warning</i>
        <a href="javascript:;">Get More Space...</a>
        </div>
    </div-->
</div>