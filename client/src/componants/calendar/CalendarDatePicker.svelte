<script lang="ts">
  import "flatpickr/dist/flatpickr.css";
  import "flatpickr/dist/themes/light.css";

  import { createEventDispatcher } from "svelte";
  import Flatpickr, { type SvelteFlatpickrProps } from "svelte-flatpickr";

  import Vacation from "../../apis/vacations/Vacation";
  import type { CalenderRequestFormResponseType } from "../../utils/types";
  import { validateStartEndDates } from "../../utils/validations";
  import Alert from "../ui/Alert.svelte";

  const today = new Date();
  export let startDate: string = `${today.getFullYear()}-${
    today.getMonth() + 1
  }-${today.getDate()}`;
  export let endDate: string = `${today.getFullYear()}-${
    today.getMonth() + 1
  }-${today.getDate() + 3}`;

  export let onlyStart = false;
  export let calculate = true;

  let errorMessage: string | undefined;
  const dispatch = createEventDispatcher();

  async function calculateActualVacationBalance() {
    const vacationCalculator = await Vacation.calculator(startDate, endDate);

    dispatch("calculate", {
      days: vacationCalculator
    });

    dispatch("updateDates", {
      startDate,
      endDate
    });
  }

  function validateDate(): CalenderRequestFormResponseType {
    errorMessage = undefined;

    let validated: CalenderRequestFormResponseType = validateStartEndDates(
      startDate,
      endDate
    );

    if (!validated.isError && calculate) {
      calculateActualVacationBalance();
    }
    errorMessage = validated.message;
    return validated;
  }

  $: startDate, validateDate();
  $: endDate, validateDate();

  let startDateOptions: SvelteFlatpickrProps["options"] = {
    defaultDate: startDate,
    onValueUpdate: (_selectedDates: Date[], dateStr: string) => {
      startDate = dateStr;
    }
  };

  let endDateOptions: SvelteFlatpickrProps["options"] = {
    defaultDate: endDate,
    onValueUpdate: (_selectedDates: Date[], dateStr: string) => {
      endDate = dateStr;
    }
  };
</script>

<div class="container table-primary table-responsive">
  <div class="mx-5">
    <slot name="toggler" />

    <div class="my-4 px-3">
      <div class="end-date">
        <Flatpickr
          bind:value={startDateOptions["defaultDate"]}
          bind:options={startDateOptions}
          element="#start-day"
        >
          <div class="flatpickr form-outline mb-4" id="start-day">
            <div class="form-group row pt-2">
              <div class="col-6 d-flex align-items-center">
                <label for="startDayInput"> Start day </label>
              </div>

              <div class="col-6 d-flex align-items-center">
                <input
                  class="form-control"
                  id="startDayInput"
                  type="text"
                  placeholder="Select Start Day."
                  data-input
                />
              </div>
            </div>
          </div>
        </Flatpickr>
      </div>

      {#if !onlyStart}
        <div class="end-date">
          <Flatpickr
            bind:options={endDateOptions}
            bind:value={endDateOptions["defaultDate"]}
            element="#end-day"
          >
            <div class="flatpickr form-outline mb-4" id="end-day">
              <div class="form-group row">
                <div class="col-6 d-flex align-items-center">
                  <label for="endDayInput"> End day </label>
                </div>

                <div class="col-6 d-flex align-items-center">
                  <input
                    class="form-control"
                    id="endDayInput"
                    type="text"
                    placeholder="Select End Day."
                    data-input
                  />
                </div>
              </div>
            </div>
          </Flatpickr>
        </div>
      {/if}
      <slot name="form" />

      {#if errorMessage}
        <div class="mt-2">
          <Alert title={"Error"} message={errorMessage} className={"danger"} />
        </div>
        <!-- <small class="text-danger">{errorMessage}</small> -->
      {/if}
    </div>
  </div>
</div>
