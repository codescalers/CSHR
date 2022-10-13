<script lang="ts">
  import Members from './Members.svelte';
  import Supervisors from './Supervisors.svelte';

  import { onMount } from 'svelte';
  import { TeamStore, SupervisorStore } from '../../stores';
  import teamDataService from '../../services/axios/team/TeamDataService';
  import type { PaginatedInterface, SupervisorType, TeamType } from '../../types';

  export let isLoading = false;
  export let isError: boolean | null = null;

  let members: any;
  let supervisors: any;


  onMount(async () => {
    isLoading = true;
    try {
      if ($TeamStore === undefined || $TeamStore.results.length === 0) {
        const team: PaginatedInterface<TeamType> = await teamDataService.getTeams();
        const supervisor: PaginatedInterface<SupervisorType> = await teamDataService.getSupervisor();
        members = team
        supervisors = supervisor
        if ($TeamStore === undefined) {
          $TeamStore = team;
          $SupervisorStore = supervisor;
        } else {
          TeamStore.set(team);
          SupervisorStore.set(supervisor);
        }
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>
<!-- svelte-ignore missing-declaration -->

{#if isLoading}
Loading....
{:else if supervisors && members}
  <div class="container">
    <div class="row">
      <div class="col-12">
          <h4>Supervisors</h4>
        </div>
          <div class="col-12">
            <Supervisors supervisors={supervisors.results} />
          </div>
      </div>
    <div class="row">
      <div class="col-12">
        <h4>Members</h4>
      </div>
        <div class="col-12">
          <Members members={members.results}/>
        </div>
    </div>
  </div>
{/if}
