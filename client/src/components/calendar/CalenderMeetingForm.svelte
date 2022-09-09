<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  import PeopleSelect from "../select/PeopleSelect.svelte";
  export let startDate: string;
  export let endDate: string;

  // if true the disable submit button
  export let datePickerDisabled: boolean = false;

  let meetingLocationIsError: boolean | null = null;
  let meetingPeopleIsError: boolean | null = null;
  let meetingLocationValue: string;

  export let isLoading: boolean = false;
  export let isError: boolean | null = false;

  let disabled: boolean = true;
  $: disabled =
    (meetingLocationIsError === null || meetingLocationIsError === true) ||
    (meetingPeopleIsError === null || meetingPeopleIsError === true) ||
    datePickerDisabled;

</script>

<form>
  <div class="form-group row">
    <label for="colFormLabel" class="col-sm-4 col-form-label py-3">People</label
    >
    <div class="col-sm-8">
      <PeopleSelect bind:isError={meetingPeopleIsError} />
    </div>
  </div>
  <Input
    type="text"
    label={"Location"}
    bind:value={meetingLocationValue}
    handleInput={() => {
      return true;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={"please write omar"}
    placeholder={"please enter meeting location"}
    bind:isError={meetingLocationIsError}
  />
  <Submit label="Submit" onClick={() => {}} {disabled} />
</form>
