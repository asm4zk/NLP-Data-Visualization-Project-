<script>
    export let status = 0;
    export let info = ""
</script>
<div class="progress">
  <div class="progress-bar" role="progressbar" style="width: {status}%" aria-valuenow="{status}" aria-valuemin="0" aria-valuemax="100">{info}</div>
</div>