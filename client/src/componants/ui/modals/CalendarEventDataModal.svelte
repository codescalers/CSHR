<script lang="ts">
  import type {
    calendarItemsType,
    eventItemType,
  } from "../../../utils/types";
  import ProfileImage from "../../profile/ProfileImage.svelte";
  import CalendarModal from "./CalendarModal.svelte";

  export let showModal: boolean = false;
  export let clickedItemOnModal: calendarItemsType;
  export let currentEventActive: eventItemType;
  
  let fromDate: Date = new Date(currentEventActive.from_date);
  let endDate: Date = new Date(currentEventActive.end_date);

  function formatAMPM(date: Date) {
    var hours = date.getHours();
    var minutes: number | string = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' +minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  };

</script>


<CalendarModal bind:showModal>
  <header slot="header">
    <h6 class="modal-title" id="exampleModalLongTitle">
      {clickedItemOnModal.title.toUpperCase()}
    </h6>
  </header>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      {#if currentEventActive}
        <h4 class="mx-auto text-muted text-center">{currentEventActive.name}</h4>
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <strong>
                  Description
                </strong>
              </div>
              <div class="col-12">
                <p class="text-muted">
                  {currentEventActive.description}
                </p>
              </div>
              <div class="col-12">
                <strong>
                  Location
                </strong>
              </div>
              <div class="col-12">
                <p class="text-muted">
                  {currentEventActive.location}
                </p>
              </div>
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
                  <td class="align-middle">{fromDate.getFullYear()} - {fromDate.getMonth()} - {fromDate.getDate()}</td>
                  <td class="align-middle">{endDate.getFullYear()} - {endDate.getMonth()} - {endDate.getDate()}</td>
                  <td class="align-middle">{formatAMPM(fromDate)}</td>
                  <td class="align-middle">{formatAMPM(endDate)}</td>
                </tr>
              </tbody>
            </table>
            <h4 class="text-center">Invited users</h4>
            <div class="d-flex justify-content-center">
              {#each currentEventActive.custom_people as user}
                <ProfileImage size={50} {user}/>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</CalendarModal>
