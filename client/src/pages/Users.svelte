<script lang="ts">
  import AllUsers from "../components/users/AllUsers.svelte";

  import Sidebar from "../components/sidebar/Sidebar.svelte";
</script>

<Sidebar>
  <span slot="page-name">Users</span>
  <section class="fluid-container mt-5 content" slot="content">
    <AllUsers />
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
</style>
