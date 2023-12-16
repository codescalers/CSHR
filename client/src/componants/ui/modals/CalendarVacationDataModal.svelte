<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Link, navigate } from "svelte-navigator";

  import Requests from "../../../apis/requests/Requests";
  import {
    CalenderEventEmojeTyoe,
    RequestStatus,
    UserTypeEnum
  } from "../../../utils/enums";
  import { capitalize } from "../../../utils/helpers";
  import { UserStore } from "../../../utils/stores";
  import type {
    calendarItemsType,
    vacationItemType
  } from "../../../utils/types";
  import ProfileImage from "../../profile/ProfileImage.svelte";
  import Alert from "../Alert.svelte";
  import Loading from "../Loading.svelte";
  import CalendarModal from "./CalendarModal.svelte";
  import vacation from "../../../apis/vacations/Vacation";
  export let showModal = false;

  export let clickedItemOnModal: calendarItemsType;
  export let currentVacationActive: vacationItemType;
  export let currentVacationID: number = +currentVacationActive.id;

  let approveLoading = false;
  let rejectLoading = false;
  let isDisable = false;
  let showAlert = false;
  let responseMessage: string;
  let responseClass: string;
  let responseTitle: string;

  const dispatch = createEventDispatcher();

  async function approveVacation() {
    approveLoading = true;
    isDisable = true;
    try {
      const response = await Requests.approve(
        currentVacationActive,
        +currentVacationActive.id
      );
      currentVacationActive.status = RequestStatus.approved;
      currentVacationActive.approval_user = $UserStore;
      responseMessage = response.data.message;
      responseTitle = "Success!";
      responseClass = "success";
      showAlert = true;
      setTimeout(() => {
        showAlert = false;
      }, 5000);
    } catch (error: any) {
      responseMessage = error.message;
      responseTitle = "Error!";
      responseClass = "danger";
      showAlert = true;
    } finally {
      isDisable = false;
      approveLoading = false;
    }
  }

  async function rejectVacation() {
    rejectLoading = true;
    isDisable = true;
    try {
      const response = await Requests.reject(
        currentVacationActive,
        +currentVacationActive.id
      );
      responseMessage = response.data.message;
      currentVacationActive.status = RequestStatus.rejected;
      currentVacationActive.approval_user = $UserStore;
      responseTitle = "Success!";
      responseClass = "success";
      showAlert = true;
      dispatch("reject", true);
      setTimeout(() => {
        showAlert = false;
      }, 3000);
    } catch (error: any) {
      responseMessage = error.message;
      responseTitle = "Error!";
      responseClass = "danger";
      showAlert = true;
    } finally {
      isDisable = false;
      rejectLoading = false;
    }
  }

  const activateVacation = (vacation: vacationItemType) => {
    currentVacationActive = vacation;
    currentVacationID = +vacation.id;
  };
</script>

