<script lang="ts">
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  import AllUsers from "../componants/users/AllUsers.svelte";
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar>
  <div class="container" slot="content">
    <AllUsers bind:isLoading bind:isError />
  </div>
</Sidebar>
