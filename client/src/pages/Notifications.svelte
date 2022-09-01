<script lang="ts">
    import type { UserInterface } from "../types";
    export let user: UserInterface;
    import Sidebar2 from "../components/sidebar/Sidebar2.svelte";
    
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
    }];
</script>
  
  <Sidebar2 bind:user={user}>
    <span slot="page-name">Notification</span>
    <section class=" fluid-container mt-5" slot="content">

      <div>
          <h4 class="child mx-5">All Notifications</h4>
          <div class="sort">
            <box-icon name='sort-up'></box-icon>
            <label class="text-muted mb-0">Sort</label>
            
            <box-icon name='filter-alt' type='solid' ></box-icon>
            <label class="text-muted mb-0 filter">Filter</label>
            
        </div>
          
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
                    {#each  requests as request }
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
               <div class="pagination-labels"><label class="text-muted mb-0 ">Rows per page:</label></div>
               <div class="pagination-labels">
                <select >
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </div>
              <div class="pagination-labels"> <label class="text-muted mb-0">1-8 of 1240</label> </div>
              <div class="d-flex flex-column">
                <i class="fa fa-angle-up" style="font-size:30px"></i>
              <i class="fa fa-angle-down" style="font-size:30px"></i>
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

.icon {
  padding-right: 0.2cm;
}

</style>