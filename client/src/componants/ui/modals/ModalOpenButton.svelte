<script lang="ts">
    export let disabled = false;
    export let className = '';
    export let label = '';
    export let modalID: number;
    export let width: number;
  </script>
  
  <button
    type={'button'}
    style="width: {width}%;"
    class={`abtn ${className.length !== 0 ? className : 'submit'}`}
    data-bs-toggle={'modal'}
    data-bs-target={'#modal' + modalID}
    {disabled}>{label}</button
  >
