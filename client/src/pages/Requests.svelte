<script lang="ts">
 
    import { Filter, Bank, CloudMoon } from "svelte-bootstrap-icons";
    import type { UserInterface } from "../types";
    export let user: UserInterface;
    import Sidebar from "../components/sidebar/Sidebar.svelte";
   
    let pageCount = 0;
    let pageSize = 3;    
    let requests = [
    {
        "name" : "Michael",
        "period": 2,
        "role": "Engineering Manager",
        "date": "28 May, 2000",
        "time": "6.33",
        "status":"Approved",
    },
    {
        "name" : "Marwan",
        "period": 3,
        "role": "SRE",
        "date": "28 May, 2000",
        "time": "6.33",
        "status":"primary",
    },
    {
        "name" : "Joel",
        "period": 3,
        "role": "QA Engineer",
        "date": "28 May, 2000",
        "time": "6.33",
        "status":"primary",
    },{
        "name" : "Marc",
        "period": 2,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "status":"Rejected",
    },
    {
        "name" : "Joe",
        "period": 3,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "status":"Pending",
    },
    {
        "name" : "Test",
        "period": 3,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "status":"Approved",
    },

    ];
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
    let totalRequests= requests.length;
</script>
  
  <Sidebar bind:user={user}>
    <span slot="page-name">Requests</span>
    <section class=" fluid-container mt-5" slot="content">

      <div>
        <div class="d-flex justify-content-between"> 
            <div>
                <h4 class="child mx-5">All Requests</h4>
            </div>
            <div class="me-5">
                <button class="btn "><i style="font-size:25px" class="bi bi-sort-up "></i></button>
                <button class="btn "><i   style="font-size:25px" class="bi bi-funnel-fill "></i></button>

            </div>
        </div>
          
          
        <table class="table align-middle mb-0 mx-5">
                <thead >
                  <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Date</th>
                    <th>Desicion</th>
                  </tr>
                </thead>
                <tbody>
                    {#each  requests.slice(pageCount * 3, pageCount * 3 + 3) as request}
                    
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
                          <p class="text-muted mb-0">Updated {request.period} days ago</p>
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
                   <td class="justify-content-center">
                        <div class="container">
                          <div class="column">
                        {#if request.status == "Rejected"}
                            <div class="row btn-group">
                            <button type="button" class="btn btn-danger btn-sm w-50" disabled>Rejected</button>
                            <button type="button" class="btn w-25 p-0"><i class="bi bi-three-dots-vertical"></i></button>
                          </div>
                        {:else}
                            {#if request.status == "Approved"}
                            <div class="row btn-group">
                                <button type="button" class="btn btn-success btn-sm w-50" disabled>Approved</button>
                                <button type="button" class="btn p-0"><i class="bi bi-three-dots-vertical"></i></button>
                            </div>
                            {:else}
                            <div class="row">
                            <button type="button" class="btn btn-success btn-sm w-50 mb-2   ">Approve</button>
                          </div>
                          <div class="row">
                            <button type="button" class="btn btn-danger btn-sm w-50">Reject</button>
                          </div>
                            {/if}
                        {/if}
                      </div>
                      </div>
                    </td>
                  </tr>
                
                  {/each}
                </tbody>
        </table>

              <div class="pagination">
               <div class="pagination-labels">
                <label class="text-muted mb-0 ">Rows per page:</label>
              </div>
                
              <div class="pagination-labels"> 
                <label class="text-muted mb-0">{pageCount+1} of {totalRequests / pageSize}</label>
                <button class="pagination-button" on:click={decrement}><i class="icon fa-solid fa-chevron-left"></i></button>
                <button class="pagination-button" on:click={increment}><i class="icon fa-solid fa-chevron-right"></i></button>
              </div>
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

.child {
  display: inline-block;
  left: 10cm;
}

.pagination {
  margin-top: 1cm;
  padding-left: 39cm;
}
.pagination-labels {
  margin: 0.1cm;
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
outline: unset !important

}

</style>
