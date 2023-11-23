<script lang="ts">
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  import VacationDetails from "../componants/vacations/VacationDetails.svelte";
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar>
  <section class="fluid-container mt-5 content" slot="content">
    <VacationDetails bind:isLoading bind:isError />
  </section>
</Sidebar>
