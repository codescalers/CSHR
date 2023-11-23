<script lang="ts">
  import { onMount } from "svelte";
  import { Route } from "svelte-navigator";
  import { Link } from "svelte-navigator";
  import { navigate } from "svelte-navigator";

  import HRLetterDataService from "../../apis/hr_letter/hr_letter";
  import Requests from "../../apis/requests/Requests";
  import Error from "../../pages/Error.svelte";
  import { RequestStatus } from "../../utils/enums";
  import { UserStore } from "../../utils/stores";
  import type { HRLetterType } from "../../utils/types";
  import ProfileImage from "../profile/ProfileImage.svelte";
  import ActionButton from "../requests/requestsButtons.svelte";
  import Loading from "../ui/Loading.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  var path = window.location.pathname;
  const hrLetterID = path.split("/")[2];
  let hrLetter: HRLetterType;

  if (!+hrLetterID) {
    isError = true;
  }

  onMount(async () => {
    isLoading = true;
    try {
      const hrLetterAPI = await HRLetterDataService.getByID(+hrLetterID);
      hrLetter = hrLetterAPI.data.results;
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });

  const handleActions = (event: { detail: { text: any } }) => {
    const sRequest = event.detail.text;
    hrLetter.status = hrLetter.status;
    hrLetter.status = sRequest.status;
    hrLetter.approval_user = $UserStore;
  };
</script>

{#if isError}
  <Route>
    <Error error={404} />
  </Route>
{/if}

<div class="container pt-5">
  {#if isLoading}
    <div class="height-100 d-flex justify-content-center align-items-center">
      <Loading className={"loader"} />
    </div>
  {:else if hrLetter}
    {#if $UserStore.user_type == "Supervisor"}
      <div class="mb-4" style="width: 20%;">
        <ActionButton request={hrLetter} on:message={handleActions} />
      </div>
    {/if}
    {#if $UserStore.user_type == "User" && hrLetter.status == RequestStatus.pinding}
      <div class="d-flex display-buttons">
        <Link to="/hrLetters/{hrLetter.id}/update" class="abtn btn-primary mb-2 custom-a" style="color: #fff">
          <span class="nav_name">Update hrLetter</span>
        </Link>
        <button
          on:click={async () => {
            await Requests.delete(hrLetter);
            navigate("/", { replace: true });
          }}
          class="abtn btn-danger mb-2 custom-a"
          style="color: #fff"
        >
          <span class="nav_name">Delete hrLetter</span>
        </button>
      </div>
      <small class="text-muted text-center">
        Hint: Once you click on the delete button the request will delete without any confirmation
      </small>
    {/if}
    <div class="card p-4 d-flex justify-content-center">
      <div class="row">
        <div class="col-6">
          <p>Applying User</p>
        </div>
        <div class="col-6 d-flex">
          {#if hrLetter.applying_user != undefined}
            <ProfileImage user={hrLetter.applying_user} />
            <p class="p-2">{hrLetter.applying_user.full_name}</p>
          {/if}
        </div>
        <div class="col-6">
          <p>Approval User</p>
        </div>
        <div class="col-6 d-flex">
          {#if hrLetter.approval_user != null}
            <ProfileImage user={hrLetter.approval_user} />
            <p class="p-2">{hrLetter.approval_user.full_name}</p>
          {:else}
            <p class="p-2 text-muted">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-hourglass-bottom"
                viewBox="0 0 16 16"
              >
                <path
                  d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5zm2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702s.18.149.5.149.5-.15.5-.15v-.7c0-.701.478-1.236 1.011-1.492A3.5 3.5 0 0 0 11.5 3V2h-7z"
                />
              </svg>
              Under aprroving...
            </p>
          {/if}
        </div>
        <div class="col-6 mt-2">
          <p>Start Date</p>
        </div>
        <div class="col-6 mt-2">
          <p>{hrLetter.from_date || "--"}</p>
        </div>
        <div class="col-6">
          <p>End Date</p>
        </div>
        <div class="col-6">
          <p>{hrLetter.end_date || "--"}</p>
        </div>
        <div class="col-6">
          <p>Addresses</p>
        </div>
        <div class="col-6">
          <p>{hrLetter.addresses}</p>
        </div>
        <div class="col-6">
          <p>With salary mentioned</p>
        </div>
        <div class="col-6">
          {#if hrLetter.with_salary_mentioned == false}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-x-lg text-danger"
              viewBox="0 0 16 16"
            >
              <path
                d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"
              />
            </svg>
            No
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-check2-all text-success"
              viewBox="0 0 16 16"
            >
              <path
                d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"
              />
              <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z" />
            </svg>
            Yes
          {/if}
        </div>
        <div class="col-6">
          <p>With date mentioned</p>
        </div>
        <div class="col-6">
          {#if hrLetter.with_date == false}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-x-lg text-danger"
              viewBox="0 0 16 16"
            >
              <path
                d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"
              />
            </svg>
            No
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-check2-all text-success"
              viewBox="0 0 16 16"
            >
              <path
                d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"
              />
              <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z" />
            </svg>
            Yes
          {/if}
        </div>
        <div class="col-6">
          <p>Status</p>
        </div>
        <div class="col-6">
          <p class="text-muted">
            {#if hrLetter.status == RequestStatus.pinding}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-hourglass-bottom text-muted"
                viewBox="0 0 16 16"
              >
                <path
                  d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5zm2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702s.18.149.5.149.5-.15.5-.15v-.7c0-.701.478-1.236 1.011-1.492A3.5 3.5 0 0 0 11.5 3V2h-7z"
                />
              </svg>
            {:else if hrLetter.status == RequestStatus.approved}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-check2-all text-success"
                viewBox="0 0 16 16"
              >
                <path
                  d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"
                />
                <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z" />
              </svg>
            {:else}
              <!-- Rejacted -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-x-lg text-danger"
                viewBox="0 0 16 16"
              >
                <path
                  d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"
                />
              </svg>
            {/if}
            {hrLetter.status}
          </p>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .display-buttons {
    flex-direction: column;
    width: 20%;
  }
</style>
