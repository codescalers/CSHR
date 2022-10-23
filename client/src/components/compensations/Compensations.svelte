<script lang="ts">
    import Input from '../input/Input.svelte';
    import Submit from '../submit/Submit.svelte';
    import CalendarLeaveForm from '../calendar/CalendarLeaveForm.svelte';
    import CalendarDatePicker from '../calendar/CalendarDatePicker.svelte';
    import CompensationsDataService from "../../services/axios/compensation/compensations"
    import type { CompensationType } from "../../types"

    export let isLoading: boolean = false;
    export let isError: boolean = false;

    let isErrorReason: boolean | null = null;
    let isErrorDates: boolean;
    let thisDate: Date = new Date();
    let startDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate()}`;
    let endDate = `${thisDate.getFullYear()}-${thisDate.getMonth() + 1}-${thisDate.getDate() + 2}`;
    let datePickerDisabled = false;
    let successMessage: string;
    let errorMessage: string;
  
    let CompensationData: CompensationType = {
        "from_date": "",
        "end_date": "",
        "reason": "",
    } ;

    $: submitDisabled = 
        isErrorReason == true || isErrorReason == null;
</script>

<h5 class="text-center text-muted">Apply for compensation days, Admin will see your request as soon as he/she can</h5>

<div class="row mt-4 d-flex justify-content-center">
    <div class="col-12">
        <div class="container" style="width: 30%;">
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
                            label={'Reason'}
                            bind:value={ CompensationData.reason }
                            handleInput={ () => {return false;}}
                            size={150}
                            errorMessage="Invalid Reason"
                            hint={'please enter a valid reason'}
                            placeholder={'Enter Reason'}
                            bind:isError={ isErrorReason }
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
                width={'30'}
                successMessage={successMessage}
                errorMessage={errorMessage}
                label="Submit"
                onClick={async () => {
                    isLoading = true;
                    try {
                        CompensationData.from_date = startDate;
                        CompensationData.end_date = endDate;
                        const axios = await CompensationsDataService.post(CompensationData);
                        successMessage = axios.data.message;
                        isError = false;
                    } catch (error) {
                        isError = true;
                        errorMessage = error.message;
                        console.log(error);
                        
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
