<script lang="ts">
  import ProfileImage from "../profile/ProfileImage.svelte";
  import Table from "../table/Table.svelte";
  // import { SupervisorStore } from '../../stores';

  export let members: any;

  let pageIndex: number = 0;
  let length: number = 10;
  let headers = [
    "Name",
    "Email",
    "Phone",
    // 'Address',
    "Position",
  ];
</script>

<Table bind:pageIndex bind:length bind:headers>
  <tbody slot="table-body">
    {#each members as member}
      <tr>
        <th scope="row">
          <ProfileImage user={member} />
        </th>
        <td>{member.full_name}</td>
        <td>{member.email}</td>
        <td>{member.mobile_number || "---"}</td>
        <!-- <td>{member.address || '---'}</td> -->
        <td>{member.job_title || "---"}</td>
      </tr>
    {/each}
  </tbody>
</Table>
