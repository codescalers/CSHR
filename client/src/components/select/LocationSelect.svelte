<script lang="ts">
  import officeDataService from "../../services/axios/offices/OfficeDataService";
  import type { OfficeInterface } from "../../types";
  import { onMount } from "svelte";
  import { OfficeStore } from "../../stores";
  import Select from "./Select.svelte";
  export let selected: number[] = [];
  export let placeholder = `Select Users`;
  export let removeAllTitle = "Remove all users";
  export let isLoading = false;
  export let isError: boolean | null = null;
  export let options: string[] = [];

  onMount(async () => {
    isLoading = true;
    try {
      if ($OfficeStore.length === 0) {
        const offices = await officeDataService.getAll();
        OfficeStore.set(offices);
        options = offices.map((office: OfficeInterface) => office.id + "");
      }
    } catch (e) {
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
