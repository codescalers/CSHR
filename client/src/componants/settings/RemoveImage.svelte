<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let label: string;
  export let buttonBackgraound: string;
  const dispatch = createEventDispatcher();

  let removed = false;
</script>

<div class="row">
  <div class="col-7 d-flex align-items-center">
    <label class="form-check-label" for="flexCheckDefault">{label}</label>
  </div>
  <div class="col-5 d-flex align-items-center justify-content-end">
    <button
      style="background: {buttonBackgraound};"
      on:click={() => {
        if (removed) {
          removed = false;
        } else {
          removed = true;
        }
        dispatch("message", {
          text: removed,
        });
      }}
    >
      {#if removed}
        Will Remove
        <span>✔️</span>
      {:else}
        Click to Remove
        <span>❌</span>
      {/if}
    </button>
  </div>
</div>

<style>
  button {
    padding: 10px;
    width: 80%;
    border-radius: 8px;
    color: rgb(255 255 255);
    border: 0;
    outline: 0;
  }
</style>
