<script lang="ts">
  import { onMount } from "svelte";
  import type { UserInterface } from "../../utils/types";
  import User from "./User.svelte";
  import { AllUsersStore } from "../../utils/stores";
  import usersDataService from "../../apis/users/users";

  export let isLoading = false;
  export let isError: boolean | null = null;

  onMount(async () => {
    isLoading = true;
    try {
      const users: UserInterface[] = await usersDataService.getAll();
      $AllUsersStore = users;
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if !isLoading && !isError && $AllUsersStore}
  <div class="container">
    <div class="d-flex flex-column justify-content-between">
      <div>
        <div class="row justify-content-between">
          {#each $AllUsersStore as user}
            <div class="col-12 col-md-6 col-lg-4 my-4">
              <User bind:user />
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}
