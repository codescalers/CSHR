<script lang="ts">
  import Loading from "../Loading.svelte";
  export let showModal: boolean = false;

  let isLoading: boolean = false;
  const displayLoading = () => {
    if (showModal) {
      document.getElementById("body-pd").style.overflow = "hidden";
    }
    isLoading = true;
    setTimeout(() => {
      isLoading = false;
    }, 200);
  };

  $: showModal, displayLoading();
</script>

<div
  class={`modal modal-lg fade overlay ${showModal === true ? "show" : ""}`}
  aria-hidden={!showModal}
  tabindex="-1"
  style={`display:${showModal === true ? "block" : "none"}`}
  aria-modal={showModal}
>
  {#if isLoading}
    <Loading className={"loader loading-no-transform"} />
  {:else}
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <slot name="header" />
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
            on:click={() => {
              document.getElementById("body-pd").style.overflow = "auto";
              showModal = false;
            }}
          />
        </div>
        <div class="modal-body">
          <slot name="body" />
        </div>
        <div class="modal-footer">
          <slot name="modal-footer" />
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .overlay {
    background: rgb(4 4 4 / 74%);
    overflow: hidden !important;
  }
</style>
