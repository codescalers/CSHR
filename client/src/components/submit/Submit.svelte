<script lang="ts">
  import { v4 as uuidv4 } from 'uuid';

  export let disabled = false;
  export let className = '';
  export let label = '';
  export let onClick: () => boolean | Promise<boolean>;
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

<style>
  .submit:disabled {
    background-color: #e2e8f0;
    color: rgb(43 81 95);
  }
  .submit {
    font-size: 1rem;
    color: #000;
    background-color: var(--secondary-color);
    width: 100%;
    border: 1px solid var(--primary-color);
  }
  .submit:hover {
    background-color: var(--primary-color);
    color: #fff;
  }
  .success-bg {
    background-color: #d4edda;
    color: #155724;
  }
  .danger-bg {
    background-color: #fcb8b8;
    color: red;
  }
</style>
