<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  export let startDate: string;
  export let endDate: string;
  let locationValue: any;
  // if true the disable submit button
  export let datePickerDisabled = false;
  let locationIsError: boolean | null = null;
  let disabled: boolean = false;
  $: disabled =
    locationIsError === null || locationIsError === true || datePickerDisabled;
</script>

<div>
  <Input
    type="text"
    label={"Location"}
    bind:value={locationValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={"please write proper location"}
    placeholder={"write event location"}
    bind:isError={locationIsError}
  />
  <Submit label="Submit" onClick={() => {}} {disabled} />
</div>
