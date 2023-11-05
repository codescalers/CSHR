<script lang="ts">
    import { v4 as uuidv4 } from 'uuid';
    import Toast from './Toast.svelte';
  
    export let disabled = false;
    export let className = '';
    export let label = '';
    export let onClick: () => boolean | Promise<boolean>;
    export let successMessage: string;
    export let errorMessage: string;
    export let id = uuidv4();
    export let success: Promise<boolean> | boolean = true;
    export let width:string = "100";

    let showToast = false;
    let isLoading = false;
  </script>
  
<button
    {id}
    type="submit"
    class="abtn {`${className.length !== 0 ? className : 'submit'}`}"
    style="width: {width}%;"
    on:click|preventDefault={async () => {
    isLoading = true;
    showToast = true;
    success = !(await onClick());
    isLoading = false;
    setTimeout(() => showToast = false, 4000)
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
  
{#if showToast}
    <Toast {successMessage} {errorMessage} {success} bind:show={showToast} />
{/if}

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
  