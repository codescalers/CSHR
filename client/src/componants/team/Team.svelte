<script lang="ts">
  import { onMount } from "svelte";

  import teamDataService from "../../apis/team/TeamDataService";
  import type { SupervisorType, TeamType } from "../../utils/types";
  import Loading from "../ui/Loading.svelte";
  import Members from "./Members.svelte";
  import Supervisors from "./Supervisors.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  let members: TeamType;
  let supervisors: SupervisorType;

  onMount(async () => {
    isLoading = true;
    try {
      const team = await teamDataService.getTeams();
      const supervisor = await teamDataService.getSupervisor();
      members = team.data.results;
      supervisors = supervisor.data.results;
    } catch (error) {
      isError = true;
    } finally {
      isLoading = false;
    }
  });
</script>

<!-- svelte-ignore missing-declaration -->

<div class="container">
  {#if isLoading}
    <div class="height-100 d-flex justify-content-center align-items-center">
      <Loading className={"loader"} />
    </div>
  {:else if supervisors && members}
    <div class="row">
      <Supervisors {supervisors} />
      <Members {members} />
    </div>
  {/if}
</div>
