<script lang="ts">
    import UpdateCompensations from '../components/compensations/UpdateCompensations.svelte';
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
    <section class="fluid-container mt-5 content" slot="content">
        <UpdateCompensations bind:isLoading bind:isError />
    </section>
</Sidebar>