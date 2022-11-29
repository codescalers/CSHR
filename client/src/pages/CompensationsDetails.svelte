<script lang="ts">
    import CompensationsDetails from '../componants/compensations/CompensationsDetails.svelte';
    import Sidebar from '../componants/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
    <section class="fluid-container mt-5 content" slot="content">
        <CompensationsDetails bind:isLoading bind:isError />
    </section>
</Sidebar>