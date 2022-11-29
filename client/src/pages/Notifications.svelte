<script lang="ts">
    import Sidebar from '../componants/sidebar/Sidebar.svelte';
    import { onMount } from 'svelte';
    import notificationsAPI from "../apis/notifications/Notifications"
    import Notifacations from "../componants/notifications/Notifications.svelte"
  
    let isLoading = false;
    let isError: boolean | null = null;
    let notifications: any;
  
    onMount(async () => {
      isLoading = true;
      try {
        notifications = await notificationsAPI.getAll();
      } catch (error) {
        isError = true;
      }
      isLoading = false;
    });
  </script>
  
<Sidebar>
    <section class=" fluid-container mt-5" slot="content">
        <Notifacations bind:notifications/>
    </section>
</Sidebar>
  