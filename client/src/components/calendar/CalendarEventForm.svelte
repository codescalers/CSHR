<script lang="ts">
  import Input from '../input/Input.svelte';
  import ModalOpenButton from '../modal/ModalOpenButton.svelte';
  import ModalCloseButton from '../modal/ModalCloseButton.svelte';
  import Modal from '../modal/Modal.svelte';
  import PeopleSelect from '../select/PeopleSelect.svelte';
  import CalendarDataService from '../../services/axios/home/CalendarDataService';

  export let startDate: string;
  export let endDate: string;
  export let datePickerDisabled = false;
  let modalID = 11988731;
  let eventLocationValue: string;
  let eventNameValue: string;
  let eventDescriptionValue: string;
  let eventFromTimeValue: string;
  let eventEndTimeValue: string;
  let eventNameIsError: boolean | null = null;
  let eventDescriptionIsError: boolean | null = null;
  let eventFromTimeIsError: boolean | null = null;
  let eventEndTimeIsError: boolean | null = null;
  let eventPeopleIsError: boolean | null = null;

  let peopleSelected: number[] = [];
  let isLoading: boolean = false;
  let isError: boolean = false;

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
    eventFromTimeIsError === null ||
    eventFromTimeIsError === true ||
    datePickerDisabled ||
    eventEndTimeIsError === null ||
    eventEndTimeIsError === true ||
    peopleSelected.length === 0;
</script>

<div>
  <Input
    type="text"
    label={'Location'}
    bind:value={eventLocationValue}
    handleInput={() => {
      return false;
    }}
    size={20}
    errorMessage="location is invalid"
    hint={'please write proper location'}
    placeholder={'write event location'}
    bind:isError={locationIsError}
  />
  <ModalOpenButton label="Fill" disabled={fillDisabled} {modalID} />
</div>

<Modal
  id={modalID + ''}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={'Done'}
  deleteText={'Delete'}
>
  <header slot="header">
    <h6>🎉 Event Form</h6>
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
        label={'Event Name'}
        bind:value={eventNameValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="name is invalid"
        hint={'please write proper name'}
        placeholder={'write event name'}
        bind:isError={eventNameIsError}
      />
      <Input
        type="text"
        label={'Event Description'}
        bind:value={eventDescriptionValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Description is invalid"
        hint={'please write proper description'}
        placeholder={'write event description'}
        bind:isError={eventDescriptionIsError}
      />
      <div class="form-group row">
        <label for="colFormLabel" class="col-sm-4 col-form-label py-3"
          >People</label
        >
        <div class="col-sm-8">
          <PeopleSelect
            bind:isError={eventPeopleIsError}
            bind:selected={peopleSelected}
          />
        </div>
      </div>
      <Input
        type="time"
        label={'Event From Time'}
        bind:value={eventFromTimeValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Time is invalid"
        hint={'please write proper Time'}
        placeholder={'write event time'}
        bind:isError={eventFromTimeIsError}
      />
      <Input
        type="time"
        label={'Event End Time'}
        bind:value={eventEndTimeValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Time is invalid"
        hint={'please write proper Time'}
        placeholder={'write event time'}
        bind:isError={eventEndTimeIsError}
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
          await CalendarDataService.postEvent({
            description: eventDescriptionValue,
            end_time: eventEndTimeValue,
            location: eventLocationValue,
            name: eventNameValue,
            people: peopleSelected,
            end_date: endDate,
            from_date: startDate,
            from_time: eventFromTimeValue,
          });
        } catch (e) {
          isError = true;
        } finally {
          isLoading = false;
          eventDescriptionValue = '';
          eventEndTimeValue = '';
          eventLocationValue = '';
          peopleSelected = [];
        }
      }}
      className="btn btn-primary"
      disabled={submitDisabled}
    />
  </div>
</Modal>
