<script lang="ts">
  import { v4 as uuidv4 } from 'uuid';

  export let disabled = false;
  export let className = '';
  export let label = '';
  export let onClick: () => boolean | Promise<boolean>;
  export let successMessage: string;
  export let errorMessage: string;
  export let id = uuidv4();
  export let success: Promise<boolean> | boolean = true;
  export let show = false;
  let isLoading = false;
</script>

<button
  {id}
  type="submit"
  class={`btn ${className.length !== 0 ? className : 'submit'}`}
  on:click|preventDefault={async () => {
    isLoading = true;
    success = !(await onClick());
    show = true;
    isLoading = false;
  }}
  {disabled}
>
  {#if isLoading}
    <span
      class="spinner-border spinner-border-sm"
      role="status"
      aria-hidden="true"
    />
    Loading...
  {:else}
    {label}
  {/if}
</button>

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
      <small>1 sec ago</small>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="toast"
        aria-label="Close"
      />
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
