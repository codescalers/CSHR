<script lang="ts">
  import Input from "../input/Input.svelte";
  import Submit from "../submit/Submit.svelte";
  import ModalButton from "../modal/ModalButton.svelte";
  import Modal from "../modal/Modal.svelte";
  export let startDate: string;
  export let endDate: string;
  export let datePickerDisabled = false;
  let modalID = 11988731;
  let eventLocationValue: string;
  let eventNameValue: string;
  let eventDescriptionValue: string;
  let eventTimeValue: string;
  let eventNameIsError: boolean | null = null;
  let eventDescriptionIsError: boolean | null = null;
  let eventTimeIsError: boolean | null = null;
  let isLoading: boolean = false;
  let isError: boolean | null = null;

  // if true the disable submit button
  let locationIsError: boolean | null = null;
  $: fillDisabled =
    locationIsError === null || locationIsError === true || datePickerDisabled;
  $: submitDisabled =
    fillDisabled === true ||
    eventNameIsError === null ||
    eventNameIsError === true ||
    eventDescriptionIsError === null ||
    eventDescriptionIsError === true ||
    eventTimeIsError === null ||
    eventTimeIsError === true ||
    datePickerDisabled;
</script>

<div>
  <Input
    type="text"
    label={"Location"}
    bind:value={eventLocationValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={"please write proper location"}
    placeholder={"write event location"}
    bind:isError={locationIsError}
  />
  <ModalButton label="Fill" disabled={fillDisabled} {modalID} />
</div>

<Modal
  title="🎉 Event Form"
  body=""
  id={modalID}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={"Done"}
  deleteText={"Delete"}
>
  <form slot="form">
    <Input
      type="text"
      label={"Event Name"}
      bind:value={eventNameValue}
      handleInput={() => {
        return false;
      }}
      size={20}
      errorMessage="name is invalid"
      hint={"please write proper name"}
      placeholder={"write event name"}
      bind:isError={eventNameIsError}
    />
    <Input
      type="text"
      label={"Event Description"}
      bind:value={eventDescriptionValue}
      handleInput={() => {
        return false;
      }}
      size={20}
      errorMessage="Description is invalid"
      hint={"please write proper description"}
      placeholder={"write event description"}
      bind:isError={eventDescriptionIsError}
    />
    <Input
      type="time"
      label={"Event Time"}
      bind:value={eventTimeValue}
      handleInput={() => {
        return false;
      }}
      size={20}
      errorMessage="Time is invalid"
      hint={"please write proper Time"}
      placeholder={"write event time"}
      bind:isError={eventTimeIsError}
    />
  </form>
  <div slot="submit">
    <Submit
      label="Submit"
      onClick={() => {}}
      className="btn btn-primary"
      disabled={submitDisabled}
    />
  </div>
</Modal>
