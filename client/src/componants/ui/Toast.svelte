<script lang="ts">
    export let successMessage: string;
    export let errorMessage: string;
    export let success: Promise<boolean> | boolean = true;
    export let show;
    
</script>
  
<div class="position-fixed bottom-0 end-0 p-3 " style="z-index: 1100">
  <div
    id="liveToast"
    class="toast"
    class:show
    role="alert"
    aria-live="assertive"
    aria-atomic="true"
  >
    <div class="toast-header">
      <strong
        class={`me-auto text-${
          success ? 'success success-bg' : 'danger danger-bg'
        } text-uppercase fw-bold `}
        >{success ? 'SuccessFully Submitted' : 'Error Occurred'}</strong
      >
    </div>
    <div
      class={`toast-body text-${
        success ? 'success success-bg' : 'danger danger-bg'
      } text-uppercase fw-bold `}
    >
      {success ? successMessage : errorMessage}
    </div>
  </div>
</div>
  
<style>
  .submit:disabled {
    background-color: #e2e8f0;
    color: #a0aec0;
  }
  .submit {
    font-size: 1rem;
    color: var(--primary-color);
    background-color: var(--secondary-color);
    width: 100%;
    border: 1px solid var(--primary-color);
  }
  .submit:hover {
    background-color: var(--primary-color);
    color: var(--secondary-color);
  }
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
  