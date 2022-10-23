<script lang="ts">
    import Input from '../input/Input.svelte';
    import Submit from '../submit/Submit.svelte';
    import CalendarLeaveForm from '../calendar/CalendarLeaveForm.svelte';
    import CalendarDatePicker from '../calendar/CalendarDatePicker.svelte';
    import CompensationsDataService from "../../services/axios/compensation/compensations"
    import type { CompensationType } from "../../types"
    import { onMount } from 'svelte';
    import { RequestStatus } from '../../services/utils/enums';
    import { Route } from 'svelte-navigator';
    import Error from '../../pages/Error.svelte';

    export let isLoading: boolean|null = false;
    export let isError: boolean|null = false;

    let CompensationData: CompensationType;
    var path = window.location.pathname;
    const compensationID = path.split("/")[2];
    let startDate: string, endDate: string;

    if (! +compensationID){
        isError = true;
    }

    onMount(async function () {
        const CompensationDataAPI = await CompensationsDataService.getByID(+compensationID);
        CompensationData = CompensationDataAPI.data.results;
        CompensationData.applying_user = CompensationDataAPI.data.results.applying_user.id
        startDate = CompensationData.from_date;
        endDate = CompensationData.end_date;
    });

    let isErrorReason: boolean | null = null;
    let isErrorDates: boolean;
    let datePickerDisabled = false;
    let successMessage: string;
    let errorMessage: string;
  

    $: submitDisabled = 
        isErrorReason == true || startDate == "" || endDate == "";
</script>
{#if CompensationData}
    {#if CompensationData.status != RequestStatus.pinding}
        <Route>
            <Error error={404} />
        </Route>
    {/if}
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
                            const axios = await CompensationsDataService.update(CompensationData, +compensationID);
                            successMessage = axios.data.message;
                            isError = false;
                        } catch (error) {
                            isError = true;
                            errorMessage = error.message;
                            console.log(error);
                            
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