<script lang="ts">
  export let title: string = "";
  export let className: string;
  export let message: string;
  export let closable: boolean = false;
</script>

<div
  class="{`alert alert-${className}`} alert-dismissible fade show"
  role="alert"
>
  {#if title.length}
    <span><strong>{title}</strong></span>,
  {/if}
  {message}
  {#if closable}
    <button
      type="button"
      class="btn-close"
      data-bs-dismiss="alert"
      aria-label="Close"
    />
  {/if}
</div>

<style>
  .alert {
    margin-bottom: 0px;
  }
</style>
