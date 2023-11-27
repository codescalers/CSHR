<script lang="ts">
  import Toast from "./Toast.svelte";

  export let disabled = false;
  export let className = "";
  export let label = "";
  export let onClick: () => boolean | Promise<boolean> | void | Promise<void>;
  export let successMessage: string | undefined = undefined;
  export let errorMessage: string | undefined = undefined;
  export let width = "100";

  let showToast = false;
  let isLoading = false;
</script>

<button
  type="submit"
  class="abtn {`${className.length !== 0 ? className : 'submit'}`}"
  style="width: {width}%;"
  on:click|preventDefault={async () => {
    isLoading = true;
    showToast = true;
    await onClick();
    isLoading = false;
    setTimeout(() => {
      showToast = false;
      successMessage = undefined;
      errorMessage = undefined;
    }, 4000);
  }}
  {disabled}
>
  {#if isLoading}
    <span
      class="spinner-border spinner-border-sm"
      role="status"
      aria-hidden="true"
    />
    Requesting...
  {:else}
    {label}
  {/if}
</button>

{#if (showToast && successMessage) || (showToast && errorMessage)}
  <Toast bind:successMessage bind:errorMessage />
{/if}

<style>
  .success-bg {
    background-color: #d4edda;
    color: #155724;
  }
  .danger-bg {
    background-color: #fcb8b8;
    color: red;
  }
</style>
