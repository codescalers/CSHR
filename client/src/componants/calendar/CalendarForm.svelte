<script lang="ts">
  import CalendarMeetingForm from './forms/MeetingForm.svelte';
  import CalendarEventForm from './forms/EventForm.svelte';
  import CalendarLeaveForm from './forms/LeaveForm.svelte';
  import CalendarDatePicker from './CalendarDatePicker.svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let formToggle: number = 0;
  let thisDate: Date = new Date();
  let endDate: string;
  let startDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate()}`;
  const daysInCurrentMonth = getDaysInMonth(thisDate.getFullYear(), thisDate.getMonth() + 1);

  if (thisDate.getDate() + 2 > daysInCurrentMonth){
    endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 2}-${thisDate.getDate() + 2 - daysInCurrentMonth}`;
  } else {
    endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate() + 2}`;
  }
  
  let datePickerDisabled = false;
  let VacationCalculator: number;

  const handleVacationCalculator = (event: { detail: { text: number; }; }) => {
    VacationCalculator = event.detail.text;
  };

  function getDaysInMonth(year: number, month: number) {
    return new Date(year, month, 0).getDate();
  }
  
  </script>
  
  <div class="container">
    <CalendarDatePicker
      onlyStart={formToggle === 1}
      bind:startDate
      bind:endDate
      bind:datePickerDisabled
      on:message={handleVacationCalculator}
    >
      <div slot="toggler" class="my-4">
        <div class="options">
          <button
            class:active={formToggle === 0}
            on:click={() => {
              formToggle = 0;
            }}>Leave</button
          >
          <div class="separator" />
          <button
            class:active={formToggle === 1}
            on:click={() => {
              formToggle = 1;
            }}>Meeting</button
          >
          <div class="separator" />
          <button
            class:active={formToggle === 2}
            on:click={() => {
              formToggle = 2;
            }}>Event</button
          >
        </div>
      </div>
      <div slot="form">
        {#if formToggle === 0}
          <CalendarLeaveForm
            bind:startDate
            bind:endDate
            bind:datePickerDisabled
            calculatorValue = {VacationCalculator}
            on:message={(event) => {
              dispatch('message', {
                postedVacation: event.detail.postedVacation
              });
            }}
          />
        {/if}
        {#if formToggle === 1}
          <CalendarMeetingForm
            bind:startDate
            bind:datePickerDisabled
            on:message={(event) => {
              dispatch('message', {
                postedMeeting: event.detail.postedMeeting
              });
            }}
          />
        {/if}
  
        {#if formToggle === 2}
          <CalendarEventForm
            bind:startDate
            bind:endDate
            bind:datePickerDisabled
            on:message={(event) => {
              dispatch('message', {
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