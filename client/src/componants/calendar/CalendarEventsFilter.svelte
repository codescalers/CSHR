<script lang="ts">
    import type { eventNameType } from '../../utils/types';
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
  
<div class="row align-items-center mt-4">
    <div class="col-6 d-flex justify-content-center mb-2">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="task--danger hint-labels d-flex flex-row justify-content-between"
        on:click={() => {eventChanger('meeting');}}
      >
        <span> 💼 Meeting </span>
        <span> {eventNames.has('meeting') ? '✔️' : '❌'} </span>
      </div>
    </div>
    <div class="col-6 d-flex justify-content-start mb-2">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--info hint-labels  d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger('event');
        }}
      >
        <span> 🎉 Event </span>
        <span> {eventNames.has('event') ? '✔️' : '❌'} </span>
      </div>
    </div>
    <div class="col-6 d-flex mb-4 justify-content-center">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--warning hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger('vacation');
        }}
      >
        <span> 🌴 Vacation </span>
        <span> {eventNames.has('vacation') ? '✔️' : '❌'} </span>
      </div>
    </div>
    <div class="col-6 d-flex mb-4 justify-content-start">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="task--primary hint-labels d-flex flex-row justify-content-between"
        on:click={() => {
          eventChanger('birthday');
        }}
      >
        <span> 🎂 Birthday </span>
        <span> {eventNames.has('birthday') ? '✔️' : '❌'} </span>
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