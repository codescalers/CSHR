<script lang="ts">
  import { CalenderEventEmojeTyoe } from "../../../utils/enums";
  import type {
    calendarItemsType,
    meetingItemType,
    dateType
  } from "../../../utils/types";
  import ProfileImage from "../../profile/ProfileImage.svelte";
  import CalendarModal from "./CalendarModal.svelte";

  export let showModal: boolean = false;
  export let clickedItemOnModal: calendarItemsType;
  export let currentMeetingActive: meetingItemType;
  export let currentMeetingID: number = currentMeetingActive.id;
  
  let meetingDate: dateType = currentMeetingActive.date;
  
  const activateUser = (meeting: meetingItemType) => {
    currentMeetingID = meeting.id;
    currentMeetingActive = meeting;
    meetingDate = currentMeetingActive.date
  };

  function formatAMPM(hours: number, minutes: number | string) {
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' +minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  };

</script>

<CalendarModal bind:showModal>
  <header slot="header" class="text-center w-100">
    <h6 class="modal-title" id="exampleModalLongTitle">
      <strong>
        {clickedItemOnModal.meeting[0].date.year} - 
        {clickedItemOnModal.meeting[0].date.month} - 
        {clickedItemOnModal.meeting[0].date.day} 
        Meetings 
        {CalenderEventEmojeTyoe.meeting}
      </strong>
    </h6>
  </header>
  <div slot="body">
    <div class="container d-flex flex-column gap-5 px-5 my-5">
      <h4 class="mx-auto text-muted text-center">Meetings available, Created by.</h4>
      <div class="row m-0 justify-content-center">
        {#each clickedItemOnModal.meeting as meeting}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class={`col-2 p-0 justify-content-center d-flex photo-active ${meeting.id === currentMeetingID ? 'active-user' : ''}`} on:click={
                () => {
                    activateUser(meeting)
                }
            }>
                <ProfileImage size={70} user={meeting.host_user} noLink={true}/>
            </div>
        {/each}
      </div>
      {#if currentMeetingActive}
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-6 text-center">
                  <strong>
                      Name
                  </strong>
              </div>
              <div class="col-6">
                  <p class="text-muted">
                      {currentMeetingActive.host_user.full_name.trim().length ? currentMeetingActive.host_user.full_name : '--'}
                  </p>
              </div>
              <div class="col-6 text-center">
                  <strong>
                      Team
                  </strong>
              </div>
              <div class="col-6">
                  <p class="text-muted">
                      {currentMeetingActive.host_user.team || "--"}
                  </p>
              </div>
              <div class="col-6 text-center">
                  <strong>
                      Link
                  </strong>
              </div>
              <div class="col-6">
                  <a class="text-primary"
                    href="{
                      currentMeetingActive.meeting_link.startsWith('http') ? 
                      currentMeetingActive.meeting_link : 
                      'https://' + currentMeetingActive.meeting_link
                    }" 
                    target="_blank" rel="noreferrer"
                  >
                  <i class="fa fa-link"></i>
                  Meeting Link
                  </a>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <table class="table table-bordered text-center">
              <thead>
                  <tr class="bg-light-gray">
                    <th class="text-uppercase">Date</th>
                    <th class="text-uppercase">Time</th>
                  </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="align-middle">{meetingDate.year} - {meetingDate.month} - {meetingDate.day}</td>
                  <td class="align-middle">{formatAMPM(meetingDate.hour, meetingDate.minute)}</td>
                </tr>
              </tbody>
            </table>
            {#if currentMeetingActive.invited_users.length}
              <h4 class="text-center">Invited users</h4>
              <div class="d-flex justify-content-center">
                {#each currentMeetingActive.invited_users as user}
                  <ProfileImage size={50} {user}/>
                {/each}
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>
  <div slot="modal-footer">
    <button type="button" class="abtn btn-secondary" on:click={() => {
      document.getElementById("body-pd").style.overflow = "auto";
      showModal = false;
    }}>
      Close
    </button>
  </div>
</CalendarModal>

<style>
  .photo-active {
    z-index: 9;
    cursor: pointer;
  }
  .active-user,
  .photo-active:hover {
    z-index: 10;    
  }
  .photo-active:not(:first-child) {
    margin-left: -75px;
  }
</style>