<script lang="ts">
  import type { UserInterface } from "../types";
  export let user: UserInterface;
  import Sidebar from "../components/sidebar/Sidebar.svelte";
  
  function approve_btn(request) {
    request.status = "Approved"
    console.log(request);
  }
  function reject_btn(request) {
    request.status = "Rejected"
    console.log(request);
  }
  let pageCount = 0;
  let pageSize = 3;
  let requests = [
    {
      name: "Michael",
      period: 2,
      role: "Engineering Manager",
      date: "28 May, 2000",
      time: "6.33",
      status: "Approved",
    },
    {
      name: "Marwan",
      period: 3,
      role: "SRE",
      date: "28 May, 2000",
      time: "6.33",
      status: "primary",
    },
    {
      name: "Joel",
      period: 3,
      role: "QA Engineer",
      date: "28 May, 2000",
      time: "6.33",
      status: "primary",
    },
    {
      name: "Marc",
      period: 2,
      role: "Software Engineer",
      date: "28 May, 2000",
      time: "6.30",
      status: "Rejected",
    },
    {
      name: "Joe",
      period: 3,
      role: "Software Engineer",
      date: "28 May, 2000",
      time: "6.30",
      status: "Pending",
    },
    {
      name: "Test",
      period: 3,
      role: "Software Engineer",
      date: "28 May, 2000",
      time: "6.30",
      status: "Approved",
    },
  ];
  function increment() {
    if (totalRequests - pageCount * 3 - pageSize > 0) {
      pageCount++;
    }
  }
  function decrement() {
    if (pageCount > 0) {
      pageCount--;
    }
  }
  let totalRequests = requests.length;
</script>

<Sidebar bind:user>
  <span slot="page-name">Requests</span>
  <section class=" container-fluid mt-5" slot="content">
    <div class="row">
      <h4 class="child  mx-5">All Requests</h4>
      <table class="table align-middle mb-0 mx-5">
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
            <th>Date</th>
            <th>Desicion</th>
          </tr>
        </thead>
        <tbody>
          {#each requests.slice(pageCount * 3, pageCount * 3 + 3) as request}
            <tr>
              <td>
                <div class="d-flex  align-items-center">
                  <img
                    src="https://mdbootstrap.com/img/new/avatars/8.jpg"
                    alt=""
                    style="width: 45px; height: 45px"
                    class="rounded-circle"
                  />
                  <div class="ms-3">
                    <p class="fw-bold mb-1">{request.name}</p>
                    <p class="text-muted mb-0">
                      Updated {request.period} days ago
                    </p>
                  </div>
                </div>
              </td>
              <td>
                <p class="fw-bold mb-1">{request.role}</p>
                <p class="text-muted mb-0">{request.date}</p>
              </td>
              <td>
                <p class="fw-bold mb-1">{request.date}</p>
                <p class="text-muted mb-0">{request.time}</p>
              </td>
              <td >
                <div class="container p-0">
                  <div class="column">
                    {#if request.status == "Rejected"}
                    <div class="row row-cols-2 align-items-center">
                      <div class="col-4">
                        <button
                          type="button"
                          class="btn btn-danger btn-sm w-100 "
                          disabled>Rejected</button
                        >
              
                      </div>
                      <div class="col-2 pl-0">
                        <button type="button" class="btn p-0"
                          ><i class="bi bi-three-dots-vertical" /></button
                        >
                      </div>
                    </div>
                    {:else if request.status == "Approved"}
                    <div class="row row-cols-2 align-items-center">
                      <div class="col-4">
                        <button
                          type="button"
                          class="btn btn-success btn-sm w-100 "
                          disabled>Approved</button
                        >
              
                      </div>
                      <div class="col-2 pl-0">
                        <button type="button" class="btn p-0"
                          ><i class="bi bi-three-dots-vertical" /></button
                        >
                      </div>
                    </div>
                    {:else}
                    <div class="row row-cols-2 align-items-center">
                      <div class="col-4">
                        <button
                          type="button"
                          on:click={approve_btn(request)}
                          class="btn btn-success btn-sm w-100 mb-1"
                          >Approve</button
                        >
                        <button
                            type="button"
                            on:click={reject_btn(request)}
                            class="btn btn-danger btn-sm w-100"
                            >Reject</button
                          >
                      </div>
                      <div class="col-2 pl-0">
                        <button type="button" class="btn p-0"
                          ><i class="bi bi-three-dots-vertical" /></button
                        >
                      </div>
                    </div>
                          
                       
                      
                    {/if}
                  </div>
                </div>
              </td>
              
            </tr>
          {/each}
        </tbody>
      </table> 
    </div>
    <div class="row justify-content-end mt-3">
      <div class="col-2 mr-5">
        
          <label class="text-muted mb-0 ">Rows per page:</label>
          <label class="text-muted mb-0"
            >{pageCount + 1} of {totalRequests / pageSize}</label
          >
          <button class="pagination-button" on:click={decrement}
            ><i class="icon fa-solid fa-chevron-left" /></button
          >
          <button class="pagination-button" on:click={increment}
            ><i class="icon fa-solid fa-chevron-right" /></button
          >
               
       
      </div>
    </div>
  </section>
</Sidebar>

<style>
  .page-body {
    position: absolute;
    height: 942px;
    left: 285px;
    right: 33px;
    top: 128px;
  }



  .sort {
    display: inline-block;
    padding-left: 35cm;
  }
  label {
    font-weight: 300;
    font-size: larger;
    padding-right: 0.5cm;
  }
  section {
    overflow: hidden;
  }
  .icon {
    padding-right: 0.3cm;
  }
  .pagination-button {
    background: unset !important;
    border: unset !important;
    outline: unset !important;
  }
</style>
