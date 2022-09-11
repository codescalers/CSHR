<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  import ModalButton from "../modal/ModalButton.svelte";
  import Modal from "../modal/Modal.svelte";
  import PeopleSelect from "../select/PeopleSelect.svelte";

  export let startDate: string;
  export let endDate: string;

  // if true the disable submit button
  export let datePickerDisabled: boolean = false;
  let modalID = 129981;
  let meetingLocationValue: string;
  let meetingLocationIsError: boolean | null = null;
  let meetingLinkValue: string;
  let meetingLinkIsError: boolean | null = null;
  let meetingTimeValue: string;
  let meetingTimeIsError: boolean | null = null;

  let meetingPeopleIsError: boolean | null = false;
  export let isLoading: boolean = false;
  export let isError: boolean | null = false;

  let peopleSelected: number[] = [];
  $: fillDisabled =
    meetingLocationIsError === null ||
    meetingLocationIsError === true ||
    meetingPeopleIsError === null ||
    meetingPeopleIsError === true ||
    datePickerDisabled ||
    peopleSelected.length === 0;
  let submitDisabled = true;
  $: submitDisabled =
    fillDisabled ||
    meetingLinkIsError === null ||
    meetingLinkIsError === true ||
    meetingTimeIsError === null ||
    meetingTimeIsError === true ||
    peopleSelected.length === 0;
</script>

<form>
  <div class="form-group row">
    <label for="colFormLabel" class="col-sm-4 col-form-label py-3">People</label
    >
    <div class="col-sm-8">
      <PeopleSelect
        bind:isError={meetingPeopleIsError}
        bind:selected={peopleSelected}
      />
    </div>
  </div>
  <Input
    type="text"
    label={"Location"}
    bind:value={meetingLocationValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={"please write a valid location"}
    placeholder={"Meeting Location"}
    bind:isError={meetingLocationIsError}
  />
  <ModalButton label="Fill" bind:disabled={fillDisabled} {modalID} />
</form>

<Modal
  id={modalID + ""}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={"Done"}
  deleteText={"Delete"}
  isClose={false}
>
  <header slot="header">
    <h6>💼 Meeting Form</h6>
  </header>
  <form slot="form">
    <Input
      type="text"
      label={"Meeting Link"}
      bind:value={meetingLinkValue}
      handleInput={() => {
        return false;
      }}
      size={20}
      errorMessage="Meeting Link is invalid"
      hint={"please write a valid link"}
      placeholder={"Meeting Link"}
      bind:isError={meetingLinkIsError}
    />
    <Input
      type="time"
      label={"Meeting Time"}
      bind:value={meetingTimeValue}
      handleInput={() => {
        return false;
      }}
      size={20}
      errorMessage="Meeting Time is invalid"
      hint={"please write a valid time"}
      placeholder={"Meeting Time"}
      bind:isError={meetingTimeIsError}
    />
  </form>
  <div slot="submit">
    <Submit
      label="Submit"
      onClick={() => {}}
      className="btn btn-primary"
      bind:disabled={submitDisabled}
    />
  </div>
</Modal>
