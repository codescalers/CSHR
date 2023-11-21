<script lang="ts">
  import type { calendarItemsType } from "../../../utils/types";
  import CalendarModal from "./CalendarModal.svelte";
  import { CalenderEventEmojeTyoe } from "../../../utils/enums";
  import { onMount } from "svelte";

  export let showModal: boolean = false;
  export let clickedItemOnModal: calendarItemsType;

  function getHolidayClass(holiday) {
    return holiday.expired ? "expired" : "";
  }

</script>

<CalendarModal bind:showModal>
  <header slot="header" class="text-center w-100">
    <h6 class="modal-title" id="exampleModalLongTitle">
      <strong>
        {clickedItemOnModal.date} is a public holiday {CalenderEventEmojeTyoe.publicHoliday}
        in {#each clickedItemOnModal.holidays as holiday}
          <strong>{holiday.location.country + ", "}</strong>
        {/each}
      </strong>
    </h6>
  </header>

  <div slot="body" class="card bg-confetti-animated">
    <div class="card-title title p-4 text-center">
      {#each clickedItemOnModal.holidays as holiday, index}
        <strong class={getHolidayClass(holiday)}>
          {holiday.location.country.trimEnd()}
        </strong>
        {#if clickedItemOnModal.holidays.length > 1 && index + 1 != clickedItemOnModal.holidays.length}
          <strong><small class="--and">& </small></strong>
        {/if}
      {/each}
    </div>

    <div class="card-body body">
      {clickedItemOnModal.date} is a public holiday in
      {#each clickedItemOnModal.holidays as holiday}
        <strong>{holiday.location.country + ", "}</strong>
      {/each}

      We hope you and your family have a peaceful and enjoyable holiday.
      <strong>Please be aware</strong> that our
      {clickedItemOnModal.holidays.length > 1 ? "offices" : "office"} in
      {#each clickedItemOnModal.holidays as holiday}
        <strong>{holiday.location.country + ", "}</strong>
      {/each}
      will be closed on this date.

      <strong>Thank you! :)</strong>
    </div>
  </div>

  <div slot="modal-footer">
    <button
      type="button"
      class="abtn btn-secondary"
      on:click={() => {
        document.getElementById("body-pd").style.overflow = "auto";
        showModal = false;
      }}>Close</button
    >
  </div>
</CalendarModal>

<style scoped>
  .--and {
    margin-left: 3px;
    margin-right: 3px;
    color: coral;
  }

  .title {
    background: #f5f5dce0;
    margin: 10px;
    font-size: 23px;
  }

  .body {
    margin-top: 15px;
    margin-bottom: 15px;
    padding: 20px;
    border: 1px solid #e2e0e2;
    margin-left: 10px;
    margin-right: 10px;
    border-left-width: 15px;
    border-left: inset;
  }

  .expired {
    background-color: #9d0d0d80;
    padding: 6px;
    border-radius: 5px;
    color: wheat;
  }

  .bg-confetti-animated {
    background-repeat: repeat-x;
    background-position: top -10px center;
    background-image: url("data:image/svg+xml,%3Csvg width='600' height='90' viewBox='0 0 600 90' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='42' y='-10' width='6' height='10'/%3E%3Crect x='84' y='-10' width='6' height='10'/%3E%3Crect x='126' y='-13' width='5' height='13'/%3E%3Crect x='168' y='-13' width='5' height='13'/%3E%3Crect x='210' y='-10' width='6' height='10'/%3E%3Crect x='252' y='-13' width='5' height='13'/%3E%3Crect x='294' y='-10' width='6' height='10'/%3E%3Crect x='336' y='-13' width='5' height='13'/%3E%3Crect x='378' y='-13' width='5' height='13'/%3E%3Crect x='420' y='-10' width='6' height='10'/%3E%3Crect x='462' y='-10' width='6' height='10'/%3E%3Crect x='504' y='-13' width='5' height='13'/%3E%3Crect x='546' y='-10' width='6' height='10'/%3E%3Cstyle type='text/css'%3E rect %7B opacity: 0; %7D rect:nth-child(1) %7B transform-origin: 45px 5px; transform: rotate(-145deg); animation: blast 700ms infinite ease-out; animation-delay: 88ms; animation-duration: 631ms; %7D rect:nth-child(2) %7B transform-origin: 87px 5px; transform: rotate(164deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 442ms; %7D rect:nth-child(3) %7B transform-origin: 128px 6px; transform: rotate(4deg); animation: blast 700ms infinite ease-out; animation-delay: 92ms; animation-duration: 662ms; %7D rect:nth-child(4) %7B transform-origin: 170px 6px; transform: rotate(-175deg); animation: blast 700ms infinite ease-out; animation-delay: 17ms; animation-duration: 593ms; %7D rect:nth-child(5) %7B transform-origin: 213px 5px; transform: rotate(-97deg); animation: blast 700ms infinite ease-out; animation-delay: 122ms; animation-duration: 476ms; %7D rect:nth-child(6) %7B transform-origin: 255px 6px; transform: rotate(57deg); animation: blast 700ms infinite ease-out; animation-delay: 271ms; animation-duration: 381ms; %7D rect:nth-child(7) %7B transform-origin: 297px 5px; transform: rotate(-46deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 619ms; %7D rect:nth-child(8) %7B transform-origin: 338px 6px; transform: rotate(-65deg); animation: blast 700ms infinite ease-out; animation-delay: 85ms; animation-duration: 668ms; %7D rect:nth-child(9) %7B transform-origin: 380px 6px; transform: rotate(13deg); animation: blast 700ms infinite ease-out; animation-delay: 128ms; animation-duration: 377ms; %7D rect:nth-child(10) %7B transform-origin: 423px 5px; transform: rotate(176deg); animation: blast 700ms infinite ease-out; animation-delay: 311ms; animation-duration: 508ms; %7D rect:nth-child(11) %7B transform-origin: 465px 5px; transform: rotate(108deg); animation: blast 700ms infinite ease-out; animation-delay: 108ms; animation-duration: 595ms; %7D rect:nth-child(12) %7B transform-origin: 506px 6px; transform: rotate(62deg); animation: blast 700ms infinite ease-out; animation-delay: 105ms; animation-duration: 375ms; %7D rect:nth-child(13) %7B transform-origin: 549px 5px; transform: rotate(16deg); animation: blast 700ms infinite ease-out; animation-delay: 149ms; animation-duration: 491ms; %7D rect:nth-child(odd) %7B fill: %2365BB5C; %7D rect:nth-child(even) %7B z-index: 1; fill: %2333AAFF; %7D rect:nth-child(4n) %7B animation-duration: 1400ms; fill: %23F23B14; %7D rect:nth-child(3n) %7B animation-duration: 1750ms; animation-delay: 700ms; %7D rect:nth-child(4n-7) %7B fill: %232A2F6A; %7D rect:nth-child(6n) %7B fill: %23FBBA23; %7D @keyframes blast %7B from %7B opacity: 0; %7D 20%25 %7B opacity: 1; %7D to %7B transform: translateY(90px); %7D %7D %3C/style%3E%3C/svg%3E%0A");
  }
</style>
