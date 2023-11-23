<script lang="ts">
  import { CalenderEventEmojeTyoe } from "../../utils/enums";
  import type { eventNameType } from "../../utils/types";
  export let eventNames: Set<eventNameType>;

  function eventChanger(event: eventNameType) {
    if (eventNames.has(event)) {
      eventNames.delete(event);
      eventNames = new Set([...eventNames]);
    } else {
      eventNames.add(event);
      eventNames = new Set([...eventNames]);
    }
  }
</script>

<div class="card filter mt-4">
  <div class="card-title mt-4" style="margin-left: 15px;">
    <strong>Calendar Filters</strong>
    <br />
    <small>Click on any filter to hide the value of it from the calendar</small>
  </div>
  <div class="row align-items-center p-4">
    <div class="col-6 d-flex justify-content-start">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--danger hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger("meeting");
        }}
      >
        <span>Meetings {CalenderEventEmojeTyoe.meeting}</span>
        <span> {eventNames.has("meeting") ? "✔️" : "❌"} </span>
      </div>
    </div>
    <div class="col-6 d-flex justify-content-end">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--info hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger("event");
        }}
      >
        <span>Events {CalenderEventEmojeTyoe.event}</span>
        <span> {eventNames.has("event") ? "✔️" : "❌"} </span>
      </div>
    </div>
    <div class="col-6 d-flex mt-2 justify-content-start">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--warning hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger("vacation");
        }}
      >
        <span>Vacations {CalenderEventEmojeTyoe.vacation}</span>
        <span> {eventNames.has("vacation") ? "✔️" : "❌"} </span>
      </div>
    </div>
    <div class="col-6 d-flex mt-2 justify-content-end">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--success hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger("public_holiday");
        }}
      >
        <span>Public-Holidays {CalenderEventEmojeTyoe.publicHoliday}</span>
        <span> {eventNames.has("public_holiday") ? "✔️" : "❌"} </span>
      </div>
    </div>
    <div class="col-6 d-flex mt-2 justify-content-center">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--primary hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger("birthday");
        }}
      >
        <span>Birthday {CalenderEventEmojeTyoe.birthday}</span>
        <span> {eventNames.has("birthday") ? "✔️" : "❌"} </span>
      </div>
    </div>
  </div>
</div>

<style scoped>
  .hint-labels {
    cursor: pointer;
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 100%;
    text-align: center !important;
    font-weight: 600;
  }
</style>
