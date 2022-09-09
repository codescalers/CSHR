<script lang="ts">
  import Submit from "../submit/Submit.svelte";
  // import Input from "../input/Input.svelte";
  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let datePickerDisabled = false;
</script>

<form>
  <Submit label="Submit" onClick={() => {}} disabled={datePickerDisabled} />
</form>
