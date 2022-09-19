<script lang="ts">
  import Members from "./Members.svelte";
  import Supervisors from "./Supervisors.svelte";

  import { onMount } from "svelte";
  import { TeamStore } from "../../stores";
  import LoadingComponent from "../loader/LoadingComponent.svelte";
  import ErrorComponent from "../error/ErrorComponent.svelte";
  import teamDataService from "../../services/axios/team/TeamDataService";
  import type { PaginatedInterface, TeamType } from "../../types";

  export let isLoading = false;
  export let isError: boolean | null = null;

  onMount(async () => {
    isLoading = true;
    try {
      if ($TeamStore.results.length === 0) {
        const team:PaginatedInterface<TeamType>  = await teamDataService.get();
        TeamStore.set(team);
        }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

<div class="container">
  {#if isError}
    <ErrorComponent
      errorMessage="please try to reload page and raise an issues"
    />
  {:else if isLoading}
    <LoadingComponent />
  {:else}
    <div class="row">
      <div class="col-12">
        <h4>Supervisors</h4>
      </div>
      <div class="col-12">
        <Supervisors />
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h4>Members</h4>
      </div>
      <div class="col-12">
        <Members />
      </div>
    </div>
  {/if}
</div>
