<script lang="ts">
  import { createEventDispatcher } from "svelte";

  // import PeopleSelect from '../../ui/select/UsersMultiSelect.svelte';
  import CalendarDataService from "../../../apis/home/home";
  import { UserStore } from "../../../utils/stores";
  import type {
    calendarItemsType,
    SelectOptionType
  } from "../../../utils/types";
  import Submit from "../../ui/Button.svelte";
  import Input from "../../ui/Input.svelte";
  import ModalOpenButton from "../../ui/modals/ModalOpenButton.svelte";
  //import ModalCloseButton from '../modal/ModalCloseButton.svelte';
  import Modal from "../../ui/modals/SimpleModal.svelte";

  const today = new Date();
  export let startDate: string = `${today.getFullYear()}-${
    today.getMonth() + 1
  }-${today.getDate()}`;
  export let isError = false;
  export let datePickerDisabled = false;
  export let isLoading = false;

  // if true the disable submit button
  const modalID = 129981;

  let responseMeeting: calendarItemsType;
  const dispatch = createEventDispatcher();

  // let meetingLocationValue: string;
  // let meetingLocationIsError: boolean | null = null;
  let meetingLinkValue: string;
  let meetingLinkIsError: boolean | null = null;
  let meetingTimeValue: string;
  let meetingTimeIsError: boolean | null = null;

  let submitDisabled = true;
  let meetingPeopleIsError: boolean | null = false;
  let peopleSelected: SelectOptionType[] = [];

  $: fillDisabled =
    meetingPeopleIsError === null ||
    meetingPeopleIsError === true ||
    datePickerDisabled;

  $: submitDisabled =
    fillDisabled ||
    meetingLinkIsError === null ||
    meetingLinkIsError === true ||
    meetingTimeIsError === true ||
    meetingTimeIsError === null;

  let successMessage: string;
  let errorMessage: string;
</script>

<form>
  <!-- <PeopleSelect
        isTop={true}
        placeholder={"Select Users.."}
        bind:isError={meetingPeopleIsError}
        bind:selected={peopleSelected}
    /> -->
  <!-- <Input
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
    /> -->
  <div class="width-100 mt-4">
    <ModalOpenButton
      width={100}
      label="Fill"
      bind:disabled={fillDisabled}
      {modalID}
    />
  </div>
</form>

<Modal
  id={modalID + ""}
  isDelete={false}
  isDone={false}
  isFooter={true}
  doneText={"Done"}
  deleteText={"Delete"}
  isClose={true}
  on:close={() => {
    meetingTimeValue = "";
    meetingLinkValue = "";
    peopleSelected = [];
    isError = false;
    isLoading = false;
    meetingLinkIsError = false;
    meetingTimeIsError = false;
  }}
>
  <header slot="header">
    <h6>💼 Meeting Form</h6>
  </header>

  <form slot="form">
    {#if isLoading}
      <div class="alert alert-info" role="alert">
        <strong>Loading...</strong> Please wait.
      </div>
    {:else}
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
    {/if}
  </form>

  <div slot="submit">
    <Submit
      bind:successMessage
      bind:errorMessage
      label="Post Meeting!"
      onClick={async () => {
        isLoading = true;
        try {
          isError = false;
          // const invited_people = peopleSelected.map((person) =>
          //   Number(person.value)
          // );
          let time = meetingTimeValue;
          if (time.split(":")[0] == "00") {
            time.split(":")[0] = "12";
          }
          // location: meetingLocationValue,
          const axios = await CalendarDataService.postMeeting({
            hostedUserID: $UserStore.id,
            date: startDate,
            invitedUsers: [],
            location: "Remote",
            meetingLink: meetingLinkValue,
            time: time
          });
          successMessage = "The meeting was scheduled successfully.";
          isLoading = false;
          // meetingLocationValue = '';
          meetingTimeValue = "";
          meetingLinkValue = "";
          peopleSelected = [];

          responseMeeting = axios.data.results;
          dispatch("message", {
            postedMeeting: responseMeeting
          });
        } catch (error) {
          errorMessage = `Failed to schedule a new meeting due ${error}.`;
          isError = true;
        } finally {
          isLoading = false;
          // meetingLocationValue = '';
          meetingTimeValue = "";
          meetingLinkValue = "";
          peopleSelected = [];
        }
        return isError;
      }}
      bind:disabled={submitDisabled}
    />
  </div>
</Modal>
