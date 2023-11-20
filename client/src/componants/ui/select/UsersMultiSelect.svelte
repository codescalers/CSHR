<script lang="ts">
  import usersDataService from "../../../apis/users/users";
  import { onMount } from "svelte";
  import { AllUsersStore, UserStore } from "../../../utils/stores";
  import PeopleSlot from "./UsersSlot.svelte";
  import MultiSelect from "./MultiSelect.svelte";
  import type {
    GeneralUserInterface,
    SelectOptionType,
  } from "../../../utils/types";
  import LoadingComponent from "../../ui/Loading.svelte";
  export let placeholder = `Select Users`;
  export let removeAllTitle = "Remove all users";
  export let isLoading = false;
  export let isError: boolean | null = null;
  export let mylabel = "People";
  export let isTop: boolean;
  export let multiple: boolean = true;
  export let selected: SelectOptionType[] = [];
  export let usersInAdminOffice: boolean = false;

  let options: SelectOptionType[] = [];
  let users: GeneralUserInterface[];

  onMount(async () => {
    isLoading = true;
    try {
      if ($AllUsersStore === undefined || $AllUsersStore.length === 0) {
        if (usersInAdminOffice) {
          users = await usersDataService.getOfficeUsers();
        } else {
          users = await usersDataService.getAll();
        }
        if ($AllUsersStore === undefined) {
          $AllUsersStore = users;
        } else {
          AllUsersStore.set(users);
        }
      }
      $AllUsersStore.forEach((user) => {
        if (user.id !== $UserStore.id)
          options.push({
            value: user.id,
            label: user.full_name,
            extraData: {
              full_name: user.full_name,
              image: user.image,
              team: user.team,
            },
          });
      });
    } catch (e) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if (isLoading && !isError) || $AllUsersStore === undefined}
  <LoadingComponent />
{:else if !isLoading && !isError}
  <MultiSelect
    bind:options
    bind:selected
    label={mylabel}
    {placeholder}
    {removeAllTitle}
    isLabel={false}
    {isTop}
    {multiple}
  >
    <PeopleSlot let:option {option} slot="option" />
  </MultiSelect>
{/if}
