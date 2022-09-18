<script lang="ts">
  import Sidebar from "../components/sidebar/Sidebar.svelte";
  import Team from "../components/team/Team.svelte";
</script>

<Sidebar>
  <span slot="page-name">Team</span>
  <section class="fluid-container mt-5 content" slot="content">
    <Team />
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
</style>
