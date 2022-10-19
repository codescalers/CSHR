<script lang="ts">
    import Submit from '../submit/Submit.svelte';
	import Flatpickr from 'svelte-flatpickr'
	import 'flatpickr/dist/flatpickr.css'
	import 'flatpickr/dist/themes/light.css'
    import Vacation from "../../services/axios/vacations/Vacation"
    
    export let isLoading: boolean = false;
    export let isError: boolean = false;
    export let annualValue: number, leaveValue: number, emergencyValue: number = -1;

    let date: any = null
    let dates: string[] = []

	const flatpickrOptions = {
        mode: "multiple",
		element: '#my-picker'
	}
    
    $:submitDisabled = 
        annualValue == 0 || 
        leaveValue == 0 || 
        emergencyValue == 0 || 
        date == null || date.length == 0;

    const handleDates = (dates_: string[]) => {        
        dates_.forEach(thisDate => {
            let newdate = new Date(thisDate)
            dates.push(`${newdate.getFullYear()}-${newdate.getMonth()+1}-${newdate.getDate()}`)
        });  
        return dates;
    }
</script>

<Flatpickr options="{ flatpickrOptions }" bind:value={date} element="#my-picker">
    <div class="flatpickr form-outline mb-4" id="my-picker">
        <div class="form-group row">
            <div class="col-4">
                <label class="col-sm-4 col-form-label py-3" for="datePickerInput">Public holidays</label>
            </div>
            <div class="col-sm-8">
                <input class="form-control" id="datePickerInput" type="text" placeholder="Select Date.." data-input>
            </div>
        </div>
    </div>
</Flatpickr>

<div class="col-12 mt-4  d-flex justify-content-end">
    <Submit
        width={'15'}
        successMessage={'Evaluation is Submitted'}
        errorMessage={' Evaluation Submission Failed'}
        label="Submit"
        onClick={async () => {
        isLoading = true;
        try {
            await Vacation.postAdminBalance({
                annual_leaves: +annualValue,
                leave_execuses: +leaveValue,
                emergency_leaves: +emergencyValue,
                public_holidays: handleDates(date),
            });
        } catch (error) {
            isError = true;
        } finally {
            isLoading = false;
            annualValue = 0;
            leaveValue = 0;
            emergencyValue = 0;
            date = null;
            dates = [];
        }
        return isError;
        }}
        className=""
        bind:disabled={submitDisabled}
    />
</div>

<style>
    input {
        margin-top: 0.3cm !important;
        background-color: var(--secondary-color) !important;
    }
    .form-control {
        display: block;
        width: 100%;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.5;
        color: rgb(33 37 41);
        background-color: rgb(255 255 255);
        background-clip: padding-box;
        border: 1px solid rgb(206 212 218);
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        border-radius: 0.375rem;
        transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
    }
</style>