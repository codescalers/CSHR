<script lang="ts">
  import { onMount } from "svelte";
  import type { UserInterface } from "../../utils/types";
  import User from "./User.svelte";
  import { AllUsersStore } from "../../utils/stores";
  import usersDataService from "../../apis/users/users";
  import Loading from "../ui/Loading.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  let users: UserInterface[];
  onMount(async () => {
    isLoading = true;
    try {
      users = await usersDataService.getAll();
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if isLoading}
  <div class="height-100 d-flex justify-content-center align-items-center">
    <Loading className={"loader"} />
  </div>
{:else if !isLoading && !isError && users}
  <div class="container">
    <div class="d-flex flex-column justify-content-between">
      <div>
        <div class="row justify-content-between">
          {#each users as user}
            <div class="col-12 col-md-6 col-lg-4 my-4">
              <User bind:user />
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}
