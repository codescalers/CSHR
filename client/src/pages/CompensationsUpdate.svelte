<script lang="ts">
  import UpdateCompensations from "../componants/compensations/UpdateCompensations.svelte";
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar>
  <section class="fluid-container mt-5 content" slot="content">
    <UpdateCompensations bind:isLoading bind:isError />
  </section>
</Sidebar>
