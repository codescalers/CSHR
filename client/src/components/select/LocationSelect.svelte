 <script lang="ts">
  import type {OfficeType } from '../../types';
  import officeDataService from '../../services/axios/offices/OfficeDataService';
  import { onMount } from 'svelte';
  import { OfficeStore } from '../../stores';
  import MultiSelect from './MultiSelect.svelte';
  import type { SelectOptionType } from './types';
  import ErrorComponent from '../error/ErrorComponent.svelte';
  import LoadingComponent from '../loader/LoadingComponent.svelte';
  export let placeholder = `Select Location`;
  export let removeAllTitle = 'Remove the location';
  export let isLoading = false;
  export let isError: boolean | null = null;
  export let mylabel = 'People';
  export let isTop : boolean ;
  export let selected: SelectOptionType[];
  let options: SelectOptionType[] = [];

  onMount(async () => {
    isLoading = true;
    try {
      if ($OfficeStore === undefined || $OfficeStore.length === 0) {
        const offices = await officeDataService.getAll();
        if ($OfficeStore === undefined) {
          $OfficeStore = offices;
        } else {
          OfficeStore.set(offices);
        }
      }
      $OfficeStore.forEach((office: OfficeType) => {
            options.push({
            value: office.id,
            label: office.name
          });
      });
    } catch (e) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if isError}
  <ErrorComponent />
{:else if (isLoading && !isError) || $OfficeStore === undefined}
  <LoadingComponent />
{:else if !isLoading && !isError}
  <MultiSelect
    bind:options
    bind:selected
    label= {mylabel}
    {placeholder}
    {removeAllTitle}
    isLabel={false}
    isTop ={isTop}
    multiple= {false}
  >
    <div let:option {option} slot="option" >
    {option.label}
    </div>
  </MultiSelect>
{/if}

         