<CalendarModal bind:showModal>
  <header slot="header" class="text-center w-100">
    <h6 class="modal-title" id="exampleModalLongTitle">
      {#if clickedItemOnModal.vacation}
        <strong>
          <span class="text-primary">From</span>
          {clickedItemOnModal.vacation[0].from_date}
          <span class="text-primary">to</span>
          {clickedItemOnModal.vacation[0].end_date}
          <span class="text-primary">|</span>
          Vacations {CalenderEventEmojeTyoe.vacation}
        </strong>
      {/if}
    </h6>
  </header>
  <div slot="body">
    <div class="pt-3 card-body px-4 card-hover">
      <h5 class="card-title">
        {#if clickedItemOnModal.vacation}
          <div class="row m-0 justify-content-center">
            {#each clickedItemOnModal.vacation as vacation}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <div
                class={`col-2 p-0 justify-content-center d-flex photo-active ${
                  +vacation.id === currentVacationID ? "active-user" : ""
                }`}
                on:click={() => {
                  activateVacation(vacation);
                }}
              >
                <ProfileImage
                  size={70}
                  user={vacation.applying_user}
                  noLink={true}
                />
              </div>
            {/each}
          </div>
        {/if}
      </h5>

      <div class="text-center mt-4 mb-2 text-dark">
        {currentVacationActive.applying_user.full_name}
      </div>
      <p class="w-100 text-center text-muted">
        <span>{currentVacationActive.applying_user.job_title}</span>
        <small class="blockquote-footer">
          <cite title="Team">{currentVacationActive.applying_user.team}</cite>
        </small><br />
        <small>
          <cite>{currentVacationActive.applying_user.email}</cite>
        </small>
      </p>

      <div class="row dates mb-3">
        <div class="col-6 d-flex">
          <div class="col-6">
            <strong>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                fill="currentColor"
                class="bi bi-calendar-event mr-2"
                viewBox="0 0 16 16"
              >
                <path
                  d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"
                />
                <path
                  d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"
                />
              </svg>
              From
            </strong>
          </div>
          <div class="col-6 d-flex justify-content-end">
            {`${currentVacationActive.from_date}`}
          </div>
        </div>

        <div class="col-6 d-flex">
          <div class="col-6">
            <strong>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                fill="currentColor"
                class="bi bi-calendar-event mr-2"
                viewBox="0 0 16 16"
              >
                <path
                  d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"
                />
                <path
                  d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"
                />
              </svg>
              To
            </strong>
          </div>
          <div class="col-6 d-flex justify-content-end">
            {`${currentVacationActive.end_date}`}
          </div>
        </div>
        <div class="col-6 d-flex">
          <div class="col-6">
            <strong>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                fill="currentColor"
                class="bi bi-cursor-fill"
                viewBox="0 0 16 16"
              >
                <path
                  d="M14.082 2.182a.5.5 0 0 1 .103.557L8.528 15.467a.5.5 0 0 1-.917-.007L5.57 10.694.803 8.652a.5.5 0 0 1-.006-.916l12.728-5.657a.5.5 0 0 1 .556.103z"
                />
              </svg>
              Reason
            </strong>
          </div>
          <div class="col-6 d-flex justify-content-end">
            {capitalize(currentVacationActive.reason).replaceAll("_", " ")}
          </div>
        </div>

        <div class="col-6 d-flex">
          <div class="col-6">
            <strong>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-menu-button"
                viewBox="0 0 16 16"
              >
                <path
                  d="M0 1.5A1.5 1.5 0 0 1 1.5 0h8A1.5 1.5 0 0 1 11 1.5v2A1.5 1.5 0 0 1 9.5 5h-8A1.5 1.5 0 0 1 0 3.5zM1.5 1a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5z"
                />
                <path
                  d="m7.823 2.823-.396-.396A.25.25 0 0 1 7.604 2h.792a.25.25 0 0 1 .177.427l-.396.396a.25.25 0 0 1-.354 0zM0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"
                />
              </svg>
              Status
            </strong>
          </div>
          <div class="col-6 d-flex justify-content-end">
            {capitalize(currentVacationActive.status)}
          </div>
        </div>
        {#if currentVacationActive.approval_user && currentVacationActive.approval_user.full_name}
          <div class="col-12 d-flex">
            <div class="col-6">
              <strong>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  fill="currentColor"
                  class="bi bi-person-check"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"
                  />
                </svg>
                Approved by
              </strong>
            </div>
            <div class="col-6 d-flex justify-content-end">
              <Link to="/profile/{currentVacationActive.approval_user.id}">
                @{currentVacationActive.approval_user.full_name}
              </Link>
            </div>
          </div>
        {/if}
        <br />
        <button
        class="abtn btn-success view-btn"
        on:click={() => navigate(`/vacations/${currentVacationActive.id}`)}
      >
        View
      </button>
      </div>
      {#if showAlert}
        <Alert
          title={responseTitle}
          message={responseMessage}
          className={responseClass}
        />
      {/if}

      {#if $UserStore.user_type == UserTypeEnum.admin && currentVacationActive.status == RequestStatus.pinding}
        <div class="buttons mt-4 mb-4">
          <button
            class="abtn btn-success"
            on:click={() => {
              approveVacation();
            }}
            disabled={isDisable}
          >
            {#if approveLoading}
              <Loading />
            {:else}
              Approve
            {/if}
          </button>

          <button
            class="abtn btn-danger"
            on:click={() => {
              rejectVacation();
            }}
            disabled={isDisable}
          >
            {#if rejectLoading}
              <Loading />
            {:else}
              Reject
            {/if}
          </button>
        </div>
      {/if}
    </div>
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

<svelte:head>
  <style>
    .dates {
      padding: 20px;
      background: rgb(241 247 247 / 64%);
      border-radius: 7px;
    }
    .buttons {
      float: right;
    }
    svg {
      margin-right: 5px;
    }
    .modal-backdrop.show {
      opacity: var(--bs-backdrop-opacity);
      display: block !important;
    }
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
    .view-btn{
      width: 15%;
    margin-top: 20px;
    }
  </style>
</svelte:head>
