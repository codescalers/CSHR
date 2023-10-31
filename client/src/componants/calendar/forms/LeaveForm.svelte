<script lang="ts">
  import Submit from '../../ui/Button.svelte';
  import Alert from "../../ui/Alert.svelte"
  import {onMount} from "svelte";
  import Vacations from '../../../apis/vacations/Vacation';
  import { UserStore } from '../../../utils/stores';
  import type { VacationBalance, calendarItemsType } from '../../../utils/types';
  import { createEventDispatcher } from 'svelte';

  export let startDate: string;
  export let endDate: string;
  export let isLoading = false;
  export let isError = false;
  export let datePickerDisabled = false;
  export let calculatorValue: number = 0;
  export let isUpdate = false;
  export let selectedReason: any = 0;
  export let vacationID: string="";
  export let withReason: boolean = true;
  export let withSubmit: boolean = true;
  export let showCalclator: boolean = true;

  let errorMessage: string = "", successMessage: string = "";
  let alertTitle: string, alertClass: string, alertMessage: string, showAlert: boolean;
  let vBalance: VacationBalance;
  let responseVacation: calendarItemsType;
  const dispatch = createEventDispatcher();

  onMount(async ()=>{
    vBalance = await Vacations.balance($UserStore.id);
  });
  

  $: submitDisabled =
    selectedReason == 0 || datePickerDisabled == true

</script>

<form>
  {#if withReason}
    <div class="form-group row">
      <label class="col-sm-4 col-form-label py-3" for="Reason">Reason</label>
      <div class="col-sm-8">
        <select bind:value={selectedReason} id="Reason" class="form-select form-control" aria-label="Default select example">
          {#if vBalance}
            {#each Object.entries(vBalance) as [name, _value]}
                {#if name != "user"}
                  <option value={name}>{name} {_value.reserved} / {_value.all}</option>
                {/if}
            {/each}
          {/if}
        </select>
      </div>
    </div>
  {/if}
  {#if showCalclator}
    <div class="alert alert-light p-0 text-center">
      Actual value after deducting weekend holidays {calculatorValue}
    </div>
  {/if}
  {#if withSubmit}
    <div>
      <Submit
        successMessage={successMessage}
        errorMessage={errorMessage}
        label="Request"
        onClick={async () => {
          isLoading = true;
            try {
              if(isUpdate && vacationID != ""){
                const axios = await Vacations.update(vacationID, {
                  end_date: endDate,
                  from_date: startDate,
                  reason: selectedReason,
                  applyingUserId: $UserStore.id,
                });
                successMessage = axios.message
              } else {
                const axios = await Vacations.post({
                  end_date: endDate,
                  from_date: startDate,
                  reason: selectedReason,
                  applyingUserId: $UserStore.id,
                });
                successMessage = axios.data.message
                responseVacation = axios.data.results
                dispatch('message', {
                  postedVacation: responseVacation
                });
                vBalance[selectedReason].reserved = vBalance[selectedReason].reserved + calculatorValue
              }
            } catch (error) {
                isError = true;
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
  {/if}
{#if showAlert}
  <div class="mt-2">
    <Alert title={alertTitle} message={alertMessage} className={alertClass}/>
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
