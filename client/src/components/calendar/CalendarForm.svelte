<script lang="ts">
  import CalendarLeaveForm from "./CalendarLeaveForm.svelte";
  import CalendarMeetingForm from "./CalenderMeetingForm.svelte";
  import CalendarEventForm from "./CalendarEventForm.svelte";
  import CalendarDatePicker from "./CalendarDatePicker.svelte";
</script>

<div class="container">
  <CalendarDatePicker />
  <div class="options">
    <button value="leave" class="active">Leave</button>
    <div class="separator" />
    <button value="meeting">Meeting</button>
    <div class="separator" />
    <button value="event">Event</button>
  </div>

  <CalendarMeetingForm />
  <CalendarLeaveForm />
  <CalendarEventForm />
</div>

<style>
  .options {
    display: flex;
    justify-content: center;
    background-color: #d7e3f1;

    border-radius: 1%;
    padding: 0.2rem;
  }
  .options button {
    padding: 0.7rem 2rem;
    background-color: #d7e3f1;
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
