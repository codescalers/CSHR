<script lang="ts">
  export let loadingHeader: string = "Loading...";
  export let loadingMessage: string = "Please wait .";
</script>

<div class="container alert alert-info" role="alert">
  <span
    class="spinner-border spinner-border-sm"
    role="status"
    aria-hidden="true"
  />
  <strong> {loadingHeader}</strong>
  {loadingMessage}
</div>
