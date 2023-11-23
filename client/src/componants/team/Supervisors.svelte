<script lang="ts">
  import Table from "../../componants/table/Table.svelte";
  import ProfileImage from "../profile/ProfileImage.svelte";
  import Alert from "../ui/Alert.svelte";

  export let supervisors: any;

  let headers = ["Name", "Email", "Phone", "Position", "Department"];
</script>

{#if supervisors.length}
  <div class="mt-5">
    <h4 style="font-weight: 800;">Reporting to</h4>
    <Table bind:headers>
      <tbody slot="table-body">
        {#each supervisors as supervisor}
          <tr class="mt-3 hover-tr">
            <th scope="row">
              <ProfileImage user={supervisor} />
            </th>
            <td class="text-center td-col">{supervisor.full_name}</td>
            <td class="text-center td-col">{supervisor.email}</td>
            <td class="text-center td-col">{supervisor.mobile_number || "---"}</td>
            <td class="text-center td-col">{supervisor.job_title || "---"}</td>
            <td class="text-center td-col">{supervisor.team || "---"}</td>
          </tr>
        {/each}
      </tbody>
    </Table>
  </div>
{:else}
  <Alert
    className="primary text-center mb-5 mt-3"
    message="There are no members in the `reporting to` section, not available."
  />
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
