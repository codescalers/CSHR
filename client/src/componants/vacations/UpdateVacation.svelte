<script lang="ts">
  import CalendarLeaveForm from "../calendar/forms/LeaveForm.svelte";
  import CalendarDatePicker from "../calendar/CalendarDatePicker.svelte";
  import Vacation from "../../apis/vacations/Vacation";
  import { onMount } from "svelte";
  import { RequestStatus } from "../../utils/enums";
  import { Route } from "svelte-navigator";
  import Error from "../../pages/Error.svelte";

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

  let formToggle: number = 0;
  let datePickerDisabled = false;

  let VacationCalculator: number;

  const handleVacationCalculator = (event: { detail: { text: number } }) => {
    VacationCalculator = event.detail.text;
  };
</script>

{#if vacation && vacation.status != RequestStatus.pinding}
  <Route>
    <Error error={404} />
  </Route>
{/if}

<div class="container" style="width: 30%;">
  {#if startDate && endDate}
    <CalendarDatePicker
      onlyStart={formToggle === 1}
      bind:startDate
      bind:endDate
      bind:datePickerDisabled
      on:message={handleVacationCalculator}
    >
      <div slot="form">
        {#if formToggle === 0}
          <CalendarLeaveForm
            bind:startDate
            bind:endDate
            bind:datePickerDisabled
            calculatorValue={VacationCalculator}
            isUpdate={true}
            {vacationID}
            selectedReason={vacation.reason}
          />
        {/if}
      </div>
    </CalendarDatePicker>
  {/if}
</div>
