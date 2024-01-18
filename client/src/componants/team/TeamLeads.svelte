<script lang="ts">
  import Table from "../table/Table.svelte";
  import ProfileImage from "../profile/ProfileImage.svelte";

  export let teamLeads: any;

  let headers = ["Name", "Email", "Phone", "Position", "Department"];
</script>

{#if teamLeads.length}
  <div class="mt-5">
    <h4 style="font-weight: 800;">Reporting to</h4>
    <Table bind:headers>
      <tbody slot="table-body">
        {#each teamLeads as teamLead}
          <tr class="mt-3 hover-tr">
            <th scope="row">
              <ProfileImage user={teamLead} />
            </th>
            <td class="text-center td-col">{teamLead.full_name}</td>
            <td class="text-center td-col">{teamLead.email}</td>
            <td class="text-center td-col"
              >{teamLead.mobile_number || "---"}</td
            >
            <td class="text-center td-col">{teamLead.job_title || "---"}</td>
            <td class="text-center td-col">{teamLead.team || "---"}</td>
          </tr>
        {/each}
      </tbody>
    </Table>
  </div>
{/if}

<style scoped>
  .td-col {
    justify-content: center;
    align-items: center;
    height: 100% auto;
    height: auto;
    padding: 16px;
    font-weight: 600;
  }
</style>
