<script lang="ts">
  import "flatpickr/dist/flatpickr.css";
  import "flatpickr/dist/themes/light.css";

  import { createEventDispatcher } from "svelte";
  import Flatpickr from "svelte-flatpickr";

  import Vacation from "../../apis/vacations/Vacation";
  import { formatDate } from "../../utils/helpers";
  import type { CalenderRequestFormResponseType } from "../../utils/types";
  import { validateStartEndDates } from "../../utils/validations";
  import Alert from "../ui/Alert.svelte";

  export let startDate: string | Date;
  export let endDate: string | Date;

  export let onlyStart = false;
  export let calculate = true;

  let errorMessage: string | undefined;

  startDate = new Date(startDate);
  endDate = new Date(endDate);

  const dispatch = createEventDispatcher();

  async function calculateActualVacationBalance() {
    const vacationCalculator = await Vacation.calculator(
      formatDate(startDate as Date),
      formatDate(endDate as Date)
    );

    dispatch("calculate", {
      days: vacationCalculator
    });
  }

  function validateDate(): CalenderRequestFormResponseType {
    errorMessage = undefined;

    let validated: CalenderRequestFormResponseType = validateStartEndDates(
      startDate as Date,
      endDate as Date
    );

    if (!validated.isError && calculate) {
      calculateActualVacationBalance();
    }
    errorMessage = validated.message;
    return validated;
  }

  $: startDate, validateDate();
  $: endDate, validateDate();
</script>

<div class="container table-primary table-responsive">
  <div class="mx-5">
    <slot name="toggler" />

    <div class="my-4 px-3">
      <div class="end-date">
        <Flatpickr bind:value={startDate} element="#start-day">
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
          <Flatpickr bind:value={endDate} element="#end-day">
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
