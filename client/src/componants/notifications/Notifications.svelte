<script lang="ts">
  export let notifications: any;
  import ProfileImage from "../profile/ProfileImage.svelte";
  import { Link } from "svelte-navigator";
</script>

<div>
  {#if notifications && notifications.length > 0}
    <h4 class="child mx-5 mt-4">All Notifications</h4>
    <table class="table align-middle">
      <thead>
        <tr>
          <th>User</th>
          <th>Content</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each notifications as notification}
          <tr>
            <td>
              <div class="d-flex align-items-center">
                <ProfileImage user={notification.user} />
                <div class="ms-3">
                  <p class="fw-bold mb-1">{notification.user.full_name}</p>
                  <p class="text-muted mb-0">
                    {notification.user.job_title}
                  </p>
                </div>
              </div>
            </td>
            <td>
              <p class="fw-bold mb-1">{notification.title}</p>
              <p class="text-muted mb-0">{notification.created_at}</p>
            </td>
            {#if notification.type != "official-document"}
              <td>
                <Link
                  class="text-dark"
                  to="/{notification.type}/{notification.event_id}"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="22"
                    height="22"
                    fill="currentColor"
                    class="bi bi-eye-fill"
                    viewBox="0 0 16 16"
                  >
                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z" />
                    <path
                      d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"
                    />
                  </svg>
                </Link>
              </td>
            {:else}
              <td> -- </td>
            {/if}
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <div
      class="mt-4 d-flex height-100 justify-content-center align-items-center"
    >
      <div class="row">
        <div class="col-12 d-flex justify-content-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="50"
            height="50"
            fill="currentColor"
            class="bi bi-bell-slash-fill"
            viewBox="0 0 16 16"
          >
            <path
              d="M5.164 14H15c-1.5-1-2-5.902-2-7 0-.264-.02-.523-.06-.776L5.164 14zm6.288-10.617A4.988 4.988 0 0 0 8.995 2.1a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 7c0 .898-.335 4.342-1.278 6.113l9.73-9.73zM10 15a2 2 0 1 1-4 0h4zm-9.375.625a.53.53 0 0 0 .75.75l14.75-14.75a.53.53 0 0 0-.75-.75L.625 15.625z"
            />
          </svg>
        </div>
        <div class="col-12 d-flex justify-content-center">
          <div class="mt-4 pt-4 mb-4 pb-4 d-flex">
            <h4>Will let you know when you have updates.</h4>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .child {
    display: inline-block;
    left: 10cm;
  }

  /* .pagination {
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
    } */
</style>
