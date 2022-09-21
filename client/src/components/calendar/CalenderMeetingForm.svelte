<script lang="ts">
  import Input from '../input/Input.svelte';
  import ModalOpenButton from '../modal/ModalOpenButton.svelte';
  import ModalCloseButton from '../modal/ModalCloseButton.svelte';
  import Modal from '../modal/Modal.svelte';
  import PeopleSelect from '../select/PeopleSelectNotWorking.svelte';
  import CalendarDataService from '../../services/axios/home/CalendarDataService';
  import { UserStore } from '../../stores';

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
  export let isError: boolean = false;

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
    meetingTimeValue === undefined ||
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
    label={'Location'}
    bind:value={meetingLocationValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={'please write a valid location'}
    placeholder={'Meeting Location'}
    bind:isError={meetingLocationIsError}
  />
  <ModalOpenButton label="Fill" bind:disabled={fillDisabled} {modalID} />
</form>

<Modal
  id={modalID + ''}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={'Done'}
  deleteText={'Delete'}
  isClose={true}
>
  <header slot="header">
    <h6>💼 Meeting Form</h6>
  </header>

  <form slot="form">
    {#if isError}
      <div class="alert alert-danger" role="alert">
        <strong>Oh snap!</strong> Change a few things up and try submitting again.
      </div>
    {:else if isLoading}
      <div class="alert alert-info" role="alert">
        <strong>Loading...</strong> Please wait.
      </div>
    {:else}
      <Input
        type="text"
        label={'Meeting Link'}
        bind:value={meetingLinkValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Meeting Link is invalid"
        hint={'please write a valid link'}
        placeholder={'Meeting Link'}
        bind:isError={meetingLinkIsError}
      />
      <Input
        type="time"
        label={'Meeting Time'}
        bind:value={meetingTimeValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Meeting Time is invalid"
        hint={'please write a valid time'}
        placeholder={'Meeting Time'}
        bind:isError={meetingTimeIsError}
      />
    {/if}
  </form>

  <div slot="submit">
    <ModalCloseButton
      {modalID}
      label="Submit"
      onClick={async () => {
        isLoading = true;
        try {
          await CalendarDataService.postMeeting({
            hostedUserID: $UserStore.id,
            date: startDate,
            invitedUsers: peopleSelected,
            location: meetingLocationValue,
            meetingLink: meetingLinkValue,
            time: meetingTimeValue,
          });
          isLoading = false;
          meetingLocationValue = '';
          meetingTimeValue = '';
          meetingLinkValue = '';
          peopleSelected = [];
        } catch (e) {
          isError = true;
        } finally {
          isLoading = false;
          meetingLocationValue = '';
          meetingTimeValue = '';
          meetingLinkValue = '';
          peopleSelected = [];
        }
      }}
      className="btn btn-primary"
      bind:disabled={submitDisabled}
    />
  </div>
</Modal>
