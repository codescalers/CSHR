<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import Vacation from "../../apis/vacations/Vacation";
  import type { CalenderRequestFormResponseType } from "../../utils/types";
  import { validateStartEndDates } from "../../utils/validations";
  import "flatpickr/dist/flatpickr.css";
  import "flatpickr/dist/themes/light.css";

  import Flatpickr from "svelte-flatpickr";

  export let startDate: string;
  export let endDate: string;

  export let onlyStart = false;
  export let calculate = true;
  
  let errorMessage: string | undefined;

  const dispatch = createEventDispatcher();

  async function calculateActualVacationBalance() {
    const vacationCalculator = await Vacation.calculator(startDate, endDate);
    dispatch("message", {
      text: vacationCalculator,
    });
  }

  function validateDate(date: string): CalenderRequestFormResponseType {
    const _startDate = new Date(startDate) 
    const _endDate = new Date(endDate) 

    let validated: CalenderRequestFormResponseType = validateStartEndDates(_startDate, _endDate);
    console.log(validated);

    if (validated.isError == false && calculate) {
      calculateActualVacationBalance();
    }
    errorMessage = validated.message;
    return validated;
  }

  $: startDate, validateDate(startDate);
  $: endDate, validateDate(endDate);
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
                  <label for="startDayInput">
                    Start day
                  </label>
                </div>
          
                <div class="col-6 d-flex align-items-center">
                  <input class="form-control" id="startDayInput" type="text" placeholder="Select Start Day." data-input />
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
                    <label for="endDayInput">
                      End day
                    </label>
                  </div>
            
                  <div class="col-6 d-flex align-items-center">
                    <input class="form-control" id="endDayInput" type="text" placeholder="Select End Day." data-input />
                  </div>
            
                </div>
              </div>
            </Flatpickr>
          </div>
        {/if}
        <slot name="form" />
      </div>
    </div>
</div>
