<script lang="ts">
  import { onMount } from "svelte";

  import teamDataService from "../../apis/team/TeamDataService";
  import type { TeamLeadType, TeamType } from "../../utils/types";
  import Loading from "../ui/Loading.svelte";
  import Members from "./Members.svelte";
  import TeamLeads from "./TeamLeads.svelte";

  export let isLoading = false;
  export let isError: boolean | null = null;

  let members: TeamType;
  let teamLeads: TeamLeadType;

  onMount(async () => {
    isLoading = true;
    try {
      const team = await teamDataService.getTeams();
      const teamLead = await teamDataService.getTeamLead();
      members = team.data.results;
      teamLeads = teamLead.data.results;
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
  {:else if teamLeads && members}
    <div class="row">
      <TeamLeads {teamLeads} />
      <Members {members} />
    </div>
  {/if}
</div>
