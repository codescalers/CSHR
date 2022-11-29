<script lang="ts">
    import Input from '../../ui/Input.svelte';
    import ModalOpenButton from '../../ui/modals/ModalOpenButton.svelte';
    import Modal from '../../ui/modals/SimpleModal.svelte';
    import PeopleSelect from '../../ui/select/UsersMultiSelect.svelte';
    import type { SelectOptionType, calendarItemsType } from '../../../utils/types';
    import CalendarDataService from '../../../apis/home/home';
    import Submit from '../../ui/Button.svelte';
    import { createEventDispatcher } from 'svelte';
  
    export let startDate: string;
    export let endDate: string;
    export let datePickerDisabled = false;

    let responseEvent: calendarItemsType;
    const dispatch = createEventDispatcher();

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
  
    let peopleSelected: SelectOptionType[] = [];
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
      eventFromTimeIsError === true ||
      datePickerDisabled ||
      eventEndTimeIsError === true ||
      peopleSelected.length === 0;
  
    const modalData = {
      'data-bs-dismiss': 'modal',
      'data-bs-target': `#modal${modalID}`,
      'aria-label': 'Close',
    };
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
    <div class="width-100 mt-4">
        <ModalOpenButton width={100} label="Fill" disabled={fillDisabled} {modalID} />
    </div>
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
        <PeopleSelect
            isTop={true}
            bind:isError={eventPeopleIsError}
            bind:selected={peopleSelected}
        />
      {/if}
    </form>
    <div slot="submit">
      <Submit
        successMessage={eventNameValue + ' Event Submitted'}
        errorMessage={eventNameValue + ' Event Submission Failed'}
        {modalData}
        label="Post Event!"
        onClick={async () => {
          isLoading = true;
          try {
            let selected = peopleSelected.map((item) => Number(item.value));
            const axios = await CalendarDataService.postEvent({
              description: eventDescriptionValue,
              end_time: eventEndTimeValue,
              location: eventLocationValue,
              name: eventNameValue,
              people: selected,
              end_date: endDate,
              from_date: startDate,
              from_time: eventFromTimeValue,
            });
            responseEvent = axios.data.results
            dispatch('message', {
              postedEvent: responseEvent
            });
            // postedEvent
          } catch (error) {
            isError = true;
          } finally {
            isLoading = false;
            eventDescriptionValue = '';
            eventEndTimeValue = '';
            eventLocationValue = '';
            peopleSelected = [];
          }
          return isError;
        }}
        bind:disabled={submitDisabled}
      />
    </div>
  </Modal>
  