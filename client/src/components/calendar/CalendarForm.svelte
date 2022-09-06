<script lang="ts">
  import CalendarMeetingForm from "./CalenderMeetingForm.svelte";
  import CalendarEventForm from "./CalendarEventForm.svelte";
  import CalendarDatePicker from "./CalendarDatePicker.svelte";
  let formToggle: number = 0;
  let formDisable = true;
</script>

<div class="container">
  <CalendarDatePicker onlyStart={formToggle === 1}>
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
      {#if formToggle === 1}
        <CalendarMeetingForm />
      {/if}

      {#if formToggle === 2}
        <CalendarEventForm />
      {/if}
      <button type="button" class="btn submit my-5" disabled={formDisable}
        >Submit</button
      >
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

  .submit {
    margin-top: 0.5cm;
    font-size: 16px;
    color: #2b515f;
    background-color: #eff6ff;
    width: 100%;
    border: none;
  }
  .submit:hover {
    background-color: #2b515f;
    color: #eee;
  }
</style>
