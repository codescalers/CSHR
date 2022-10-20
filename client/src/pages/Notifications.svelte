<script lang="ts">
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import { onMount } from 'svelte';
  import NotificationService from "../services/axios/notifications/notifications"
  import ProfileImage from '../components/profile/ProfileImage.svelte';
  import { Link } from 'svelte-navigator';

  let isLoading = false;
  let isError: boolean | null = null;
  let notifications: any;

  onMount(async () => {
    isLoading = true;
    try {
      notifications = await NotificationService.getAll();
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

<Sidebar>
  <section class=" fluid-container mt-5" slot="content">
    <div>
      <h4 class="child mx-5">All Notifications</h4>

      <table class="table align-middle mb-0 mx-5">
        <thead>
          <tr>
            <th>User</th>
            <th>Content</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {#if notifications}
            {#each notifications as notification}
                <tr>
                  <td>
                    <div class="d-flex align-items-center">
                      <ProfileImage user={JSON.parse(notification.user)}/>
                      <div class="ms-3">
                        <p class="fw-bold mb-1">{JSON.parse(notification.user).full_name}</p>
                        <p class="text-muted mb-0">
                          {JSON.parse(notification.user).user_type}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <p class="fw-bold mb-1">{notification.title}</p>
                    <p class="text-muted mb-0">{notification.created_at}</p>
                  </td>
                  <td>
                    <Link class="text-dark" to="/{notification.type}/{notification.event_id}">
                      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                        <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
                        <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
                      </svg>
                    </Link>
                  </td>
                </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
  </section>
</Sidebar>

<style>
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
