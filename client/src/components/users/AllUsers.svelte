<script lang="ts">
  import { onMount } from "svelte";
  import type { UserInterface } from "../../types";
  import User from "./User.svelte";
  import { AllUsersStore } from "../../stores";
  import userDataService from "../../services/axios/users/UserDataService";
  import LoadingComponent from "../loader/LoadingComponent.svelte";
  import ErrorComponent from "../error/ErrorComponent.svelte";
  import Pagination from "../pagination/Pagination.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  onMount(async () => {
    isLoading = true;
    try {
      if ($AllUsersStore.length === 0) {
        const users: UserInterface[] = (await userDataService.getAll()).data;
        AllUsersStore.set(users);
      }
    } catch (e) {
      isError = true;
    }
    isLoading = false;
  });

  let value = 1;
  let users: UserInterface[] = [];

  $: users = $AllUsersStore.filter(
    (_, index) => index < value * 10 && index >= (value - 1) * 10
  );
  $: length = Math.ceil($AllUsersStore.length / parseFloat(20 + ""));

</script>

<div class="container">
  {#if isError}
    <ErrorComponent errorMessage="please try to reload page and raise an issues" />
  {:else if isLoading}
    <LoadingComponent />
  {:else}
    <div class="input-group rounded d-flex flex-row my-2">
      <input
        type="search"
        class="form-control rounded"
        placeholder="Search"
        aria-label="Search"
        aria-describedby="search-addon"
      />
      <span class="input-group-text border-0" id="search-addon">
        <i class="fas fa-search" />
      </span>
    </div>
    <div class="row justify-content-between">
      {#each users as user (user.id)}
        <div class="col-12 col-md-6 col-lg-4 my-4">
          <User bind:user />
        </div>
      {/each}
    </div>
    <Pagination bind:length bind:value />
  {/if}
</div>
