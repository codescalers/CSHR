<script lang="ts">
  import HRLetterDataService from "../../apis/hr_letter/hr_letter";
  import type { HRLetterType } from "../../utils/types";
  import CalendarDatePicker from "../calendar/CalendarDatePicker.svelte";
  import CalendarLeaveForm from "../calendar/forms/LeaveForm.svelte";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";

  export let isLoading = false;
  export let isError = false;

  let isErrorAddress: boolean | null = null;
  let thisDate: Date = new Date();
  let startDate = `${thisDate.getFullYear()}-${
    thisDate.getMonth() + 1
  }-${thisDate.getDate()}`;
  let endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${
    thisDate.getDate() + 2
  }`;
  let formToggle = 0;
  let datePickerDisabled = false;
  let successMessage: string;
  let errorMessage: string;

  let VacationCalculator: number;

  let hrLetterData: HRLetterType = {
    from_date: "",
    end_date: "",
    addresses: "",
    with_date: false,
    with_salary_mentioned: false
  };

  const handleVacationCalculator = (event: { detail: { text: number } }) => {
    VacationCalculator = event.detail.text;
  };

  $: submitDisabled = isErrorAddress == true || isErrorAddress == null;
</script>

<div class="container mt-5 pt-5">
  <div class="card">
    <div class="card-title pt-3">
      <h5 class="text-center text-muted">
        Apply for hr letter, Admin will see your request as soon as he/she can
      </h5>
    </div>
    <div class="card-body">
      <div class="row mt-4 d-flex justify-content-center">
        <div class="col-12">
          <div class="form-outline">
            <Input
              type="text"
              label={"Address"}
              bind:value={hrLetterData.addresses}
              handleInput={() => {
                return false;
              }}
              size={150}
              errorMessage="Invalid Address"
              hint={"please enter a valid address"}
              placeholder={"Enter Address"}
              bind:isError={isErrorAddress}
            />
          </div>
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              value=""
              id="salary-mention"
              bind:checked={hrLetterData.with_salary_mentioned}
            />
            <label class="form-check-label" for="salary-mention">
              salary should be mentioned
            </label>
          </div>
          <div class="form-check">
            <input
              class="form-check-input"
              bind:checked={hrLetterData.with_date}
              type="checkbox"
              value=""
              id="date-mention"
            />
            <label class="form-check-label" for="date-mention">
              with date mentioned
            </label>
          </div>
          {#if hrLetterData.with_date}
            {#if startDate && endDate}
              <div class="container" style="width: 40%;">
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
                        withReason={false}
                        withSubmit={false}
                      />
                    {/if}
                  </div>
                </CalendarDatePicker>
              </div>
            {/if}
          {/if}
        </div>
        <div class="col-12">
          <div
            class="card-body form-outline mt-4 d-flex justify-content-center"
          >
            <Submit
              width={"30"}
              bind:successMessage
              bind:errorMessage
              label="Submit"
              onClick={async () => {
                isLoading = true;
                try {
                  if (hrLetterData.with_date) {
                    hrLetterData.from_date = startDate;
                    hrLetterData.end_date = endDate;
                  } else {
                    hrLetterData.from_date = null;
                    hrLetterData.end_date = null;
                  }
                  const axios = await HRLetterDataService.post(hrLetterData);
                  isError = false;
                  successMessage = axios.data.message;
                } catch (error) {
                  isError = true;
                  errorMessage = error.message;
                } finally {
                  hrLetterData.addresses = "";
                  hrLetterData.with_date = false;
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
    </div>
  </div>
</div>
