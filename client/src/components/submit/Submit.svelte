<script lang="ts">
  export let disabled = false;
  export let className = "";
  export let label = "";
  export let onClick: () => void;
</script>

<button
  type="submit"
  class={`btn submit ${className}`}
  on:click|preventDefault={onClick}
  {disabled}>{label}</button
>

<style>
  .submit:disabled {
    background-color: #e2e8f0;
    color: #a0aec0;
  }
  .submit {
    margin-top: 0.5cm;
    font-size: 16px;
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
