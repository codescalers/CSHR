<script lang="ts">
  import ProfileImage from '../profile/ProfileImage.svelte';
  import Table from '../table/Table.svelte';

  export let supervisors: any;
  let pageIndex: number = 0;
  let length: number = 10;
  let headers = [
    'Name',
    'Email',
    'Phone',
    'Address',
    'Posation',
  ];
</script>

<Table bind:pageIndex bind:length bind:headers>
  <tbody slot="table-body" >
    {#each supervisors as supervisor}
        <tr class="mt-3">
          <th scope="row">
            <ProfileImage user={supervisor}/>
          </th>
          <td>{supervisor.full_name}</td>
          <td>{supervisor.email}</td>
          <td>{supervisor.mobile_number || '---'}</td>
          <td>{supervisor.address || '---'}</td>
          <td>{supervisor.job_title || '---'}</td>
        </tr>
    {/each}
  </tbody>
</Table>