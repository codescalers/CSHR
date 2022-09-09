<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  export let startDate: string;
  export let endDate: string;
  let locationValue: any;
  let locationIsError: boolean | null;
  let disabled = true;
</script>

<div>
  <Input
    type="text"
    label={"Location"}
    bind:value={locationValue}
    handleInput={() => {
      return true;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={"please write proper location"}
    placeholder={"write event location"}
    bind:isError={locationIsError}
  />
  <Submit label="Submit" onClick={() => {}} {disabled} />
</div>
