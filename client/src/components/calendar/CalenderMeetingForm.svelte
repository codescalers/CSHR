<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  import PeopleSelect from "../select/PeopleSelect.svelte";
  export let startDate: string;
  export let endDate: string;

  let meetingLocationValue: string;
  let meetingLocationIsError: boolean | null;
  let disabled = true;
  export let isLoading = false;
  export let isError = false;
</script>

<form>
  <div class="form-group row">
    <label for="colFormLabel" class="col-sm-4 col-form-label py-3">People</label
    >
    <div class="col-sm-8">
      <PeopleSelect />
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
