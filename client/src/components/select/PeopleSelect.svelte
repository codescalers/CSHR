<script lang="ts">
  import type { UserInterface } from "../../types";
  import userDataService from "../../services/axios/users/UserDataService";
  import { onMount } from "svelte";
  import { AllUsersStore } from "../../stores";
  import PeopleSlot from "./PeopleSlot.svelte";
  import MultiSelect from "svelte-multiselect";
  export let selected: number[] = [];
  export let placeholder = `Select Users`;
  export let removeAllTitle = "Remove all users";
  export let isLoading = false;
  export let isError: boolean | null = null;
  let options: number[] = [];

  onMount(async () => {
    isLoading = true;
    try {
      if ($AllUsersStore.length === 0) {
        const users = (await userDataService.getAll()).data;
        AllUsersStore.set(users);
        options = users.map((user: UserInterface) => user.id);
      }
    } catch (e) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if isLoading && !isError}
  loading...
{/if}
{#if isError}
  error loading users
{/if}
{#if !isLoading && !isError}
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
  >
    <PeopleSlot let:option {option} slot="option" />
    <PeopleSlot let:option {option} slot="selected" />
  </MultiSelect>
{/if}

<!--   https://www.npmjs.com/package/svelte-multiselect -->

<!-- https://svelte-multiselect.netlify.app/#with-css-variables -->
<style>
  :global(.li-option:hover) {
    background-color: var(--secondary-color);
    color: var(--primary-color);
  }
  :global(.li-selected) {
    background-color: var(--primary-color) !important;
    color: var(--secondary-color) !important;
    width: fit-content !important;
  }
  :global(.li-selected img) {
    display: none;
  }
  :global(.select-box) {
    width: 100%;
    height: 100%;
  }
</style>
