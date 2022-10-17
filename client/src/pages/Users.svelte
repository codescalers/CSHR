<script lang="ts">
  import AllUsers from '../components/users/AllUsers.svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar bind:isLoading bind:isError>
  <div class="container" slot="content">
    <AllUsers bind:isLoading bind:isError />
  </div>
</Sidebar>
