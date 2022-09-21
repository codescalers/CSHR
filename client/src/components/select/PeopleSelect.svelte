<script lang="ts">
  import type { UserInterface } from '../../types'
  import usersDataService from '../../services/axios/users/UsersDataService'
  import { onMount } from 'svelte'
  import { AllUsersStore, UserStore } from '../../stores'
  import PeopleSlot from './PeopleSlot.svelte'
  import MultiSelect from 'svelte-multiselect'
  export let selected: number[] = []
  export let placeholder = `Select Users`
  export let removeAllTitle = 'Remove all users'
  export let isLoading = false
  export let isError: boolean | null = null
  // user ids
  let options: string[] = []

  onMount(async () => {
    isLoading = true
    try {
      if ($AllUsersStore === undefined || $AllUsersStore.length === 0) {
        const users = await usersDataService.getAll()
        if ($AllUsersStore === undefined) {
          $AllUsersStore = users
        } else {
          AllUsersStore.set(users)
        }
      }
      $AllUsersStore.forEach((user: UserInterface) => {
        if (user.id !== $UserStore.id) options.push(user.id + '')
      })
    } catch (e) {
      isError = true
    }
    isLoading = false
  })
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
    id="people-select"
    name="people-select"
  >
    <PeopleSlot let:idx {idx} let:option {option} slot="option" />
    <PeopleSlot let:idx {idx} let:option {option} slot="selected" />
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
  .loader {
    width: 40px;
    height: 40px;
    text-align: center;
    margin: 0 auto;
  }
</style>
