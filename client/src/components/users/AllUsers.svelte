<script lang="ts">
  import { onMount } from "svelte";
  import type { UserInterface } from "../../types";
  import User from "./User.svelte";
  import { AllUsersStore } from "../../stores";
  import userDataService from "../../services/axios/users/UserDataService";

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

  <div class="row justify-content-between">
    {#each $AllUsersStore as user (user.id)}
    <div class="col-sm-5 col-lg-3 my-4">
        <User bind:user />
      </div>
      {/each}
  </div>
</div>
