<script lang="ts">
  import Requests from '../components/requests/Requests.svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
</script>

<Sidebar>
  <section slot="content">
    <Requests />
  </section>
</Sidebar>

