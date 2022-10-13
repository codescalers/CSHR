<script lang="ts">
  import type { eventNameType } from '../../services/axios/home/types';
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

  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<div class="row align-items-center">
  <div class="col-6 d-flex justify-content-center mb-2">
    <div class="task--danger hint-labels d-flex flex-row justify-content-between"
      on:click={() => {eventChanger('meetings');}}
    >
      <span> 💼 Meeting </span>
      <span> {eventNames.has('meetings') ? '✔️' : '❌'} </span>
    </div>
  </div>
  <div class="col-6 d-flex justify-content-start mb-2">
    <div
      class="task--info hint-labels  d-flex flex-row justify-content-between"
      on:click={() => {
        eventChanger('events');
      }}
    >
      <span> 🎉 Event </span>
      <span> {eventNames.has('events') ? '✔️' : '❌'} </span>
    </div>
  </div>
  <div class="col-6 d-flex mb-4 justify-content-center">
    <div
      class="task--warning hint-labels d-flex flex-row justify-content-between"
      on:click={() => {
        eventChanger('vacations');
      }}
    >
      <span> 🌴 Vacation </span>
      <span> {eventNames.has('vacations') ? '✔️' : '❌'} </span>
    </div>
  </div>
  <div class="col-6 d-flex mb-4 justify-content-start">
    <div
      class="task--primary hint-labels d-flex flex-row justify-content-between"
      on:click={() => {
        eventChanger('birthdates');
      }}
    >
      <span> 🎂 Birthday </span>
      <span> {eventNames.has('birthdates') ? '✔️' : '❌'} </span>
    </div>
  </div>
</div>

<style>
  .hint-labels {
    cursor: pointer;
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 10rem;
  }
</style>