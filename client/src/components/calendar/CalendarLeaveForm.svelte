<script lang="ts">
    import Submit from "../submit/Submit.svelte";
  // import Input from "../input/Input.svelte";
  export let startDate: string;
  export let endDate: string;
  let disabled = true;
  export let isLoading = false;
  export let isError = false;
</script>

<form>
  <Submit label="Submit" onClick={() => {}} {disabled} />
</form>
