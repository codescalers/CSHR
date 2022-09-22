<script lang="ts">
  import Members from './Members.svelte';
  import Supervisors from './Supervisors.svelte';

  import { onMount } from 'svelte';
  import { TeamStore } from '../../stores';
  import teamDataService from '../../services/axios/team/TeamDataService';
  import type { PaginatedInterface, TeamType } from '../../types';

  export let isLoading = false;
  export let isError: boolean | null = null;

  onMount(async () => {
    isLoading = true;
    try {
      if ($TeamStore === undefined || $TeamStore.results.length === 0) {
        const team: PaginatedInterface<TeamType> = await teamDataService.get();
        if ($TeamStore === undefined) {
          $TeamStore = team;
        } else {
          TeamStore.set(team);
        }
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

<div class="container">
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
</div>
