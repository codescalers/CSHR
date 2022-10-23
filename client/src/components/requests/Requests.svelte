<script lang="ts">
  import Requests from '../../services/axios/requests/requests';
  import ActionButton from './requestsButtons.svelte';
  import { onMount } from 'svelte';
  import ProfileImage from '../profile/ProfileImage.svelte';
  import { UserStore } from "../../stores"
  import { Link } from 'svelte-navigator';


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
{#if requests && requests.length > 0}
  <div class="row ">
    <h4 class="child  mx-3">All Requests</h4>
    <table class="table align-middle mb-0 mx-3 w-100" style="overflow: hidden;">
      <colgroup>
        <col span="1" style="width: 25%;" />
        <col span="1" style="width: 35%;" />
        <col span="1" style="width: 15%;" />
        <col span="1" style="width: 15%;" />
        <col span="1" style="width: 15%; " />
      </colgroup>
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th>Type</th>
          <th>Date</th>
          <th class="d-flex justify-content-center align-items-center">Actions</th>
          <th>Status</th>
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
                {#if request.type == 'HR letters'}
                  {request.addresses}
                {:else if request.type == "Official documents"}
                  {request.document}
                {:else}
                  {request.reason}
                {/if}
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
              <div class="d-flex justify-content-center align-items-center">
                {#if $UserStore.user_type == "Admin" || $UserStore.user_type == "Supervisor"}
                    <ActionButton {request} on:message={handleActions}/>
                {/if}
                <Link class="text-dark" to="/{request.type.toLowerCase().replace(" ", "_")}/{request.id}">
                  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
                    <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
                  </svg>
                </Link>
              </div>
            </td>
            <td style="width:10%">
              <strong>{request.status}</strong>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else}
  <div class="d-flex height-100 justify-content-center align-items-center" style="flex-direction: column;">
    <div class="text-center">
      <h4 class="mb-4">
        There are no requests to view.
      </h4>
    </div>
  <br/>
    <svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" fill="currentColor" class="bi bi-file-text" viewBox="0 0 16 16">
      <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z"/>
      <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
    </svg>
  </div>
{/if}
<style>
  .float-right-span{
    float: right;
    margin-right: 15px;
  }
</style>