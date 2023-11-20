<script lang="ts">
  import OffcialDocument from "../componants/hr_letter/OffcialDocument.svelte";
  import Sidebar from "../componants/sidebar/Sidebar.svelte";
  export let isLoading = false;
  export let isError: boolean | null = null;
</script>

<Sidebar>
  <section class="mt-5 content" slot="content">
    <OffcialDocument bind:isLoading bind:isError />
  </section>
</Sidebar>
