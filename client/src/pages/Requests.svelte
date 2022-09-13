<script lang="ts">
  import getRequests from "../services/axios/requests/requests";
  import ActionButton from "../components/requests/requestsButtons.svelte"
 

  import type { UserInterface } from "../types";
  export let user: UserInterface;
  import { onMount } from "svelte";


  import Sidebar from "../components/sidebar/Sidebar.svelte";


  let pageCount = 0;
  let pageSize = 3;
  let modalID =6;
  function increment() {
      if (totalRequests - (pageCount * 3) - pageSize  > 0 ){
          pageCount++;
      }
    }
  function decrement() {
      if (pageCount > 0 ){
          pageCount--;
      }
    }
    let requests :any = [];
  let totalRequests = 1;
  onMount(async () => {
    requests = await getRequests();
    totalRequests = requests.length;
  
  });
</script>

<Sidebar bind:user>
  <span slot="page-name">Requests</span>
  <section class=" container-fluid mt-5" slot="content">
    <div class="row">
      <h4 class="child  mx-5">All Requests</h4>
      <table class="table align-middle mb-0 mx-5 w-100">
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
            <th>Desicion</th>
          </tr>
        </thead>
        <tbody>
          {#each requests.slice(pageCount * 3, pageCount * 3 + 3) as request,index (index)}
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
                    <p class="fw-bold mb-1">
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
                  {request.type == "HR letters"
                    ? request.addresses
                    : request.reason}
                </p>
              </td>
              <td>
                <p class="fw-bold mb-1">
                  <span class="text-muted">Start: </span>{request.from_date
                    ? request.from_date
                    : "---"}
                </p>
                <p class="text-muted mb-0">
                  <span class="text-muted">End: </span>{request.end_date
                    ? request.from_date
                    : "---"}
                </p>
              </td>
              <td>
                <div class="container w-100 p-0">
                  <ActionButton {request} {index}/>
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
          >{pageCount + 1} of {Math.ceil(totalRequests / pageSize)}</label
        >
        <button class="pagination-button" on:click={decrement}
          ><i class="icon fa-solid fa-chevron-left" /></button
        >
        <button class="pagination-button" on:click={increment}
          ><i class="icon fa-solid fa-chevron-right" /></button
        >
      </div>
    </div>
    
    <!-- <Modal
      id={modalID + ""}
      isDelete={false}
      isDone={false}
      isFooter={true}
      doneText={"Done"}
      deleteText={"Delete"}
      isClose={false}
    >
    <header slot="header">
      <h6>Vacation Details</h6>
    </header>
    <div slot="body">
      <RequestModal></RequestModal>
      <div>
        
      </div>
    </div> 
  
  </Modal>-->

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
