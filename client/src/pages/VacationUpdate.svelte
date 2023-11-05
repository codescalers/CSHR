<script lang="ts">
    import UpdateVacation from '../componants/vacations/UpdateVacation.svelte';
    import Sidebar from '../componants/sidebar/Sidebar.svelte';
    export let isLoading = false;
    export let isError: boolean | null = null;
</script>
  
<Sidebar>
    <section class="fluid-container mt-5 content" slot="content">
        <UpdateVacation bind:isLoading bind:isError />
    </section>
</Sidebar>