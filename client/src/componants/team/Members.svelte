<script lang="ts">
  import ProfileImage from "../profile/ProfileImage.svelte";
  import Table from "../table/Table.svelte";
  import Alert from "../ui/Alert.svelte";

  export let members: any;

  let headers = ["Name", "Email", "Phone", "Position", "Department"];
</script>

{#if members.length}
  <div class="mt-5">
    <h4 style="font-weight: 800;">Team members</h4>
    <Table bind:headers>
      <tbody slot="table-body">
        {#each members as member}
          <tr>
            <th scope="row">
              <ProfileImage user={member} />
            </th>
            <td class="text-center td-col">{member.full_name}</td>
            <td class="text-center td-col">{member.email}</td>
            <td class="text-center td-col">{member.mobile_number || "---"}</td>
            <td class="text-center td-col">{member.job_title || "---"}</td>
            <td class="text-center td-col">{member.team || "---"}</td>
          </tr>
        {/each}
      </tbody>
    </Table>
  </div>
{:else}
  <Alert
    className="primary text-center mb-5 mt-3"
    message="There are no members in the `Team members` section, not available."
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
