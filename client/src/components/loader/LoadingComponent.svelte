<script lang="ts">
  export let loadingHeader: string = "Loading...";
  export let loadingMessage: string = "Please wait .";
</script>

<div class="container alert alert-info" role="alert">
  <strong> {loadingHeader}</strong>
  {loadingMessage}
</div>
