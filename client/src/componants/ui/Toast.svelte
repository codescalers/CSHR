<script lang="ts">
  export let successMessage: string;
  export let errorMessage: string;
</script>

<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1100">
  <div id="liveToast" class="toast" role="alert" style="display: block;">
    <div class="toast-header">
      {#if successMessage}
        <strong class="me-auto text-success success-bg fw-bold"> successfully submitted. </strong>
      {/if}

      {#if errorMessage}
        <strong class="me-auto text-danger danger-bg fw-bold"> an error occurred. please try again. </strong>
      {/if}
    </div>

    {#if successMessage}
      <div class="toast-body text-success success-bg fw-bold">
        {successMessage}
      </div>
    {/if}

    {#if errorMessage}
      <div class="toast-body text-danger danger-bg fw-bold">
        {errorMessage}
      </div>
    {/if}
  </div>
</div>

<style>
  .success-bg {
    background-color: #d4edda;
    color: #155724;
  }
  strong.success-bg {
    background-color: transparent;
  }
  .danger-bg {
    background-color: #fcb8b8;
    color: red;
  }
  strong.danger-bg {
    background-color: transparent;
  }
</style>
