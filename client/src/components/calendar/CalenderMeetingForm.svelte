<script lang="ts">
  import Input from "../input/Input.svelte";
  let meetingLocationValue: any;
  let meetingLocationIsError: boolean | null;
</script>

<form>
  <div class="form-group row">
    <label for="colFormLabel" class="col-sm-4 col-form-label py-3">People</label
    >
    <div class="col-sm-8">
      <input
        type="text"
        class="form-control"
        id="colFormLabel"
        color="#EDF2F9"
      />
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
</form>

<style>
  input[type="text"] {
    margin-top: 0.3cm;
    background-color: #edf2f9;
  }
</style>
