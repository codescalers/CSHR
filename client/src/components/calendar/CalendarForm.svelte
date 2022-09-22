<script lang="ts">
  import CalendarMeetingForm from './CalenderMeetingForm.svelte';
  import CalendarEventForm from './CalendarEventForm.svelte';
  import CalendarLeaveForm from './CalendarLeaveForm.svelte';
  import CalendarDatePicker from './CalendarDatePicker.svelte';
  let formToggle: number = 0;
  let startDate = '2022-03-01';
  let endDate = '2022-03-03';
  let datePickerDisabled = false;
</script>

<div class="container">
  <CalendarDatePicker
    onlyStart={formToggle === 1}
    bind:startDate
    bind:endDate
    bind:datePickerDisabled
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
        />
      {/if}
      {#if formToggle === 1}
        <CalendarMeetingForm
          bind:startDate
          bind:endDate
          bind:datePickerDisabled
        />
      {/if}

      {#if formToggle === 2}
        <CalendarEventForm
          bind:startDate
          bind:endDate
          bind:datePickerDisabled
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
