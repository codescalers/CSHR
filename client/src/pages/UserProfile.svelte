<script lang="ts">
  import Profile from "../components/profile/Profile.svelte";
  import Sidebar from "../components/sidebar/Sidebar.svelte";
</script>

<Sidebar>
  <span slot="page-name" />
  <section class="fluid-container mt-5 content" slot="content">
    <Profile />
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
</style>
