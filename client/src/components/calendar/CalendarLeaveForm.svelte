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

  let alertTitle: string, alertClass: string, alertMessage: string, showAlert: boolean;

  let selectedReason: any = 0;
  let vBalance: VacationBalanceType;

  onMount(async ()=>{
    vBalance = await Vacation.balance();
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
            {#if _value == 100}
              <option value={name}>{name}</option>
            {:else}
              <option value={name}>{name} {_value}</option>
            {/if}
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
      showthis={false}
      label="Submit"
      onClick={async () => {
        isLoading = true;
        try {
          const axios = await CalendarDataService.postLeave({
            end_date: endDate,
            from_date: startDate,
            reason: selectedReason,
            applyingUserId: $UserStore.id,
          });
          if (axios.status != 201){
            alertMessage = axios.response.data.message;
            alertTitle = "Leave Submission Failed"
            alertClass = "danger";
          } else {
            alertMessage = axios.data.message;
            alertClass = "success";
            alertTitle = "Leave Submitted"
          }
          showAlert = true;
        } catch (error) {
          isError = true;
        } finally {
          isLoading = false;
          selectedReason = 0;
        }
        return isError;
      }}
      disabled={submitDisabled}
    />
  </div>
{#if showAlert}
  <Alert title={alertTitle} message={alertMessage} type={alertClass}/>
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