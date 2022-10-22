<script lang="ts">
    import UpdateVacation from '../components/vacations/UpdateVacation.svelte';
    import Sidebar from '../components/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar bind:isLoading bind:isError>
    <section class="fluid-container mt-5 content" slot="content">
        <UpdateVacation bind:isLoading bind:isError />
    </section>
</Sidebar>