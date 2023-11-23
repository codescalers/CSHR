<script lang="ts">
  export let errorHeader = "Oh snap error has occurred!";
  export let errorMessage = "Change a few things up and try submitting again.";
</script>

<div class="container alert alert-danger" role="alert">
  <strong>{errorHeader}</strong>
  {errorMessage}
</div>
