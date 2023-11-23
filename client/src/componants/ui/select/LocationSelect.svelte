<script lang="ts">
  import { onMount } from "svelte";

  import officeDataService from "../../../apis/offices/Office";
  import { OfficeStore } from "../../../utils/stores";
  import type { OfficeType, SelectOptionsComponent } from "../../../utils/types";
  import ErrorComponent from "../../error/ErrorComponent.svelte";
  import LoadingComponent from "../../ui/Loading.svelte";
  import MultiSelect from "./MultiSelect.svelte";

  export let options: SelectOptionsComponent;
  export let isLoading = false;

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
        options.optionsList.push({
          value: office.id,
          label: office.name,
        });
      });
      if (!options.selected.length) {
        options.selected.push(options.optionsList[0]);
      }
    } catch (e) {
      options.isError = true;
    }
    isLoading = false;
  });
</script>

{#if options.isError}
  <ErrorComponent />
{:else if (isLoading && !options.isError) || $OfficeStore === undefined}
  <LoadingComponent />
{:else if !isLoading && !options.isError}
  <MultiSelect bind:options />
{/if}
