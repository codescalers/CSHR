<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { formatDate } from "../../utils/helpers";
  import CalendarDatePicker from "./CalendarDatePicker.svelte";
  import CalendarEventForm from "./forms/EventForm.svelte";
  import CalendarLeaveForm from "./forms/LeaveForm.svelte";
  import CalendarMeetingForm from "./forms/MeetingForm.svelte";

  const dispatch = createEventDispatcher();

  let formToggle = 0;
  const today = new Date();
  const endAt = new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000); // 2 days later

  let startDate: string = formatDate(today);
  let endDate: string = formatDate(endAt);

  let vacationCalculator: number;

  const handleVacationCalculator = (event: { detail: { days: number } }) => {
    vacationCalculator = event.detail.days;
  };

  const updateDates = (event: { detail: { startDate: string, endDate: string } }) => {
    startDate = event.detail.startDate
    endDate = event.detail.endDate
  }
</script>

<div class="card mt-4">
  <CalendarDatePicker
    onlyStart={formToggle === 1}
    on:calculate={handleVacationCalculator}
    on:updateDates={updateDates}
    bind:startDate
    bind:endDate
  >
    <div slot="toggler" class="my-4">
      <div class="options">
        <button
          class:active={formToggle === 0}
          on:click={() => {
            formToggle = 0;
          }}
        >
          Leave
        </button>

        <div class="separator" />

        <button
          class:active={formToggle === 1}
          on:click={() => {
            formToggle = 1;
          }}
        >
          Meeting
        </button>

        <div class="separator" />

        <button
          class:active={formToggle === 2}
          on:click={() => {
            formToggle = 2;
          }}
        >
          Event
        </button>
      </div>
    </div>
    <div slot="form">
      {#if formToggle === 0}
        <CalendarLeaveForm
          bind:startDate
          bind:endDate
          calculatorValue={vacationCalculator}
          on:message={(event) => {
            dispatch("message", {
              postedVacation: event.detail.postedVacation
            });
          }}
        />
      {/if}

      {#if formToggle === 1}
        <CalendarMeetingForm
          bind:startDate
          on:message={(event) => {
            dispatch("message", {
              postedMeeting: event.detail.postedMeeting
            });
          }}
        />
      {/if}

      {#if formToggle === 2}
        <CalendarEventForm
          bind:startDate
          bind:endDate
          on:message={(event) => {
            dispatch("message", {
              postedEvent: event.detail.postedEvent
            });
          }}
        />
      {/if}
    </div>
  </CalendarDatePicker>
</div>

<style>
  .options {
    display: flex;
    justify-content: center;
    background-color: #eff6ff;

    border-radius: 0.5rem;
    padding: 0.1rem;
    width: fit-content;
    margin: auto;
  }
  .options button {
    padding: 0.7rem 2rem;
    background-color: #eff6ff;
    border: transparent;
    color: #7a7585;
  }
  .options .separator {
    width: 2px;
    background-color: #aaa;
    margin: 0.2rem;
  }

  .options .active {
    background-color: #2b515f;
    color: #eee;
    border-radius: 0.5rem;
  }
</style>
