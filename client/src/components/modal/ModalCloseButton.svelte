<script lang="ts">
  export let disabled = false
  export let className = ''
  export let label = ''
  export let onClick: () => void
  export let modalID: number
</script>

<button
  type="button"
  data-bs-dismiss="modal"
  data-bs-target={`#modal${modalID}`}
  aria-label="Close"
  class={`btn ${className.length !== 0 ? className : 'submit'}`}
  on:click|preventDefault={onClick}
  {disabled}>{label}</button
>

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
</style>
