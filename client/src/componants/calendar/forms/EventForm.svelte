<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import CalendarDataService from "../../../apis/home/home";
  // import PeopleSelect from '../../ui/select/UsersMultiSelect.svelte';
  import type { calendarItemsType } from "../../../utils/types";
  import { isValidDate } from "../../../utils/validations";
  import Submit from "../../ui/Button.svelte";
  import Input from "../../ui/Input.svelte";
  import ModalOpenButton from "../../ui/modals/ModalOpenButton.svelte";
  import Modal from "../../ui/modals/SimpleModal.svelte";

  export let startDate: string;
  export let endDate: string;
  export let datePickerDisabled = false;

  let responseEvent: calendarItemsType;
  const dispatch = createEventDispatcher();

  let modalID = 11988731;
  // let eventLocationValue: string;
  let eventNameValue: string;
  let eventDescriptionValue: string;
  let eventFromTimeValue: string;
  let eventEndTimeValue: string;
  let eventNameIsError: boolean | null = null;
  let eventDescriptionIsError: boolean | null = null;
  let eventFromTimeIsError: boolean | null = null;
  let eventEndTimeIsError: boolean | null = null;
  // let eventPeopleIsError: boolean | null = null;

  // let peopleSelected: SelectOptionType[] = [];
  let isLoading = false;
  let isError = false;

  // if true the disable submit button
  // let locationIsError: boolean | null = null;
  $: fillDisabled = !isValidDate(startDate) || !isValidDate(endDate);
  // locationIsError === null || locationIsError === true || datePickerDisabled;
  $: submitDisabled =
    // fillDisabled === true ||
    eventNameIsError === null ||
    eventNameIsError === true ||
    eventDescriptionIsError === null ||
    eventDescriptionIsError === true ||
    eventFromTimeIsError === true ||
    datePickerDisabled ||
    eventEndTimeIsError === true;
  // peopleSelected.length === 0;

  let successMessage: string;
  let errorMessage: string;
</script>

<div>
  <!-- <Input
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
    /> -->
  <div class="width-100 mt-4">
    <ModalOpenButton width={100} label="Fill" disabled={fillDisabled} {modalID} />
  </div>
</div>

<Modal
  id={modalID + ""}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={"Done"}
  deleteText={"Delete"}
  on:close={() => {
    eventNameValue = null;
    eventDescriptionValue = null;
    eventFromTimeValue = null;
    eventEndTimeValue = null;
    eventNameIsError = null;
    eventDescriptionIsError = null;
    eventFromTimeIsError = null;
    eventEndTimeIsError = null;
    isError = false;
  }}
>
  <header slot="header">
    <h6>🎉 Event Form</h6>
  </header>

  <form slot="form">
    {#if isLoading}
      <div class="alert alert-info" role="alert">
        <strong>Loading...</strong> Please wait.
      </div>
    {:else}
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
        label={"Event From Time"}
        bind:value={eventFromTimeValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Time is invalid"
        hint={"please write proper Time"}
        placeholder={"write event time"}
        bind:isError={eventFromTimeIsError}
      />
      <Input
        type="time"
        label={"Event End Time"}
        bind:value={eventEndTimeValue}
        handleInput={() => {
          return false;
        }}
        size={20}
        errorMessage="Time is invalid"
        hint={"please write proper Time"}
        placeholder={"write event time"}
        bind:isError={eventEndTimeIsError}
      />
      <!-- <PeopleSelect
            isTop={true}
            bind:isError={eventPeopleIsError}
            bind:selected={peopleSelected}
        /> -->
    {/if}

    {#if isError}
      <div class="mt-4 alert alert-danger" role="alert">
        <strong>Oh snap!</strong> Change a few things up and try submitting again.
      </div>
    {/if}
  </form>
  <div slot="submit">
    <Submit
      bind:successMessage
      bind:errorMessage
      label="Post Event!"
      onClick={async () => {
        isLoading = true;
        try {
          isError = false;
          // let selected = peopleSelected.map((item) => Number(item.value));
          // location: eventLocationValue,
          const axios = await CalendarDataService.postEvent({
            location: "",
            description: eventDescriptionValue,
            end_time: eventEndTimeValue,
            name: eventNameValue,
            people: [],
            end_date: endDate,
            from_date: startDate,
            from_time: eventFromTimeValue,
          });
          successMessage = "The new event has been posted successfully.";
          responseEvent = axios.data.results;
          dispatch("message", {
            postedEvent: responseEvent,
          });
        } catch (error) {
          errorMessage = "Error while trying to post a new event, please check your data and try again.";
          isError = true;
        } finally {
          isLoading = false;
          eventDescriptionValue = "";
          eventEndTimeValue = "";
          // eventLocationValue = '';
          // peopleSelected = [];
        }
        return isError;
      }}
      bind:disabled={submitDisabled}
    />
  </div>
</Modal>
