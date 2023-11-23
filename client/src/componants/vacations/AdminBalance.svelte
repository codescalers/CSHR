<script lang="ts">
  import Vacation from "../../apis/vacations/Vacation";
  import type { VacationBalanceType } from "../../utils/types";
  import Submit from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import DatePickerSelect from "./DatePickerSelect.svelte";

  export let tab: number;

  let year: number = new Date().getFullYear();
  let isLoading = false;
  let isError = false;

  let dates: string[] = [];

  let balanceValues: VacationBalanceType = {
    annual_leaves: 0,
    emergency_leaves: 0,
    leave_excuses: 0,
  };

  const removeValues = () => {
    balanceValues.annual_leaves = 0;
    balanceValues.leave_excuses = 0;
    balanceValues.emergency_leaves = 0;
  };

  const handleDates = (dates_: string[]) => {
    if (dates_ != null) {
      dates_.forEach(thisDate => {
        let newdate = new Date(thisDate);
        dates.push(`${newdate.getFullYear()}-${newdate.getMonth() + 1}-${newdate.getDate()}`);
      });
    }
    return dates;
  };

  async function loadValues() {
    isLoading = true;
    balanceValues = await Vacation.getAdminbalance();
    isLoading = false;
  }

  $: submitDisabled =
    balanceValues.annual_leaves == 0 ||
    balanceValues.leave_excuses == 0 ||
    balanceValues.emergency_leaves == 0 ||
    isLoading;

  $: if (tab === 1) loadValues();

  let successMessage: string;
  let errorMessage: string;
</script>

{#if balanceValues && balanceValues.location}
  <div class="bg-white p-3 pt-0 mt-0 card">
    <div class="card-body">
      <div class="text-center">
        <small>
          The displayed values reflect the current year's data for the respective office. If you wish to generate new
          values, please change the year. Otherwise, the existing data for <strong>{year}</strong> will be modified.
        </small>
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Office location"}
          bind:value={balanceValues.location.country}
          handleInput={() => {
            return false;
          }}
          size={25}
          errorMessage="location is invalid."
          placeholder="Office location"
          hint={"This field is not editable."}
          disabled
        />
      </div>
      <div class="form-outline">
        <Input
          type="number"
          label={"Values for year"}
          bind:value={balanceValues.year}
          handleInput={() => {
            return false;
          }}
          size={25}
          errorMessage="Year is invalid."
          placeholder="Balance Year"
          hint={"Write the year of the values"}
        />
      </div>
      <div class="form-outline">
        <Input
          type="number"
          label={"Annual leaves"}
          bind:value={balanceValues.annual_leaves}
          handleInput={() => {
            return false;
          }}
          size={25}
          errorMessage="Annual leaves is invalid."
          placeholder="Annual leaves"
          hint={"Write annual leaves in numbers"}
        />
      </div>
      <div class="form-outline">
        <Input
          type="number"
          label={"Leave execuses"}
          bind:value={balanceValues.leave_excuses}
          handleInput={() => {
            return false;
          }}
          size={25}
          errorMessage="Leave execuses is invalid."
          placeholder="Leave execuses"
          hint={"Write Leave execuses in numbers"}
        />
      </div>
      <div class="form-outline">
        <Input
          type="number"
          label={"Emergency leaves"}
          bind:value={balanceValues.emergency_leaves}
          handleInput={() => {
            return false;
          }}
          size={25}
          errorMessage="Emergency leaves is invalid."
          placeholder="Emergency leaves"
          hint={"Write Emergency leaves in numbers"}
        />
      </div>

      <DatePickerSelect on:selectedDate={removeValues} bind:date={balanceValues.public_holidays} />

      <div class="col-12 mt-4 d-flex justify-content-end">
        <Submit
          width={"30"}
          bind:successMessage
          bind:errorMessage
          label="Set Balance"
          onClick={async () => {
            isLoading = true;
            try {
              isError = false;
              await Vacation.postAdminBalance({
                annual_leaves: balanceValues.annual_leaves,
                leave_excuses: balanceValues.leave_excuses,
                emergency_leaves: balanceValues.emergency_leaves,
                public_holidays: handleDates(balanceValues.public_holidays),
                year: balanceValues.year,
                location: balanceValues.location,
              });
              successMessage = "The vacation balances have been added/updated successfully.";
              await loadValues();
            } catch (error) {
              errorMessage =
                "Error while trying to update/add vacation balances, please try again and check the provided data.";
              isError = true;
            } finally {
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
{/if}
