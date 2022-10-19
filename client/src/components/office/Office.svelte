<script lang="ts">
    import Input  from '../input/Input.svelte';
    import Submit from '../submit/Submit.svelte';
    import MultiSelect from '../select/MultiSelect.svelte';
    import { weekendHolidaysChoices } from "../../services/utils/choices"
    import type { SelectOptionType } from "../../types"
    import OfficeDataService from '../../services/axios/offices/OfficeDataService';
    import { validateName } from '../../services/utils/validators';

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let officeName: string, officeCountry: string;
    let weekendHolidays: SelectOptionType[] = weekendHolidaysChoices
    let weekendHolidaysSelected: SelectOptionType[] = [];
    $: submitDisabled = 
        officeName == "" || officeName == undefined || officeName == null ||
        officeCountry == "" || officeCountry == undefined || officeCountry == null ||
        weekendHolidaysSelected.length == 0

</script>

<div class="bg-white rounded-5">
    <form>
        <div class="form-outline">
            <Input
                type="text"
                label={'Office Name'}
                bind:value={officeName}
                handleInput={validateName}
                size={25}
                errorMessage="Office name is invalid."
                placeholder="Office name."
                hint={'Write a valid office name'}
            />
        </div>
        <div class="form-outline">
            <Input
                type="text"
                label={'Office Country'}
                bind:value={officeCountry}
                handleInput={validateName}
                size={25}
                errorMessage="Office country is invalid."
                placeholder="office country"
                hint={'Write a valid office country'}
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
        <div class="form-outline mt-4  d-flex justify-content-end">
            <Submit
                width={'15'}
                successMessage={'Evaluation is Submitted'}
                errorMessage={' Evaluation Submission Failed'}
                label="Submit"
                onClick={async () => {
                    isLoading = true;
                    try {
                        await OfficeDataService.post({
                            weekend: weekendHolidaysSelected[0].value,
                            name: officeName,
                            country: officeCountry
                        });
                    } catch (error) {
                        isError = true;
                    } finally {
                        isLoading = false;
                        officeName = '';
                        officeCountry = '';
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