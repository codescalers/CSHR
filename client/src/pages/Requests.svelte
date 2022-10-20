<script lang="ts">
  import Requests from '../services/axios/requests/requests';
  import ActionButton from '../components/requests/requestsButtons.svelte';
  import { Link } from 'svelte-navigator';
  import { onMount } from 'svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import ProfileImage from '../components/profile/ProfileImage.svelte';

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
  let totalRequests = 1;

  onMount(async () => {
    requests = await Requests.getRequests();
    totalRequests = requests.length;
  });
</script>

<Sidebar>
  <section slot="content">
    <div class="row">
      <h4 class="child  mx-3">All Requests</h4>
      <table class="table align-middle mb-0 mx-3 w-100">
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
            <th style="width:10%">Action</th>
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
              <td>
                <Link class="text-dark" to="/{request.type.toLowerCase()}s/{request.id}">
                  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
                    <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
                  </svg>
                </Link>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>
</Sidebar>

<style>
  label {
    font-weight: 300;
    font-size: 16px;
    padding-right: 0.3cm;
  }
  section {
    overflow: hidden;
  }
  .icon {
    font-size: 1rem;
  }
  .pagination-button {
    background: unset !important;
    border: unset !important;
    outline: unset !important;
  }
  .float-right-span{
    float: right;
    margin-right: 15px;
  }
</style>