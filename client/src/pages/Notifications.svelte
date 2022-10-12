<script lang="ts">
  import { onMount } from 'svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import NotificationService from "../services/axios/notifications/notifications"
  
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

  // let pageCount = 0;
  // let pageSize = 3;
  // function increment() {
  //   if (totalNotifications - pageCount * 3 - pageSize > 0) {
  //     pageCount++;
  //   }
  // }
  // function decrement() {
  //   if (pageCount > 0) {
  //     pageCount--;
  //   }
  // }
  // let totalNotifications = requests.length;
</script>
{#if notifications}
  <Sidebar bind:isLoading bind:isError>
    <div slot="content">

    </div>
  </Sidebar>
{/if}
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
