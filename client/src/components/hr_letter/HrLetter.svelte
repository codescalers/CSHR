<script lang="ts">
    import Input from '../input/Input.svelte';
    import Submit from '../submit/Submit.svelte';
    import CalendarLeaveForm from '../calendar/CalendarLeaveForm.svelte';
    import CalendarDatePicker from '../calendar/CalendarDatePicker.svelte';
    import type { HRLetterType } from "../../types"
    import HRLetterDataService from "../../services/axios/hr_letter/hr_letter"

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let isErrorAddress: boolean | null = null;
    let thisDate: Date = new Date();
    let startDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate()}`;
    let endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate() + 2}`;
    let formToggle: number = 0;
    let datePickerDisabled = false;
    let successMessage: string;
    let errorMessage: string;

    let VacationCalculator: number;
  
    let hrLetterData: HRLetterType = {
        "from_date": "",
        "end_date": "",
        "addresses": "",
        "with_date": false,
        "with_salary_mentioned": false,
    } ;

    const handleVacationCalculator = (event: { detail: { text: number; }; }) => {
      VacationCalculator = event.detail.text;
    };

    $: submitDisabled = 
        isErrorAddress == true || isErrorAddress == null;
</script>

<h5 class="text-center text-muted">Apply for hr letter, Admin will see your request as soon as he/she can</h5>

<div class="row mt-4 d-flex justify-content-center">
    <div class="col-12">
        <div class="container" style="width: 30%;">
            {#if hrLetterData.with_date }
                {#if startDate && endDate}
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
                                calculatorValue = {VacationCalculator}
                                withReason={false}
                                withSubmit={false}
                            />
                        {/if}
                    </div>
                    </CalendarDatePicker>
                {/if}
            {/if}
            <div class="form-outline">
                <Input
                    type="text"
                    label={'Address'}
                    bind:value={ hrLetterData.addresses }
                    handleInput={ () => {return false;}}
                    size={150}
                    errorMessage="Invalid Address"
                    hint={'please enter a valid address'}
                    placeholder={'Enter Address'}
                    bind:isError={ isErrorAddress }
                /> 
            </div>
            <div class="form-check">
                <input class="form-check-input"
                    type="checkbox" value="" id="salary-mention" 
                        bind:checked={hrLetterData.with_salary_mentioned}
                >
                <label class="form-check-label" for="salary-mention">
                    salary should be mentioned
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" bind:checked={hrLetterData.with_date} 
                    type="checkbox" value="" id="date-mention">
                <label class="form-check-label" for="date-mention">
                    with date mentioned
                </label>
            </div>
        </div>        
    </div>
    <div class="col-12">
        <div class="form-outline mt-4 d-flex justify-content-center">
            <Submit
                width={'30'}
                successMessage={successMessage}
                errorMessage={errorMessage}
                label="Submit"
                onClick={async () => {
                    isLoading = true;
                    try {
                        if(hrLetterData.with_date){
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
