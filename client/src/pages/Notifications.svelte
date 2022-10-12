<script lang="ts">
  import { onMount } from 'svelte';
  import Alert from "../components/alert/Alert.svelte"
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import NotificationService from "../services/axios/notifications/notifications"
  
  let isLoading = false;
  let isError: boolean | null = null;
  let notifications: any;

  
  onMount(async () => {
    isLoading = true;
    try {
      notifications = await NotificationService.getAll();
      console.log(notifications);
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>
<Sidebar bind:isLoading bind:isError>
    <div class="mt-5" slot="content">
      <h4 class="child">All Notifications</h4>
      
      {#if notifications && notifications.length > 0 }
        <table class="table align-middle mb-0">
          <thead>
            <tr>
              <th>Name</th>
              <th>Role</th>
              <th>Date</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {#each notifications as notification}
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
                      <p class="fw-bold mb-1">{notification.name}</p>
                      <p class="text-muted mb-0">
                        Updated {notification.period} days ago
                      </p>
                    </div>
                  </div>
                </td>
                <td>
                  <p class="fw-bold mb-1">{notification.role}</p>
                  <p class="text-muted mb-0">{notification.date}</p>
                </td>
                <td>
                  <p class="fw-bold mb-1">{notification.date}</p>
                  <p class="text-muted mb-0">{notification.time}</p>
                </td>
                <td>
                  <span class="badge rounded-pill text-bg-{notification.classPill} p-3"
                    >{notification.classPill}</span
                  >
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        <div class="pagination">
          <div class="pagination-labels">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="text-muted mb-0 ">Rows per page:</label>
          </div>

          <div class="pagination-labels">
            <!-- svelte-ignore missing-declaration -->
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="text-muted mb-0"
              ></label
            >
            <button class="pagination-button"
              ><i class="icon fa-solid fa-chevron-left" /></button
            >
            <button class="pagination-button"
              ><i class="icon fa-solid fa-chevron-right" /></button
            >
          </div>
        </div>
      {:else}
        <div class="mt-4">
          <Alert message = {"There are no notifications"} title={"No notifications found"} type={"primary"}/>
        </div>
      {/if}
      </div>
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
    outline: unset !important;
  }
</style>
