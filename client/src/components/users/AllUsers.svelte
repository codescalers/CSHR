<script lang="ts">
  import { onMount } from 'svelte';
  import type { UserInterface } from '../../types';
  import User from './User.svelte';
  import { AllUsersStore } from '../../stores';
  import usersDataService from '../../services/axios/users/UsersDataService';

  import Pagination from '../pagination/Pagination.svelte';

  export let isLoading = false;
  export let isError: boolean | null = null;

  onMount(async () => {
    isLoading = true;
    try {
      if ($AllUsersStore === undefined || $AllUsersStore.length === 0) {
        const users: UserInterface[] = await usersDataService.getAll();
        if ($AllUsersStore === undefined) {
          $AllUsersStore = users;
        } else {
          AllUsersStore.set(users);
        }
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });

  let pageValue = 1;
  let users: UserInterface[] = [];

  $: if ($AllUsersStore !== undefined) {
    users = $AllUsersStore.filter(
      (_: any, index: number) =>
        index < pageValue * parseFloat(process.env.PAGE_SIZE + '') &&
        index >= (pageValue - 1) * parseFloat(process.env.PAGE_SIZE + '')
    );
  }

  let length =
    $AllUsersStore !== undefined
      ? Math.ceil(
          $AllUsersStore.length / parseFloat(process.env.PAGE_SIZE + '')
        )
      : 0;
</script>

{#if !isLoading && !isError && users}
  <div class="container">
    <div class="d-flex flex-column justify-content-between">
      <div>
        <div class="row justify-content-between">
          {#each users as user (user.id)}
            <div class="col-12 col-md-6 col-lg-4 my-4">
              <User bind:user />
            </div>
          {/each}
        </div>
      </div>
      <Pagination bind:length bind:value={pageValue} />
    </div>
  </div>
{/if}
