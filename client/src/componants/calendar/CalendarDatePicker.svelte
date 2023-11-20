<script lang="ts">
  import DatePicker from "./DatePicker.svelte";
  import Input from "../ui/Input.svelte";
  import Vacation from "../../apis/vacations/Vacation";
  import { createEventDispatcher } from "svelte";
  import { validateStartEndDates } from "../../utils/validations";
  import type { CalenderRequestFormResponseType } from "../../utils/types";
  export let startDate = "2022-03-01";
  export let endDate = "2022-03-03";
  export let errorMessage = "";
  export let onlyStart = false;
  export let isLoading = false;
  export let datePickerDisabled = true;
  export let calculate: boolean = true;

  const dispatch = createEventDispatcher();
  let today = new Date();

  const locale: {
    en: {
      days: string[];
      months: string[];
      start: number;
    };
  } = {
    en: {
      days: "Su|Mo|Tu|We|Th|Fr|Sa".split("|"),
      months: "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split("|"),
      start: 0,
    },
  };

  async function calculateActualVacationBalance() {
    const vacationCalculator = await Vacation.calculator(startDate, endDate);
    dispatch("message", {
      text: vacationCalculator,
    });
  }

  function validateDate(date: string): CalenderRequestFormResponseType {
    let validated: CalenderRequestFormResponseType = validateStartEndDates(
      date,
      startDate,
      endDate
    );

    if (validated.isError == false && calculate) {
      calculateActualVacationBalance();
    }
    errorMessage = validated.message;
    return validated;
  }

  $: validateDate(startDate);
  $: validateDate(endDate);
</script>

<div class="container table-primary table-responsive">
  <fieldset
    id="isloading"
    disabled={isLoading}
    style={` opacity: ${isLoading ? "0.1" : "1"}`}
  >
    {#if errorMessage}
      <div class="mt-3">
        <DatePicker
          bind:startDate
          bind:endDate
          bind:onlyStart
          {...locale["en"]}
        />
      </div>
    {/if}

    <div class="mx-5">
      <slot name="toggler" />

      <div class="my-4 px-3">
        <Input
          label={(!onlyStart ? "Start " : "") + "Date"}
          bind:value={startDate}
          type="text"
          hint={"Right Format YYYY-MM-DD."}
          {errorMessage}
          handleInput={() => {
            return validateDate(startDate).isError;
          }}
          size={20}
          placeholder={"Start Date"}
          disabled={true}
        />

        {#if !onlyStart}
          <Input
            label="End Date"
            bind:value={endDate}
            type="text"
            hint={"Right Format YYYY-MM-DD."}
            {errorMessage}
            handleInput={() => {
              return validateDate(startDate).isError;
            }}
            size={20}
            placeholder={"End Date"}
            disabled={true}
          />
        {/if}
        <slot name="form" />
      </div>
    </div>
  </fieldset>
</div>
