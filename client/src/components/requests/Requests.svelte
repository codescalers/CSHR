<script lang="ts">
  import Requests from '../../services/axios/requests/requests';
  import ActionButton from './requestsButtons.svelte';
  import { onMount } from 'svelte';
  import ProfileImage from '../profile/ProfileImage.svelte';

  const handleActions = (event: { detail: { text: any; }; }) => {
    const sRequest = event.detail.text.request
    requests.forEach((request: any) => {
      if(request.id === sRequest.id){
        const index = requests.indexOf(request);
        requests.splice(index, 1);
        requests = requests;
      }
    });
  }

  let requests: any = [];
  onMount(async () => {
    requests = await Requests.getRequests();
  });

</script>

<div class="row">
  <h4 class="child  mx-3">All Requests</h4>
  <table class="table align-middle mb-0 mx-3 w-100" style="overflow: hidden;">
    <colgroup>
      <col span="1" style="width: 25%;" />
      <col span="1" style="width: 35%;" />
      <col span="1" style="width: 15%;" />
      <col span="1" style="width: 15%; " />
    </colgroup>
    <thead>
      <tr>
        <th scope="col">Name</th>
        <th>Type</th>
        <th>Date</th>
        <th style="width:10%">Desicion</th>
      </tr>
    </thead>
    <tbody>
      {#each requests as request}
        <tr>
          <td>
            <div class="d-flex  align-items-center">
              <ProfileImage user={request.applying_user}/>
              <div class="mx-2">
                <p class="fw-bold mb-0">
                  {request.applying_user.full_name}
                </p>
                <p class="text-muted mb-0">
                  {request.applying_user.email}
                </p>
              </div>
            </div>
          </td>
          <td>
            <p class="fw-bold mb-1">{request.type}</p>
            <p class="text-muted mb-0">
              {request.type == 'HR letters'
                ? request.addresses
                : request.reason}
            </p>
          </td>
          <td>
            <p class="fw-bold mb-1">
              <span class="text-muted">
                Start
              </span>
              <span class="float-right-span">
                {request.from_date ? request.from_date : '---'}
              </span>
            </p>
            <p class="text-muted mb-0">
              <span class="text-muted">
                End
              </span>
              <span class="text-muted float-right-span">
                {request.end_date ? request.end_date : '---'}
              </span>
            </p>
          </td>
          <td style="width:10%">
              <ActionButton {request} on:message={handleActions}/>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  .float-right-span{
    float: right;
    margin-right: 15px;
  }
</style>