<script lang="ts">
  import Sidebar from "../components/sidebar/Sidebar.svelte";
  import Team from "../components/team/Team.svelte";
</script>

<Sidebar>
  <span slot="page-name">Team</span>
  <div slot="content">
    <Team />
  </div>
</Sidebar>

