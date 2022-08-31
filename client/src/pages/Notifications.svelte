<script lang="ts">
    import type { UserInterface } from "../types";
    export let user: UserInterface;
    import Sidebar2 from "../components/sidebar/Sidebar2.svelte";
  </script>
  
  <Sidebar2 bind:user={user}>
    <span slot="page-name">Notification</span>
    <section class="fluid-container mt-5" slot="content">
        <div class="container my-5">
            <div class="shadow-4 rounded-5 overflow-hidden">
              <table class="table align-middle mb-0 bg-white">
                <thead class="bg-light">
                  <tr>
                    <th>Name</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Position</th>
                  </tr>
                </thead>
                <tbody>
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
                          <p class="fw-bold mb-1">John Doe</p>
                          <p class="text-muted mb-0">john.doe@gmail.com</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <p class="fw-bold mb-1">Software engineer</p>
                      <p class="text-muted mb-0">IT department</p>
                    </td>
                    <td>
                      <span class="badge badge-success rounded-pill">Active</span>
                    </td>
                    <td>Senior</td>
                   
                  </tr>
                </tbody>
              </table>
            </div>
          </div>        
    </section>
</Sidebar2>
<style>
    body {
  background-color: hsl(0, 0%, 94%)
}
</style>