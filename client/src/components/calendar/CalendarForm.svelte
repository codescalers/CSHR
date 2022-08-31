<script lang="ts">
  import CalendarLeaveForm from "./CalendarLeaveForm.svelte";
  import CalendarMeetingForm from "./CalenderMeetingForm.svelte";
  import CalendarEventForm from "./CalendarEventForm.svelte";
  import CalendarDatePicker from "./CalendarDatePicker.svelte";
  let formToggle:number = 0;
  
  </script>

<div class="container">
  <CalendarDatePicker />
  <div class="options">
    <button class:active={formToggle === 0} on:click={() => {formToggle = 0}}>Leave</button>
    <div class="separator" />
    <button class:active={formToggle === 1} on:click={ () => {formToggle = 1}}>Meeting</button>
    <div class="separator" />
    <button class:active={formToggle === 2} on:click={ () => {formToggle = 2}}>Event</button>
  </div>

  {#if formToggle === 0}
  <CalendarLeaveForm/>
  {:else}
	{#if formToggle === 1}
  <CalendarMeetingForm/>
	{:else}
  <CalendarEventForm/>
  {/if}
  {/if}
</div>

<style>
  .options {
    display: flex;
    justify-content: center;
    background-color: #EFF6FF;
    
    border-radius: 17px;
    padding: 0.1rem;
  }
  .options button {
    padding: 0.7rem 2rem;
    background-color: #EFF6FF;
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
