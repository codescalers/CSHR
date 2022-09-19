<script lang="ts">
  import type { eventNameType } from "../../services/axios/home/types";
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

<div class="container d-flex flex-column gap-3 px-4 my-5">
  <div class="text-left">Details</div>
  <div
    class="task--danger t  d-flex flex-row justify-content-between"
    on:click={() => {
      eventChanger("meetings");
    }}
  >
    <span> 💼 Meeting </span>
    <span> {eventNames.has("meetings") ? "✔️" : "❌"} </span>
  </div>
  <div
    class="task--info t  d-flex flex-row justify-content-between"
    on:click={() => {
      eventChanger("events");
    }}
  >
    <span> 🎉 Event </span>
    <span> {eventNames.has("events") ? "✔️" : "❌"} </span>
  </div>
  <div
    class="task--warning t d-flex flex-row justify-content-between"
    on:click={() => {
      eventChanger("vacations");
    }}
  >
    <span> 🌴 Vacation </span>
    <span> {eventNames.has("vacations") ? "✔️" : "❌"} </span>
  </div>
  <div
    class="task--primary t d-flex flex-row justify-content-between"
    on:click={() => {
      eventChanger("birthdates");
    }}
  >
    <span> 🎂 Birthday </span>
    <span> {eventNames.has("birthdates") ? "✔️" : "❌"} </span>
  </div>
</div>

<style>
  .t {
    cursor: pointer;
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 10rem;
  }
</style>
