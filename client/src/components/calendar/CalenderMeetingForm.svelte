<script lang="ts">
  import Input from '../input/Input.svelte';
  import ModalOpenButton from '../modal/ModalOpenButton.svelte';
  import Submit from '../submit/Submit.svelte';
  //import ModalCloseButton from '../modal/ModalCloseButton.svelte';
  import Modal from '../modal/Modal.svelte';
  import PeopleSelect from '../select/PeopleSelect.svelte';
  import CalendarDataService from '../../services/axios/home/CalendarDataService';
  import { UserStore } from '../../stores';
  import type { SelectOptionType } from '../select/types';

  export let startDate: string;
  //export let endDate: string;

  // if true the disable submit button
  export let datePickerDisabled: boolean = false;
  const modalID = 129981;
  let meetingLocationValue: string;
  let meetingLocationIsError: boolean | null = null;
  let meetingLinkValue: string;
  let meetingLinkIsError: boolean | null = null;
  let meetingTimeValue: string;
  let meetingTimeIsError: boolean | null = null;

  let meetingPeopleIsError: boolean | null = false;
  export let isLoading: boolean = false;
  export let isError: boolean = false;

  let peopleSelected: SelectOptionType[] = [];
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
  const modalData = {
    'data-bs-dismiss': 'modal',
    'data-bs-target': `#modal${modalID}`,
    'aria-label': 'Close',
  };
</script>

<form>
  <PeopleSelect
    bind:isError={meetingPeopleIsError}
    bind:selected={peopleSelected}
  />
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
    <Submit
      successMessage={'Meeting is Scheduled'}
      errorMessage={' Meeting Submission Failed'}
      {modalData}
      label="Submit"
      onClick={async () => {
        isLoading = true;
        try {
          const invited_people = peopleSelected.map((person) =>
            Number(person.value)
          );
          await CalendarDataService.postMeeting({
            hostedUserID: $UserStore.id,
            date: startDate,
            invitedUsers: invited_people,
            location: meetingLocationValue,
            meetingLink: meetingLinkValue,
            time: meetingTimeValue,
          });
          isLoading = false;
          meetingLocationValue = '';
          meetingTimeValue = '';
          meetingLinkValue = '';
          peopleSelected = [];
        } catch (error) {
          isError = true;
        } finally {
          isLoading = false;
          meetingLocationValue = '';
          meetingTimeValue = '';
          meetingLinkValue = '';
          peopleSelected = [];
        }
        return isError;
      }}
      className="abtn btn-primary"
      bind:disabled={submitDisabled}
    />
  </div>
</Modal>

