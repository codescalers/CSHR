<script lang="ts">
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import usersDataService from "../../../apis/users/users";
  import { AllUsersStore, UserStore } from "../../../utils/stores";
  import type {
    GeneralUserInterface,
    SelectOptionsComponent,
    SelectOptionType
  } from "../../../utils/types";
  import LoadingComponent from "../../ui/Loading.svelte";
  import MultiSelect from "./MultiSelect.svelte";
  import PeopleSlot from "./UsersSlot.svelte";

  export let isLoading = false;
  export let options: SelectOptionsComponent = {
    isError: false
  };
  export let usersInAdminOffice = false;
  const dispatch = createEventDispatcher();

  let users: GeneralUserInterface[];

  function select(e: any) {
    dispatch("select", {
      selected: e.detail.selected
    });
  }

  function removeAll(e: any) {
    dispatch("removeAllItems", {
      selected: e.detail.selected
    });
  }

  function removeItem(e: any) {
    dispatch("removeItem", {
      selected: e.detail.selected
    });
  }

  onMount(async () => {
    isLoading = true;
    options.optionsList = [];
    $AllUsersStore = users = [];

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
        if (user.id !== $UserStore.id) {
          const value: SelectOptionType = {
            value: user.id,
            label: user.full_name,
            extraData: {
              full_name: user.full_name,
              image: user.image,
              team: user.team
            }
          };

          if (!options.optionsList!.includes(value)) {
            options.optionsList!.push(value);
          }
        }
      });
    } catch (e) {
      options.isError = true;
    }
    isLoading = false;
  });

  $: options, handleMultipleUserSelection()

  /**
   * Ensures proper handling of multiple user selection.
   * If multiple users are selected and the 'multiple' option is not enabled,
   * keeps only the first selected user in the options.
  */
  function handleMultipleUserSelection() {
    // Check if multiple user selection is not allowed and multiple users are selected
    if (!options.multiple && options.selected && options.selected.length > 1) {
      // Keep only the first selected user in the options
      options.selected = [options.selected[0]];
    }
  }
</script>

{#if (isLoading && !options.isError) || $AllUsersStore === undefined}
  <LoadingComponent />
{:else if !isLoading && !options.isError}
  <MultiSelect
    bind:options
    on:select={select}
    on:removeAllItems={removeAll}
    on:removeItem={removeItem}
  >
    <PeopleSlot let:option {option} slot="option" />
  </MultiSelect>
{/if}
