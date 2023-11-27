<script lang="ts">
  import { CalenderEventEmojeTyoe } from "../../../utils/enums";
  import type { calendarItemsType, userDataType } from "../../../utils/types";
  import ProfileImage from "../../profile/ProfileImage.svelte";
  import CalendarModal from "./CalendarModal.svelte";

  export let showModal = false;
  export let clickedItemOnModal: calendarItemsType;

  export let currentUserActive: userDataType;
  export let currentUserID: number = currentUserActive.id;

  const activateUser = (user: userDataType) => {
    currentUserActive = user;
    currentUserID = user.id;
  };
</script>

<CalendarModal bind:showModal>
  <header slot="header" class="text-center w-100">
    <h6 class="modal-title" id="exampleModalLongTitle">
      <strong
        >{clickedItemOnModal.date} Birthdays {CalenderEventEmojeTyoe.birthday}</strong
      >
    </h6>
  </header>
  <div slot="body" class="bg-confetti-animated">
    {#if clickedItemOnModal.users}
      <div class="container d-flex flex-column gap-5 px-5 my-5">
        <h3 class="mx-auto text-muted">
          {clickedItemOnModal.users.length > 1
            ? "Wish them a Happy Birthday !"
            : `Wish ${
                clickedItemOnModal.users[0].gender === "Male" ? "him" : "her"
              } a BirthDay ! `}
        </h3>
        <div class="row m-0 justify-content-center">
          {#each clickedItemOnModal.users as user}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div
              class={`col-2 p-0 justify-content-center d-flex photo-active ${
                user.id === currentUserID ? "active-user" : ""
              }`}
              on:click={() => {
                activateUser(user);
              }}
            >
              <ProfileImage size={70} {user} noLink={true} />
            </div>
          {/each}
        </div>
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-6 text-center">
                <strong> Name </strong>
              </div>
              <div class="col-6">
                <p class="text-muted">
                  {currentUserActive.full_name.trim().length
                    ? currentUserActive.full_name
                    : "--"}
                </p>
              </div>
              <div class="col-6 text-center">
                <strong> Team </strong>
              </div>
              <div class="col-6">
                <p class="text-muted">
                  {currentUserActive.team || "--"}
                </p>
              </div>
              <div class="col-6 text-center">
                <strong> Email </strong>
              </div>
              <div class="col-6">
                <p class="text-muted">
                  {currentUserActive.email}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
  <div slot="modal-footer">
    <button
      type="button"
      class="abtn btn-secondary"
      on:click={() => {
        const body = document.getElementById("body-pd");
        if (body) {
          body.style.overflow = "auto";
        }
        showModal = false;
      }}
    >
      Close
    </button>
  </div>
</CalendarModal>

<style>
  .bg-confetti-animated {
    background-repeat: repeat-x;
    background-position: top -10px center;
    background-image: url("data:image/svg+xml,%3Csvg width='600' height='90' viewBox='0 0 600 90' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='42' y='-10' width='6' height='10'/%3E%3Crect x='84' y='-10' width='6' height='10'/%3E%3Crect x='126' y='-13' width='5' height='13'/%3E%3Crect x='168' y='-13' width='5' height='13'/%3E%3Crect x='210' y='-10' width='6' height='10'/%3E%3Crect x='252' y='-13' width='5' height='13'/%3E%3Crect x='294' y='-10' width='6' height='10'/%3E%3Crect x='336' y='-13' width='5' height='13'/%3E%3Crect x='378' y='-13' width='5' height='13'/%3E%3Crect x='420' y='-10' width='6' height='10'/%3E%3Crect x='462' y='-10' width='6' height='10'/%3E%3Crect x='504' y='-13' width='5' height='13'/%3E%3Crect x='546' y='-10' width='6' height='10'/%3E%3Cstyle type='text/css'%3E rect %7B opacity: 0; %7D rect:nth-child(1) %7B transform-origin: 45px 5px; transform: rotate(-145deg); animation: blast 700ms infinite ease-out; animation-delay: 88ms; animation-duration: 631ms; %7D rect:nth-child(2) %7B transform-origin: 87px 5px; transform: rotate(164deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 442ms; %7D rect:nth-child(3) %7B transform-origin: 128px 6px; transform: rotate(4deg); animation: blast 700ms infinite ease-out; animation-delay: 92ms; animation-duration: 662ms; %7D rect:nth-child(4) %7B transform-origin: 170px 6px; transform: rotate(-175deg); animation: blast 700ms infinite ease-out; animation-delay: 17ms; animation-duration: 593ms; %7D rect:nth-child(5) %7B transform-origin: 213px 5px; transform: rotate(-97deg); animation: blast 700ms infinite ease-out; animation-delay: 122ms; animation-duration: 476ms; %7D rect:nth-child(6) %7B transform-origin: 255px 6px; transform: rotate(57deg); animation: blast 700ms infinite ease-out; animation-delay: 271ms; animation-duration: 381ms; %7D rect:nth-child(7) %7B transform-origin: 297px 5px; transform: rotate(-46deg); animation: blast 700ms infinite ease-out; animation-delay: 131ms; animation-duration: 619ms; %7D rect:nth-child(8) %7B transform-origin: 338px 6px; transform: rotate(-65deg); animation: blast 700ms infinite ease-out; animation-delay: 85ms; animation-duration: 668ms; %7D rect:nth-child(9) %7B transform-origin: 380px 6px; transform: rotate(13deg); animation: blast 700ms infinite ease-out; animation-delay: 128ms; animation-duration: 377ms; %7D rect:nth-child(10) %7B transform-origin: 423px 5px; transform: rotate(176deg); animation: blast 700ms infinite ease-out; animation-delay: 311ms; animation-duration: 508ms; %7D rect:nth-child(11) %7B transform-origin: 465px 5px; transform: rotate(108deg); animation: blast 700ms infinite ease-out; animation-delay: 108ms; animation-duration: 595ms; %7D rect:nth-child(12) %7B transform-origin: 506px 6px; transform: rotate(62deg); animation: blast 700ms infinite ease-out; animation-delay: 105ms; animation-duration: 375ms; %7D rect:nth-child(13) %7B transform-origin: 549px 5px; transform: rotate(16deg); animation: blast 700ms infinite ease-out; animation-delay: 149ms; animation-duration: 491ms; %7D rect:nth-child(odd) %7B fill: %2365BB5C; %7D rect:nth-child(even) %7B z-index: 1; fill: %2333AAFF; %7D rect:nth-child(4n) %7B animation-duration: 1400ms; fill: %23F23B14; %7D rect:nth-child(3n) %7B animation-duration: 1750ms; animation-delay: 700ms; %7D rect:nth-child(4n-7) %7B fill: %232A2F6A; %7D rect:nth-child(6n) %7B fill: %23FBBA23; %7D @keyframes blast %7B from %7B opacity: 0; %7D 20%25 %7B opacity: 1; %7D to %7B transform: translateY(90px); %7D %7D %3C/style%3E%3C/svg%3E%0A");
  }
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
