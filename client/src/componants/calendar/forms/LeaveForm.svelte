<script lang="ts">
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import Vacations from "../../../apis/vacations/Vacation";
  import { capitalize, formatDate } from "../../../utils/helpers";
  import { UserStore } from "../../../utils/stores";
  import type {
    calendarItemsType,
    VacationBalance
  } from "../../../utils/types";
  import Alert from "../../ui/Alert.svelte";
  import Submit from "../../ui/Button.svelte";

  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let calculatorValue = 0;
  export let isUpdate = false;
  export let selectedReason: any = 0;
  export let vacationID = "";
  export let withReason = true;
  export let withSubmit = true;
  export let showCalclator = true;

  let errorMessage = "";
  let successMessage = "";

  let alertTitle: string,
    alertClass: string,
    alertMessage: string,
    showAlert: boolean;
  let vBalance: VacationBalance;
  let responseVacation: calendarItemsType;
  const dispatch = createEventDispatcher();

  onMount(async () => {
    const response = await Vacations.balance([$UserStore.id]);
    vBalance = response[0];
  });

  const submit = async () => {
    isLoading = true;
    isError = showAlert = false;
    alertMessage = errorMessage = "";
    alertClass = ""
    try {
      if (isUpdate && vacationID != "") {
        const axios = await Vacations.update(vacationID, {
          end_date: endDate,
          from_date: startDate,
          reason: selectedReason,
          applyingUserId: $UserStore.id
        });
        successMessage = axios.data.message;
      } else {
        const axios = await Vacations.post({
          end_date: formatDate(new Date(endDate)),
          from_date: formatDate(new Date(startDate)),
          reason: selectedReason,
          applyingUserId: $UserStore.id
        });
        successMessage = axios.data.message;
        responseVacation = axios.data.results;
        dispatch("message", {
          postedVacation: responseVacation
        });

        // vBalance[selectedReason].reserved =
        //   vBalance[selectedReason].reserved + calculatorValue;
      }
    } catch (error: any) {
      isError = showAlert = true;
      alertMessage = errorMessage = error.message;
      alertClass = "danger"
      // alertTitle = "An error while trying to post your request."
    } finally {
      isLoading = false;
    }
    return isError;
  };

  $: submitDisabled = selectedReason == 0 || calculatorValue === 0;
</script>

<form>
  {#if withReason}
    <div class="form-group row">
      <div class="col-6 d-flex align-items-center">
        <label for="endDayInput"> Reason </label>
      </div>

      <div class="col-6 d-flex align-items-center">
        <select
          bind:value={selectedReason}
          id="Reason"
          class="form-select form-control mt-0 mv-4"
          aria-label="Default select example"
        >
          {#if vBalance}
            {#each Object.entries(vBalance) as [name, _value]}
              {#if name != "user"}
                <option value={name}>
                  {capitalize(name.replace("_", " "))}
                  {_value.reserved} / {_value.all >= 100 ? "∞" : _value.all}
                </option>
              {/if}
            {/each}
          {/if}
        </select>
      </div>
    </div>
  {/if}
  {#if showCalclator}
    <div class="alert alert-light p-0 text-center">
      <br />
      {#if calculatorValue === 0}
        <small class="text-red">
          " It seems like the chosen day might be a holiday or a weekend break.
          Please verify this on your calendar. "
        </small>
      {:else}
        <small class="text-dark">
          The final count after excluding weekends and holidays is {calculatorValue}
          {calculatorValue > 1 ? "days" : "day"}.
        </small>
      {/if}
    </div>
  {/if}
  {#if withSubmit}
    <div>
      <Submit
        bind:successMessage
        bind:errorMessage
        label="Request"
        onClick={submit}
        className=""
        bind:disabled={submitDisabled}
      />
    </div>
  {/if}
  {#if showAlert}
    <div class="mt-2">
      <Alert title={alertTitle} message={alertMessage} className={alertClass} />
    </div>
  {/if}
</form>
<svelte:head>
  <style>
    .form-select:focus {
      box-shadow: none !important;
    }
  </style>
</svelte:head>
