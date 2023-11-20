<script lang="ts">
  import AllUsers from "../componants/users/AllUsers.svelte";
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar>
  <div class="container" slot="content">
    <AllUsers bind:isLoading bind:isError />
  </div>
</Sidebar>
