<script lang="ts">
  import Input from "../ui/Input.svelte";
  import Submit from "../ui/Button.svelte";
  import MultiSelect from "../ui/select/MultiSelect.svelte";
  import { weekendHolidaysChoices } from "../../utils/choices";
  import type { SelectOptionType } from "../../utils/types";
  import OfficeDataService from "../../apis/offices/Office";
  import { validateName } from "../../utils/validations";

  export let isLoading: boolean = false;
  export let isError: boolean = false;

  let officeName: string;
  let officeCountry: string;
  let weekendHolidays: SelectOptionType[] = weekendHolidaysChoices;
  let weekendHolidaysSelected: SelectOptionType[] = [];
  let successMessage: string;
  let errorMessage: string;

  $: submitDisabled =
    officeName == "" ||
    officeName == undefined ||
    officeName == null ||
    officeCountry == "" ||
    officeCountry == undefined ||
    officeCountry == null ||
    weekendHolidaysSelected.length == 0;
</script>

<div class="bg-white p-3 card">
  <div class="card-body">
    <form>
      <div class="form-outline">
        <Input
          type="text"
          label={"Office Name"}
          bind:value={officeName}
          handleInput={validateName}
          size={25}
          errorMessage="Office name is invalid."
          placeholder="Office name."
          hint={"Write a valid office name"}
        />
      </div>
      <div class="form-outline">
        <Input
          type="text"
          label={"Office Country"}
          bind:value={officeCountry}
          handleInput={validateName}
          size={25}
          errorMessage="Office country is invalid."
          placeholder="office country"
          hint={"Write a valid office country"}
        />
      </div>
      <div class="form-outline">
        <MultiSelect
          bind:options={weekendHolidays}
          bind:selected={weekendHolidaysSelected}
          isLabel={true}
          label="Weekend Holidays"
          placeholder="Select Weekend Holidays"
          removeAllTitle="Remove all Weekend Holidays"
          multiple={false}
        />
      </div>
      <div class="form-outline mt-4 d-flex justify-content-end">
        <Submit
          width={"15"}
          bind:successMessage
          bind:errorMessage
          label="Submit"
          onClick={async () => {
            isLoading = true;
            try {
              await OfficeDataService.post({
                weekend: weekendHolidaysSelected[0].value,
                name: officeName,
                country: officeCountry,
              });

              successMessage = "The new office has been created successfully.";
            } catch (error) {
              errorMessage = "Error while trying to create a new office.";
              isError = true;
            } finally {
              isLoading = false;
              officeName = "";
              officeCountry = "";
              weekendHolidaysSelected = [];
            }
            return isError;
          }}
          className=""
          bind:disabled={submitDisabled}
        />
      </div>
    </form>
  </div>
</div>
