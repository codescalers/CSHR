<script lang="ts">
  import Input from "../input/Input.svelte";
  let locationValue: any;
  let locationIsError: boolean | null;
</script>

<div>
<!--   <div class="form-group row">
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
  </div> -->
    <!--     <label for="colFormLabel" class="col-sm-4  col-form-label py-3"
      >Location</label
    >
    <div class="col-sm-8">
      <input
        type="text"
        class="form-control"
        id="colFormLabel"
        color="#EDF2F9"
      />
    </div>
 -->
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
</div>

<style>
  input[type="text"] {
    margin-top: 0.3cm;
    background-color: #edf2f9;
  } 
</style>
