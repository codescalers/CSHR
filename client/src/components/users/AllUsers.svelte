<script lang="ts">
  import { onMount } from "svelte";
  import type { UserInterface } from "../../types";
  import User from "./User.svelte";
  import { AllUsersStore } from "../../stores";
  import userDataService from "../../services/axios/users/UserDataService";
  import LoadingComponent from "../loader/LoadingComponent.svelte";
  import ErrorComponent from "../error/ErrorComponent.svelte";

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
</script>

<div class="container">
  {#if isError}
    <ErrorComponent />
  {:else if isLoading}
    <LoadingComponent />
  {:else}
    <div class="row justify-content-between">
      {#each $AllUsersStore as user (user.id)}
        <div class="col-12 col-md-6 col-lg-4 my-4">
          <User bind:user />
        </div>
      {/each}
    </div>
  {/if}
</div>
