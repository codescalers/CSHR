<script lang="ts">
  import { CalenderEventEmojeTyoe } from "../../../utils/enums";
  import type { calendarItemsType, eventItemType } from "../../../utils/types";
  // import ProfileImage from "../../profile/ProfileImage.svelte";
  import CalendarModal from "./CalendarModal.svelte";

  export let showModal = false;
  export let clickedItemOnModal: calendarItemsType;
  export let currentEventActive: eventItemType;

  // let fromDate: Date = new Date(currentEventActive.from_date);
  // let endDate: Date = new Date(currentEventActive.end_date);

  function formatAMPM(hours: number, minutes: number) {
    var ampm = hours >= 12 ? "pm" : "am";
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    let _minutes = minutes < 10 ? "0" + minutes : minutes;
    var strTime = hours + ":" + _minutes + " " + ampm;
    return strTime;
  }
</script>

<CalendarModal bind:showModal>
  <header slot="header" class="text-center w-100">
    <h6 class="modal-title" id="exampleModalLongTitle">
      <strong>
        {clickedItemOnModal.event[0].from_date.year} -
        {clickedItemOnModal.event[0].from_date.month} -
        {clickedItemOnModal.event[0].from_date.day}
        Events
        {CalenderEventEmojeTyoe.event}</strong
      >
    </h6>
  </header>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      {#if currentEventActive}
        <h4 class="mx-auto text-muted text-center">
          {currentEventActive.name}
        </h4>
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <strong> Description </strong>
              </div>
              <div class="col-12">
                <p class="text-muted">
                  {currentEventActive.description}
                </p>
              </div>
              <!-- <div class="col-12">
                <strong>
                  Location
                </strong>
              </div>
              <div class="col-12">
                <p class="text-muted">
                  {currentEventActive.location}
                </p>
              </div> -->
            </div>
          </div>
          <div class="card-footer">
            <table class="table table-bordered text-center">
              <thead>
                <tr class="bg-light-gray">
                  <th class="text-uppercase">From Date</th>
                  <th class="text-uppercase">To Date</th>
                  <th class="text-uppercase">From Time</th>
                  <th class="text-uppercase">To Time</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="align-middle"
                    >{currentEventActive.from_date.year} - {currentEventActive.from_date.month} - {currentEventActive
                      .from_date.day}</td
                  >
                  <td class="align-middle"
                    >{currentEventActive.end_date.year} - {currentEventActive.end_date.month} - {currentEventActive
                      .end_date.day}</td
                  >
                  <td class="align-middle"
                    >{formatAMPM(currentEventActive.from_date.hour, currentEventActive.from_date.minute)}</td
                  >
                  <td class="align-middle"
                    >{formatAMPM(currentEventActive.end_date.hour, currentEventActive.end_date.minute)}</td
                  >
                </tr>
              </tbody>
            </table>
            <!-- {#if currentEventActive.custom_people.length}
              <h4 class="text-center">Invited users</h4>
              <div class="d-flex justify-content-center">
                {#each currentEventActive.custom_people as user}
                  <ProfileImage size={50} {user}/>
                {/each}
              </div>
            {/if} -->
          </div>
        </div>
      {/if}
    </div>
  </div>

  <div slot="modal-footer">
    <button
      type="button"
      class="abtn btn-secondary"
      on:click={() => {
        document.getElementById("body-pd").style.overflow = "auto";
        showModal = false;
      }}
    >
      Close
    </button>
  </div>
</CalendarModal>
