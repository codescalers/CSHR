<script lang="ts">
  import officeDataService from '../../services/axios/offices/OfficeDataService';
  import type { OfficeType } from '../../types';
  import type { SelectOptionType } from './types';
  import { onMount } from 'svelte';
  import { OfficeStore } from '../../stores';
  import Select from './Select.svelte';
  export let selected: SelectOptionType[] = [];
  export let placeholder = `Select Locations`;
  export let removeAllTitle = 'Remove all Locations';
  export let isLoading = false;
  export let isError: boolean | null = null;
  export let options: SelectOptionType[] = [];

  onMount(async () => {
    isLoading = true;
    try {
      if ($OfficeStore.length === 0) {
        const offices = await officeDataService.getAll();
        OfficeStore.set(offices);
        options = offices.map((office: OfficeType) => office.id + '');
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

<Select
  bind:options
  bind:selected
  bind:isError
  {placeholder}
  {removeAllTitle}
  bind:isLoading
/>
