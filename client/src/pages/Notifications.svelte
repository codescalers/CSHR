<script lang="ts">
    import type { UserInterface } from "../types";
    export let user: UserInterface;
    import Sidebar2 from "../components/sidebar/Sidebar2.svelte";
   
    let pageCount = 0;
    let pageSize = 3;    
    let requests = [{
        "name" : "Marc",
        "period": 2,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "classPill":"danger",
    },
    {
        "name" : "Joe",
        "period": 3,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "classPill":"primary",
    },
    {
        "name" : "Joe",
        "period": 3,
        "role": "Software Engineer",
        "date": "28 May, 2000",
        "time": "6.30",
        "classPill":"primary",
    },
    {
        "name" : "Michael",
        "period": 2,
        "role": "Engineering Manager",
        "date": "28 May, 2000",
        "time": "6.33",
        "classPill":"danger",
    },
    {
        "name" : "Marwan",
        "period": 3,
        "role": "SRE",
        "date": "28 May, 2000",
        "time": "6.33",
        "classPill":"primary",
    },
    {
        "name" : "Joel",
        "period": 3,
        "role": "QA Engineer",
        "date": "28 May, 2000",
        "time": "6.33",
        "classPill":"primary",
    },
    ];
    function increment() {
      if (totalNotifications - (pageCount * 3) - pageSize  > 0 ){
          pageCount++;
      }
    }
    function decrement() {
      if (pageCount > 0 ){
          pageCount--;
      }
    }
    let totalNotifications = requests.length;
</script>
  
  <Sidebar2 bind:user={user}>
    <span slot="page-name">Notification</span>
    <section class=" fluid-container mt-5" slot="content">

      <div>
          <h4 class="child mx-5">All Notifications</h4>
          
          
         <table class="table align-middle mb-0 mx-5">
                <thead >
                  <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Date</th>
                    <th>Type</th>
                  </tr>
                </thead>
                <tbody>
                    {#each  requests.slice(pageCount * 3, pageCount * 3 + 3) as request}
                  <tr>
                    <td>
                      <div class="d-flex align-items-center">
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
                   <td>
                      <span class="badge rounded-pill text-bg-{request.classPill} p-3">{request.classPill}</span>
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
                <label class="text-muted mb-0">{pageCount+1} of {totalNotifications / pageSize}</label>
                <button class="paginatin-button" on:click={decrement}><i class="icon fa-solid fa-chevron-left"></i></button>
                <button class="paginatin-button" on:click={increment}><i class="icon fa-solid fa-chevron-right"></i></button>
              </div>
              </div>
              
          </div>        
    </section>
</Sidebar2>
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
.paginatin-button {
  background: unset !important;
border: unset !important;
outline: unset !important

}

</style>