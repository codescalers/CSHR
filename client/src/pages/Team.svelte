<script lang="ts">
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  import Team from '../components/team/Team.svelte';

  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar bind:isLoading bind:isError>
  <div slot="content">
    <Team bind:isLoading bind:isError />
  </div>
</Sidebar>
