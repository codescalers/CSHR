<script lang="ts">
  import officeDataService from "../../services/axios/offices/OfficeDataService";
  import type { OfficeInterface } from "../../types";
  import { onMount } from "svelte";
  import { OfficeStore } from "../../stores";
  import MultiSelect from "svelte-multiselect";
  export let selected: number[] = [];
  export let placeholder = `Select Users`;
  export let removeAllTitle = "Remove all users";
  export let isLoading = false;
  export let isError: boolean | null = null;
  let options: string[] = [];

  onMount(async () => {
    isLoading = true;
    try {
      if ($OfficeStore.length === 0) {
        const offices = (await officeDataService.getAll()).data;
        OfficeStore.set(offices);
        options = offices.map((office: OfficeInterface) => office.id + "");
      }
    } catch (e) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if isError}
  <img
    class="loader"
    src="https://icon-library.com/images/not-found-icon/not-found-icon-20.jpg"
    alt="Not Found"
  />
{:else if isLoading && !isError}
  <img
    class="loader"
    src="https://c.tenor.com/On7kvXhzml4AAAAi/loading-gif.gif"
    alt="Loading..."
  />
{:else if !isLoading && !isError}
  <MultiSelect
    bind:options
    bind:selected
    {placeholder}
    outerDivClass=""
    ulSelectedClass="bar"
    ulOptionsClass="baz"
    liOptionClass="li-option"
    inputClass="select-box"
    liSelectedClass="li-selected"
    liActiveOptionClass="mom"
    --sms-border-radius="0.3rem"
    --sms-options-bg="white"
    --sms-min-height="2.25rem"
    --sms-min-width="4rem"
    --sms-bg="var(--secondary-color)"
    {removeAllTitle}
  />
{/if}

<style>
  .loader {
    width: 40px;
    height: 40px;
    text-align: center;
    margin: 0 auto;
  }
</style>
