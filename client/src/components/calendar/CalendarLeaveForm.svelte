<script lang="ts">
  import Submit from '../submit/Submit.svelte';
  import Alert from "../alert/Alert.svelte"
  import {onMount} from "svelte";
  import CalendarDataService from '../../services/axios/home/CalendarDataService';
  import { UserStore } from '../../stores';
  import type { VacationBalanceType } from '../../types';
  import Vacation from '../../services/axios/vacations/Vacation';

  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let datePickerDisabled = false;
  export let calculatorValue: number;
  export let isUpdate = false;
  export let selectedReason: any = 0;
  export let vacationID: string;
  let errorMessage: string = "", successMessage: string = "";

  let alertTitle: string, alertClass: string, alertMessage: string, showAlert: boolean;

  let vBalance: VacationBalanceType;
  onMount(async ()=>{
    vBalance = await Vacation.balance($UserStore.id);
  });

  $: submitDisabled =
    selectedReason == 0 || datePickerDisabled == true 
</script>


<form>
  <div class="form-group row">
    <label class="col-sm-4 col-form-label py-3" for="Reason">Reason</label>
    <div class="col-sm-8">
      <select bind:value={selectedReason} id="Reason" class="form-select form-control" aria-label="Default select example">
        {#if vBalance}
          {#each Object.entries(vBalance) as [name, _value]}
              <option value={name}>{name} {_value}</option>
          {/each}
        {/if}
      </select>
    </div>
  </div>
  <div class="alert alert-light p-0 text-center">
    Actual value after deducting weekend holidays {calculatorValue}
  </div>
  <div>
    <Submit
      successMessage={successMessage}
      errorMessage={errorMessage}
      label="Submit"
      onClick={async () => {
        isLoading = true;
          try {
            if(isUpdate){
              const axios = await CalendarDataService.updateVacation(vacationID, {
                end_date: endDate,
                from_date: startDate,
                reason: selectedReason,
                applyingUserId: $UserStore.id,
              });
              successMessage = axios.message
            } else {
              const axios = await CalendarDataService.postLeave({
                end_date: endDate,
                from_date: startDate,
                reason: selectedReason,
                applyingUserId: $UserStore.id,
              });
              successMessage = axios.data.message
            }
          } catch (error) {
              isError = true;
              console.log(error);
              errorMessage = error.message
          } finally {
              isLoading = false;
          }
          return isError;
      }}
      className=""
      bind:disabled={submitDisabled}
    />
  </div>
{#if showAlert}
  <div class="mt-2">
    <Alert title={alertTitle} message={alertMessage} type={alertClass}/>
  </div>
{/if}
</form>

<style>
.form-control {
  display: block;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: rgb(33 37 41);
  background-clip: padding-box;
  border: 1px solid rgb(206 212 218);
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0.375rem;
  transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
}
select{
  margin-top: 0.3cm;
  background-color: var(--secondary-color);
}
select:focus{
  margin-top: 0.3cm;
  background-color: var(--secondary-color);
}
</style>