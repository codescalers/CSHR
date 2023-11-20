<script lang="ts">
  import Input from "../ui/Input.svelte";
  import Submit from "../ui/Button.svelte";
  import CalendarLeaveForm from "../calendar/forms/LeaveForm.svelte";
  import CalendarDatePicker from "../calendar/CalendarDatePicker.svelte";
  import CompensationsDataService from "../../apis/compensation/compensations";
  import type { CompensationType } from "../../utils/types";
  import { createEventDispatcher } from "svelte";

  export let isLoading: boolean = false;
  export let isError: boolean = false;

  const dispatch = createEventDispatcher();

  let isErrorReason: boolean | null = null;
  let isErrorDates: boolean;
  let thisDate: Date = new Date();
  let startDate = `${thisDate.getFullYear()}-${
    thisDate.getMonth() + 1
  }-${thisDate.getDate()}`;
  let endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${
    thisDate.getDate() + 2
  }`;
  let datePickerDisabled = false;
  let successMessage: string;
  let errorMessage: string;

  let CompensationData: CompensationType = {
    from_date: "",
    end_date: "",
    reason: "",
  };

  $: submitDisabled = isErrorReason == true || isErrorReason == null;
</script>

<div class="row mt-4 d-flex justify-content-center">
  <div class="col-12">
    <div class="container" style="width: 40%;">
      {#if startDate && endDate}
        <CalendarDatePicker
          onlyStart={false}
          bind:startDate
          bind:endDate
          bind:datePickerDisabled
          calculate={false}
        >
          <div slot="form">
            <div class="form-outline">
              <Input
                type="text"
                label={"Reason"}
                bind:value={CompensationData.reason}
                handleInput={() => {
                  return false;
                }}
                size={150}
                errorMessage="Invalid Reason"
                hint={"please enter a valid reason"}
                placeholder={"Enter Reason"}
                bind:isError={isErrorReason}
              />
            </div>
            <CalendarLeaveForm
              bind:startDate
              bind:endDate
              bind:datePickerDisabled
              bind:isError={isErrorDates}
              withReason={false}
              withSubmit={false}
              showCalclator={false}
            />
          </div>
        </CalendarDatePicker>
      {/if}
    </div>
  </div>
  <div class="col-12">
    <div class="form-outline mt-4 d-flex justify-content-center">
      <Submit
        width={"30"}
        bind:successMessage
        bind:errorMessage
        label="Submit"
        onClick={async () => {
          isLoading = true;
          try {
            CompensationData.from_date = startDate;
            CompensationData.end_date = endDate;
            const axios = await CompensationsDataService.post(CompensationData);
            dispatch("message", {
              postedCompensation: axios.data.results,
            });
            successMessage = axios.data.message;
            isError = false;
          } catch (error) {
            isError = true;
            errorMessage = error.message;
          } finally {
            CompensationData.reason = "";
            isLoading = false;
          }
          return isError;
        }}
        className=""
        bind:disabled={submitDisabled}
      />
    </div>
  </div>
</div>
