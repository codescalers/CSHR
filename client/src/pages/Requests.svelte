<script lang="ts">
  import getRequests from "../services/axios/requests/requests";
  import Modal from "../components/modal/Modal.svelte";
  import ModalButton from "../components/modal/ModalButton.svelte";
  import updateVacations from "../services/axios/requests/vacations";
  import updateLetters from "../services/axios/requests/hr_letters";
  import updateCompensation from "../services/axios/requests/compensation"
  import type { UserInterface } from "../types";
  export let user: UserInterface;
  import { onMount } from "svelte";


  import Sidebar from "../components/sidebar/Sidebar.svelte";

  let requests :any = [];
  async function  approve_btn (element: any,index:number) { 
    document.body.style.cursor ='wait';
    if (element.type == "Vacation"){
      console.log("before")
     if(await updateVacations(element.id, { status: "approved"}) ){
      console.log("after")
      requests[index].status = "approved";
     }
      
    }else if (element.type == "HR letters"){
      
      await updateLetters(element.id, { status: "approved"});
    }else if (element.type == "Compensation"){
      let data:JSON= JSON.parse('{"status":"approved"}')
      await updateCompensation(id,data);
    }
    requests = await getRequests();
    document.body.style.cursor ='defult';
    console.log(element);
  }
  async function reject_btn(type,id) {
    document.body.style.cursor='wait';
    if (type == "Vacation"){
    let data:JSON= JSON.parse('{"status":"rejected"}')
     if (await updateVacations(id,data)){

     }
      
    }else if (type == "HR letters"){
      let data:JSON= JSON.parse('{"status":"rejected"}')
      await updateLetters(id,data);
    }else if (type == "Compensation"){
      let data:JSON= JSON.parse('{"status":"rejected"}')
      await updateCompensation(id,data);
    }
    requests = await getRequests();
    document.body.style.cursor='default';
    console.log(type,id);
  }
  
  let pageCount = 0;
  let pageSize = 3;
  let modalID =3;
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
  
  let totalRequests = 1;
  onMount(async () => {
    requests = await getRequests();
    totalRequests = requests.length;
    console.log(requests)
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
                  <div class="column">
                    {#if request.status == "Rejected" || request.status == "rejected"}
                      <div class="row align-items-center">
                        <div class="col">
                          <button
                            type="button"
                            class="btn btn-danger btn-border btn-sm w-100 "
                            disabled>Rejected</button
                          >
                        </div>
                        <div class="col pl-0">
                          <button type="button" class=" btn btn-view p-0"
                          data-bs-toggle={"modal"}
                          data-bs-target={"#modal" + modalID}
                            ><i class="bi bi-eye" /></button
                          >
                        </div>
                      </div>
                    {:else if request.status == "Approved" || request.status == "approved"}
                      <div
                        class="row  align-items-center justify-content-start "
                      >
                        <div class="col">
                          <button
                            type="button"
                            class="btn btn-success btn-border btn-sm w-100 "
                            disabled>Approved</button
                          >
                        </div>
                        <div class="col pl-0">
                          <button
                            type="button"
                            class="btn  btn-view p-0"
                            data-bs-toggle={"modal"}
                            data-bs-target={"#modal" + modalID}
                            ><i class="bi bi-eye" /></button
                          >
                        </div>
                      </div>
                    {:else}
                      <div class="row align-items-center">
                        <div class="col">
                          <button
                            type="button"
                            on:click={()=>approve_btn(request,index)}
                            class="btn btn-success btn-border btn-sm w-100 mb-1"
                            >Approve</button
                          >
                          <button
                            type="button"
                            
                            on:click={()=>reject_btn(request.type, request.id)}
                            class="btn btn-danger btn-border btn-sm w-100">Reject</button
                          >
                        </div>
                        <div class="col pl-0">
                          <button type="button" class="btn btn-view p-0"
                          data-bs-toggle={"modal"}
                          data-bs-target={"#modal" + modalID}
                            ><i class="bi bi-eye" /></button
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
   
    <Modal
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
      <div>
        
      </div>
    </div>
  
  </Modal>

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
  .btn-view {
    border:none !important;
  }
  .btn-border{
    border-radius: 35px;
  }
  .btn-success{
    background:#29CC97;
    border-color: #29CC97;
  }
  .btn-danger{
    background:#F12B2C;
    border-color: #F12B2C;
  }
  
</style>
