<script lang="ts">
  import { onMount } from "svelte";
  import { Route } from "svelte-navigator";

  import Vacation from "../../apis/vacations/Vacation";
  import Error from "../../pages/Error.svelte";
  import { RequestStatus } from "../../utils/enums";
  import CalendarDatePicker from "../calendar/CalendarDatePicker.svelte";
  import CalendarLeaveForm from "../calendar/forms/LeaveForm.svelte";
  import Input from "../ui/Input.svelte";
  import ProfileImage from "../profile/ProfileImage.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  var path = window.location.pathname;
  const vacationID = path.split("/")[2];
  let vacation: any, startDate: string, endDate: string, reason: string;

  onMount(async () => {
    isLoading = true;
    try {
      vacation = await Vacation.vacatioDetails(+vacationID);
      startDate = vacation.from_date;
      endDate = vacation.end_date;
      reason = vacation.reason;
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });

  let formToggle = 0;
  let vacationCalculator: number;

  const handleVacationCalculator = (event: { detail: { days: number } }) => {
    vacationCalculator = event.detail.days;
  };

  const updateDates = (event: {
    detail: { startDate: string; endDate: string };
  }) => {
    startDate = event.detail.startDate;
    endDate = event.detail.endDate;
  };
</script>

{#if vacation && vacation.status != RequestStatus.pinding}
  <Route>
    <Error error={404} />
  </Route>
{/if}

<div class="container d-flex justify-content-center align-items-center">
  <div class="mt-5">
    {#if startDate && endDate}
    <div class="bg-white p-3 pt-0 mt-0 card">
      <div class="card-body">
        <div class="text-center">
          <small>
            Kindly be aware that you can only modify your request while its status remains 'Pending.' Once the status changes, further updates will not be permitted.
          </small>
        </div>
        <div class="card p-2 mt-3" style="margin: 0 auto; width: 85%;">
          <div class="row">
            <div class="col-6 d-flex align-items-center">
              <strong>Applying user</strong>
            </div>
            <div class="col-6 d-flex align-items-center">
              <ProfileImage user={vacation.applying_user}/>
            </div>
          </div>
        </div>

        <CalendarDatePicker
          onlyStart={formToggle === 1}
          bind:startDate
          bind:endDate
          on:calculate={handleVacationCalculator}
          on:updateDates={updateDates}
        >
          <div slot="form">
            {#if formToggle === 0}
              <CalendarLeaveForm
                bind:startDate
                bind:endDate
                calculatorValue={vacationCalculator}
                isUpdate={true}
                {vacationID}
                selectedReason={vacation.reason}
                submitWidth={"30"}
              />
            {/if}
          </div>
        </CalendarDatePicker>
      </div>
    </div>
    {/if}
  </div>
</div>
