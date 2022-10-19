<script lang="ts">
  import DatePicker from './Datepicker.svelte';
  import Input from '../input/Input.svelte';
  import Vacation from '../../services/axios/vacations/Vacation';
  import { createEventDispatcher } from 'svelte';
  export let startDate = '2022-03-01';
  export let endDate = '2022-03-03';
  export let errorMessage = '';
  export let onlyStart = false;
  export let isLoading = false;
  export let datePickerDisabled = true;

  const dispatch = createEventDispatcher();

  const locale: {
    en: {
      days: string[];
      months: string[];
      start: number;
    };
  } = {
    en: {
      days: 'Su|Mo|Tu|We|Th|Fr|Sa'.split('|'),
      months: 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'.split('|'),
      start: 0,
    },
  };
  async function validateDate(date: string, error_name: string): Promise<boolean> {
    const vacationCalculator = await Vacation.calculator(startDate, endDate);
    dispatch('message', {
			text: vacationCalculator
		});
    let check = Date.parse(date);
    if (!check) {
      //it is not a date with format YYYY-MM-DD
      errorMessage = `${error_name} format is invalid message`;
      datePickerDisabled = true;
      return true;
    } else {
      errorMessage = '';
      datePickerDisabled = false;
      return false;
    }
    //it is a date with format YYYY-MM-DD
  }
  $: validateDate(startDate, 'Start Date');
  $: validateDate(endDate, 'End Date');
</script>

<div class="container table-primary table-responsive">
  <fieldset
    id="isloading"
    disabled={isLoading}
    style={` opacity: ${isLoading ? '0.1' : '1'}`}
  >
    {#if !errorMessage}
      <div>
        <DatePicker
          bind:startDate
          bind:endDate
          bind:onlyStart
          {...locale['en']}
        />
      </div>
    {:else}
      <div class="alert alert-danger" role="alert">
        {errorMessage}
      </div>
    {/if}

    <div class="mx-5">
      <slot name="toggler" />

      <div class="my-4 px-3">
        <Input
          label={(!onlyStart ? 'Start ' : '') + 'Date'}
          bind:value={startDate}
          type="text"
          hint={'with this Format YYYY-MM-DD.'}
          errorMessage={'Please provide a valid Start Date'}
          handleInput={() => {
            return validateDate(startDate, 'Start Date');
          }}
          size={20}
          placeholder={'start date'}
          isError={errorMessage.charAt(0) === 'S'}
        />

        {#if !onlyStart}
          <Input
            label="End Date"
            bind:value={endDate}
            type="text"
            hint={'with this Format YYYY-MM-DD.'}
            errorMessage={'Please provide a valid End Date'}
            handleInput={() => {
              return validateDate(endDate, 'End Date');
            }}
            size={20}
            placeholder={'end date'}
            isError={errorMessage.charAt(0) === 'E'}
          />
        {/if}
        <slot name="form" />
      </div>
    </div>
  </fieldset>
</div>
